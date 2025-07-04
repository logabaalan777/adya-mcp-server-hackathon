"""
MCP-LOOKER Server

A Model Context Protocol (MCP) server for Looker data analytics platform.
Provides tools for querying data, managing dashboards, and analyzing insights.
"""

__version__ = "0.1.0"
__author__ = "MCP Logabaalan"
__description__ = "MCP server for Looker data analytics platform"

from . import server
import asyncio


def main():
    """Main entry point for the package."""
    # print("Running main")
    asyncio.run(server.main())

__all__ = ['main', 'server']