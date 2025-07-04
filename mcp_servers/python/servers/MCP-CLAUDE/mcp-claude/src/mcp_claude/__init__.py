"""
MCP-CLAUDE Server

A Model Context Protocol (MCP) server for Claude AI.
Provides tools for querying data, managing articles, and analyzing insights.
"""

__version__ = "0.1.0"
__author__ = "MCP Logabaalan"
__description__ = "MCP server for Claude AI"


from . import server
import asyncio


def main():
    """Main entry point for the package."""
    # print("Running main")
    asyncio.run(server.main())

# Optionally expose other important items at package level
__all__ = ['main', 'server']