"""
MCP-ALACRITTY Server

A Model Context Protocol (MCP) server for Alacritty terminal emulator.
Provides tools for managing Alacritty terminal emulator.
"""

__version__ = "0.1.0"
__author__ = "MCP Logabaalan"
__description__ = "MCP server for Alacritty terminal emulator"

from . import server
import asyncio


def main():
    """Main entry point for the package."""
    # print("Running main")
    asyncio.run(server.main())

__all__ = ['main', 'server']