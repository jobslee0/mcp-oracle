import asyncio
from dotenv import load_dotenv
from mcp_server_jysd_cx_oracle import oracle_tools

# Load environment variables from .env file
load_dotenv()

async def main():
    # Test listing tables
    tables = await oracle_tools.list_tables()
    print("Tables in database:")
    print(tables)
    
    # Test describing a table (replace 'YOUR_TABLE_NAME' with an actual table name)
    # table_desc = await oracle_tools.describe_table('YOUR_TABLE_NAME')
    # print("\nTable description:")
    # print(table_desc)
    
    # Test running a query (replace with a valid query for your database)
    # query_result = await oracle_tools.read_query('SELECT * FROM YOUR_TABLE_NAME WHERE ROWNUM < 5')
    # print("\nQuery result:")
    # print(query_result)

if __name__ == "__main__":
    asyncio.run(main())
