#!/usr/bin/env python3
"""
MCP-LOOKER Server Main Entry Point

This script runs the MCP-LOOKER server for Looker data analytics platform.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_looker.server import main

if __name__ == "__main__":
    main()
