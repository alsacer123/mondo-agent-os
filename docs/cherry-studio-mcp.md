# Cherry Studio Optional MCP Helpers

For normal use, start with `docs/cherry-studio-agent-guide.md`.

Cherry Studio should operate Mondo Agent OS as a full agent client with model reasoning, memory, and local file access. Mondo MCP is optional. Use it mainly for:

- workspace diagnosis;
- workspace scanning;
- live state export;
- compact context export;
- role-pack listing.

## Optional MCP Configuration

If you use the repository directly:

```json
{
  "mcpServers": {
    "mondo-agent-os": {
      "command": "python",
      "args": [
        "D:/AI_Workspace/outputs/ip-content-system/mondo-agent-os/scripts/mondo_mcp.py"
      ]
    }
  }
}
```

If you installed the package:

```json
{
  "mcpServers": {
    "mondo-agent-os": {
      "command": "mondo-mcp",
      "args": []
    }
  }
}
```

Replace the path with your local repository path.

Do not make MCP the main decision engine. Let the Cherry Studio assistant read the Mondo OS files, understand the user's work, and write back according to the OS rules.
