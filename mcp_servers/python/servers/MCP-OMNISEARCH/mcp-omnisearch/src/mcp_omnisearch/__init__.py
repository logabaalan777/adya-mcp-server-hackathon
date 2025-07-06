"""
MCP-OMNISEARCH Server

A Model Context Protocol (MCP) server for OmniSearch.

This server is used to search for articles and documents in the OmniSearch database.
"""

__version__ = "0.1.0"
__author__ = "MCP Logabaalan"
__description__ = "MCP server for OmniSearch"


from . import server
import asyncio


def main():
    """Main entry point for the package."""
    # print("Running main")
    asyncio.run(server.main())

# Optionally expose other important items at package level
__all__ = ['main', 'server']