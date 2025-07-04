from mcp.types import Tool, TextContent
from .toolhandler import ToolHandler
import os
import datetime
import psutil

class GetAlacrittyUsageToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_alacritty_usage")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get Alacritty usage statistics: number of running processes, uptime, CPU and memory usage.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )

    async def run_tool(self, args: dict) -> list[TextContent]:
        try:
            alacritty_procs = [
                p for p in psutil.process_iter(['pid', 'name', 'create_time', 'cpu_percent', 'memory_info'])
                if p.info['name'].lower() == 'alacritty'
            ]
            count = len(alacritty_procs)

            if count == 0:
                return [TextContent(type="text", text="No Alacritty processes are currently running.")]

            lines = [f"Alacritty processes running: {count}"]

            for p in alacritty_procs:
                uptime_seconds = int(datetime.datetime.now().timestamp() - p.info['create_time'])
                uptime_str = str(datetime.timedelta(seconds=uptime_seconds))
                mem_mb = p.info['memory_info'].rss / (1024 * 1024)
                cpu = p.cpu_percent(interval=0.1)

                lines.append(
                    f"\nPID: {p.pid}\n"
                    f"  Uptime: {uptime_str}\n"
                    f"  CPU Usage: {cpu:.2f}%\n"
                    f"  Memory Usage: {mem_mb:.2f} MB"
                )

            return [TextContent(type="text", text="\n".join(lines))]

        except Exception as e:
            return [TextContent(type="text", text=f"Error fetching Alacritty usage: {e}")]
