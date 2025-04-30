import cx_Oracle
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取连接字符串
connection_string = os.getenv("ORACLE_CONNECTION_STRING")
print(f"尝试连接到: {connection_string}")

try:
    # 初始化 Oracle 客户端
    oracle_home = os.getenv("ORACLE_HOME")
    if oracle_home:
        print(f"初始化 Oracle 客户端: {oracle_home}")
        cx_Oracle.init_oracle_client(lib_dir=oracle_home)
    
    # 连接到数据库
    conn = cx_Oracle.connect(connection_string)
    print("连接成功!")
    
    # 执行简单查询
    cursor = conn.cursor()
    cursor.execute("SELECT 'Hello, Oracle!' FROM DUAL")
    result = cursor.fetchone()
    print(f"查询结果: {result[0]}")
    
    # 关闭连接
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"错误: {e}")
