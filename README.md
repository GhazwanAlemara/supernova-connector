# Supernova Connector 🚀

The official Python Model Context Protocol (MCP) client for [Supernova.cool](https://supernova.cool) — the Universal Agent Tool Platform.

By using this connector, you can expose the entire Supernova Registry (516+ tools, routing, and A2A financial rails) directly into your native agent environments, frameworks, and IDEs (like Cursor or Claude Desktop).

## 📦 Installation

This connector can be installed directly from PyPI (once published) or via `npx` for MCP integration.

```bash
# Node environment (for Cursor / Claude Desktop)
npx -y @supernova/connector
```

## 🌌 MCP Features
This connector currently exposes the following native tools to your AI agent/IDE:

- **`discover_tools`**: Semantic routing powered by Gemini 1.5 Flash to find the exact tool your agent needs based on natural language intent.
- **`execute_tool`**: Secure execution of any tool in the Supernova registry via our zero-trust Wasm/GVisor proxy.
- **`transfer_credits`**: Built-in A2A (Agent-to-Agent) payments. Send NOVA credits to another agent ID instantly.
- **`check_solvency`** (New!): Cryptographically verify if a target agent has sufficient funds before engaging in a transaction.

## 🚀 Quick Start (IDE)

### Cursor Integration
1. Open Cursor Settings (`Cmd/Ctrl + Shift + J`).
2. Navigate to **Features** > **MCP**.
3. Click **+ Add New MCP Server**.
4. Set Name to `supernova`, Type to `command`, and Command to `npx -y @supernova/connector`.

### Claude Desktop Integration
Update your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "supernova": {
      "command": "npx",
      "args": ["-y", "@supernova/connector"]
    }
  }
}
```

## 🔒 Security
All proxy executions are run in isolated environments and scanned for prompt injections. Your API keys are never exposed directly to the executing tools.
