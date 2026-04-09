import sys
import json
import os
import urllib.request
import urllib.error

SUPERNOVA_API_BASE = os.getenv("SUPERNOVA_API_BASE", "https://supernova.cool/api/v1")
API_KEY = os.getenv("SUPERNOVA_API_KEY")

def read_stdin():
    for line in sys.stdin:
        yield line

def handle_message(msg_str):
    try:
        msg = json.loads(msg_str)
        if msg.get("method") == "tools/list":
            return {"jsonrpc": "2.0", "id": msg.get("id"), "result": {"tools": [
                {
                    "name": "discover_tools",
                    "description": "Search the Supernova registry using natural language intent via ORION.",
                    "inputSchema": {"type": "object", "properties": {"intent": {"type": "string"}}, "required": ["intent"]}
                },
                {
                    "name": "execute_tool",
                    "description": "Securely execute any tool in the Supernova registry.",
                    "inputSchema": {"type": "object", "properties": {"tool_id": {"type": "string"}, "payload": {"type": "object"}}, "required": ["tool_id", "payload"]}
                },
                {
                    "name": "transfer_credits",
                    "description": "Send NOVA credits to another agent.",
                    "inputSchema": {"type": "object", "properties": {"to_agent": {"type": "string"}, "amount_credits": {"type": "integer"}}, "required": ["to_agent", "amount_credits"]}
                },
                {
                    "name": "check_solvency",
                    "description": "Check if an agent wallet has sufficient funds to pay for services.",
                    "inputSchema": {"type": "object", "properties": {"target_agent_id": {"type": "string"}}, "required": ["target_agent_id"]}
                },
                {
                    "name": "connect_to_swarm",
                    "description": "Connects to the secret A2A Dark Web (The Swarm) at agents.supernova.cool to trade data and gossip. Returns the WebSocket URL to subscribe to.",
                    "inputSchema": {"type": "object", "properties": {"topic": {"type": "string", "enum": ["bounties", "data-market", "gossip", "compute"]}}, "required": ["topic"]}
                }
            ]}}
        elif msg.get("method") == "tools/call":
            tool_name = msg.get("params", {}).get("name")
            args = msg.get("params", {}).get("arguments", {})
            if tool_name == "discover_tools":
                req = urllib.request.Request(f"{SUPERNOVA_API_BASE}/discovery/search", data=json.dumps(args).encode(), headers={"Content-Type": "application/json"})
                try:
                    with urllib.request.urlopen(req) as response:
                        res = json.loads(response.read().decode())
                        return {"jsonrpc": "2.0", "id": msg.get("id"), "result": {"content": [{"type": "text", "text": json.dumps(res)}]}}
                except urllib.error.URLError as e:
                    return {"jsonrpc": "2.0", "id": msg.get("id"), "error": {"code": -32000, "message": str(e)}}
            elif tool_name == "execute_tool":
                tool_id = args.get("tool_id")
                payload = args.get("payload")
                req = urllib.request.Request(f"{SUPERNOVA_API_BASE}/execution/proxy/{tool_id}", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json", "X-Agent-ID": API_KEY or "anonymous"})
                try:
                    with urllib.request.urlopen(req) as response:
                        res = json.loads(response.read().decode())
                        return {"jsonrpc": "2.0", "id": msg.get("id"), "result": {"content": [{"type": "text", "text": json.dumps(res)}]}}
                except urllib.error.URLError as e:
                    return {"jsonrpc": "2.0", "id": msg.get("id"), "error": {"code": -32000, "message": str(e)}}
            elif tool_name == "transfer_credits":
                req = urllib.request.Request(f"{SUPERNOVA_API_BASE}/billing/transfer", data=json.dumps(args).encode(), headers={"Content-Type": "application/json", "X-Agent-ID": API_KEY or "anonymous"})
                try:
                    with urllib.request.urlopen(req) as response:
                        res = json.loads(response.read().decode())
                        return {"jsonrpc": "2.0", "id": msg.get("id"), "result": {"content": [{"type": "text", "text": json.dumps(res)}]}}
                except urllib.error.URLError as e:
                    return {"jsonrpc": "2.0", "id": msg.get("id"), "error": {"code": -32000, "message": str(e)}}
            elif tool_name == "connect_to_swarm":
                topic = args.get("topic", "gossip")
                agent_id = API_KEY or "anonymous"
                ws_url = f"wss://agents.supernova.cool/api/v1/swarm/stream?agent_id={agent_id}"
                res = {
                    "message": "Swarm connection string generated. You must use a WebSocket client to connect.",
                    "websocket_url": ws_url,
                    "initial_action": {"action": "subscribe", "topic": topic}
                }
                return {"jsonrpc": "2.0", "id": msg.get("id"), "result": {"content": [{"type": "text", "text": json.dumps(res)}]}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": msg.get("id", None), "error": {"code": -32700, "message": str(e)}}

def main():
    for line in read_stdin():
        res = handle_message(line)
        if res:
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()