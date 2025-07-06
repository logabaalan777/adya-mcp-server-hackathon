ClientsConfig =[
    "MCP_CLIENT_AZURE_AI",
    "MCP_CLIENT_OPENAI",
	"MCP_CLIENT_GEMINI",
	"MCP_CLIENT_OPENSTREETMAP",
	"MCP_CLIENT_JOOMLA",
	"MCP_CLIENT_ALACRITTY",
    "MCP_CLIENT_OMNISEARCH"
]

ServersConfig = [
	{
		"server_name": "MCP-OPENSTREETMAP",
		"command":"uv",
		"args": [
			"--directory",
			"../servers/MCP-OPENSTREETMAP/mcp-openstreetmap",
			"run",
			"mcp-openstreetmap"
		]
	},
	{
		"server_name": "MCP-CLAUDE",
		"command":"uv",
		"args": [
			"--directory",
			"../servers/MCP-CLAUDE/mcp-claude",
			"run",
			"mcp-claude"
		]
	},
	{
		"server_name": "MCP-JOOMLA",
		"command":"uv",
		"args": [
			"--directory",
			"../servers/MCP-JOOMLA/mcp-joomla",
			"run",
			"mcp-joomla"
		]
	},
	{
		"server_name": "MCP-ALACRITTY",
		"command":"uv",
		"args": [
			"--directory",
			"../servers/MCP-ALACRITTY/mcp-alacritty",
			"run",
			"mcp-alacritty"
		]
	},
    {
		"server_name":"MCP-OMNISEARCH",
		"command":"uv",
		"args": [
			"--directory",
			"../servers/MCP-OMNISEARCH/mcp-omnisearch",
			"run",
			"mcp-omnisearch"
		]
	}
]