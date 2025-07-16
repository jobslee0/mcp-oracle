import oracledb
import asyncio
import os

# 数据库连接配置 - 请根据实际环境修改
oracle_user = ""
oracle_password = ""
oracle_url = ""
connection_config = {
    'user':oracle_user,
    'password':oracle_password,
    'dsn':oracle_url
}

# 初始化Oracle客户端
lib_path = ""
if lib_path:
    oracledb.init_oracle_client(lib_dir=lib_path)


async def list_tables() -> list:
    tables = []
    try:
        # 在单独线程中运行数据库操作
        def db_operation():
            result_tables = []
            with oracledb.connect(**connection_config) as conn:
                cursor = conn.cursor()
                # Oracle 11g使用user_tables视图获取当前用户表
                cursor.execute(
                    "SELECT table_name FROM user_tables ORDER BY table_name")
                for row in cursor:
                    result_tables.append(row[0])
            return '\n'.join(result_tables)

        return await asyncio.to_thread(db_operation)
    except oracledb.DatabaseError as e:
        print('发生错误:', e)
        return str(e)


async def describe_table(table_name: str) -> str:
    try:
        # 在单独线程中运行数据库操作
        def db_operation(table):
            with oracledb.connect(**connection_config) as conn:
                cursor = conn.cursor()

                # 创建CSV表头
                result = [
                    "COLUMN_NAME,DATA_TYPE,NULLABLE,DATA_LENGTH,PRIMARY_KEY,FOREIGN_KEY"
                ]

                # 获取主键列 (Oracle 11g使用user_constraints和user_cons_columns)
                pk_columns = []
                cursor.execute(
                    """
                    SELECT cols.column_name
                    FROM user_constraints cons, user_cons_columns cols
                    WHERE cons.constraint_type = 'P'
                    AND cons.constraint_name = cols.constraint_name
                    AND cols.table_name = :table_name
                    """,
                    table_name=table.upper()
                )
                for row in cursor:
                    pk_columns.append(row[0])

                # 获取外键列和引用关系 (Oracle 11g适配)
                fk_info = {}
                cursor.execute(
                    """
                    SELECT a.column_name, c_pk.table_name as referenced_table, b.column_name as referenced_column
                    FROM user_cons_columns a
                    JOIN user_constraints c ON a.constraint_name = c.constraint_name
                    JOIN user_constraints c_pk ON c.r_constraint_name = c_pk.constraint_name
                    JOIN user_cons_columns b ON c_pk.constraint_name = b.constraint_name
                    WHERE c.constraint_type = 'R'
                    AND a.table_name = :table_name
                    """,
                    table_name=table.upper()
                )
                for row in cursor:
                    fk_info[row[0]] = f"{row[1]}.{row[2]}"

                # 获取主要列信息
                cursor.execute(
                    """
                    SELECT column_name, data_type, nullable, data_length 
                    FROM user_tab_columns 
                    WHERE table_name = :table_name 
                    ORDER BY column_id
                    """,
                    table_name=table.upper()
                )

                rows_found = False
                for row in cursor:
                    rows_found = True
                    column_name = row[0]
                    data_type = row[1]
                    nullable = row[2]
                    data_length = str(row[3])
                    is_pk = "YES" if column_name in pk_columns else "NO"
                    fk_ref = fk_info.get(column_name, "NO")

                    # 格式化为CSV行
                    result.append(
                        f"{column_name},{data_type},{nullable},{data_length},{is_pk},{fk_ref}")

                if not rows_found:
                    return f"表 {table} 不存在或没有列."

                return '\n'.join(result)

        return await asyncio.to_thread(db_operation, table_name)
    except oracledb.DatabaseError as e:
        print('发生错误:', e)
        return str(e)


async def read_query(query: str) -> str:
    try:
        # 检查查询是否为SELECT语句
        if not query.strip().upper().startswith('SELECT'):
            return "错误: 仅支持SELECT语句."

        # 在单独线程中运行数据库操作
        def db_operation(query):
            with oracledb.connect(**connection_config) as conn:
                cursor = conn.cursor()
                cursor.execute(query)  # 先执行查询

                # 执行查询后获取列名
                columns = [col[0] for col in cursor.description]
                result = [','.join(columns)]  # 添加列标题

                # 处理每一行
                for row in cursor:
                    # 将元组中的每个值转换为字符串
                    string_values = [
                        str(val) if val is not None else "NULL" for val in row]
                    result.append(','.join(string_values))

                return '\n'.join(result)

        return await asyncio.to_thread(db_operation, query)
    except oracledb.DatabaseError as e:
        print('发生错误:', e)
        return str(e)


if __name__ == "__main__":
    # 创建并运行异步事件循环
    async def main():
        # 示例用法
        print(await list_tables())
        # print(await describe_table('CONTACT'))
        # print(await read_query('SELECT * FROM CONTACT WHERE ROWNUM <= 10'))
        pass  # 添加空操作语句避免缩进错误
    asyncio.run(main())

