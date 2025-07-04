"""
MCP-OPENSTREETMAP Server

A Model Context Protocol (MCP) server for OpenStreetMap.
Provides tools for querying data, managing articles, and analyzing insights.
"""

__version__ = "0.1.0"
__author__ = "MCP Logabaalan"
__description__ = "MCP server for OpenStreetMap"


from . import server
import asyncio


def main():
    """Main entry point for the package."""
    # print("Running main")
    asyncio.run(server.main())

# Optionally expose other important items at package level
__all__ = ['main', 'server']