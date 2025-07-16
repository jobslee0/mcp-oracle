import os
import sys
import signal
from typing import Any
from mcp.server.fastmcp import FastMCP
import Oracle11gTools as oracle_tools
from dotenv import load_dotenv


# Load the environment variables
load_dotenv()

# Initialize the FastMCP server
mcp = FastMCP("DbOracleGetMcp")

oracle_tools.oracle_user = os.getenv("ORACLE_USER")
oracle_tools.oracle_password = os.getenv("ORACLE_PASSWORD")
oracle_tools.oracle_url = os.getenv("ORACLE_URL")
oracle_tools.lib_path = os.getenv("ORACLE_HOME")


@mcp.tool()
async def list_tables() -> str:
    """Get a list of all tables in the oracle database

    Args:
        None
    """
    return await oracle_tools.list_tables()


@mcp.tool()
async def describe_table(table_name: str) -> str:
    """Get a description of a table in the oracle database"

    Args:
        table_name (string): The name of the table to describe
    """
    return await oracle_tools.describe_table(table_name)


@mcp.tool()
async def reqd_query(query: str) -> str:
    """Execute SELECT queries to read data from the oracle database

    Args:
        query (string): The SELECT query to execute
    """
    return await oracle_tools.read_query(query)


def main() -> None:
    mcp.run(transport='stdio')

