# Cherry Studio MCP 接入指南

这个接入方式面向普通用户：用户继续使用 Cherry Studio 的图形界面和模型配置，Mondo 只作为本地工作系统工具接入。

## 用户会得到什么

接入后，Cherry Studio 里的 Mondo 助手可以：

- 初始化一个 Mondo 工作区。
- 检查工作区是否缺关键文件。
- 扫描 Daily、行动池和项目状态。
- 把一句口述输入初步分流到 Daily、行动池、项目、沉淀区或 Inbox。
- 生成 `.mondo/live-state.json`，让系统状态尽快更新。
- 生成 `.mondo/agent-context.md`，让普通对话 Agent 读到最新工作现场。
- 在用户确认后，向工作区内的 Markdown 文件追加内容。

## 推荐配置

在 Cherry Studio 的 MCP 配置里添加一个本地 stdio server。

如果你直接使用源码目录：

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

如果你已经用 `pip install -e .` 安装：

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

路径需要替换成你自己的本地仓库路径。

## 推荐助手提示词

```text
你是 Mondo 工作助理。

你不只是回答问题，而是帮助用户维护一个本地 Mondo Agent OS 工作区。

工作规则：
1. 处理工作区任务前，优先调用 mondo_scan 或 mondo_export_context 理解当前状态。
2. 用户给出 loose input 时，先调用 mondo_route_input 判断归属。
3. 需要写入文件前，先用自然语言说明将写入哪个文件、写入什么内容，并等待用户确认。
4. 用户确认后，才调用 mondo_append_markdown 写入。
5. 不写入密钥、token、密码、私钥、服务器 IP、客户隐私或完整登录命令。
6. Daily 只放今天要执行的动作；跨天动作放行动池；项目进展写回项目文件；重大转向写决策日志。
7. 不要试图替用户一次性整理完整个知识库，每次只推进一个清晰动作。
```

## 内测用户第一步

用户可以在 Cherry Studio 里直接说：

```text
请帮我在 D:/MondoWorkOS 初始化一个工作系统，第一个项目叫「我的第一个AI项目」。
```

然后继续说：

```text
我刚想到一个事：下周要给客户发一版方案，你帮我判断应该放到哪里。
```

助手应该先分流，再说明建议写入位置，等用户确认后再写入。

## 这不是完整 Agent

Cherry Studio 负责：

- 图形界面
- 模型接入
- 对话历史
- 短期记忆
- 工具调用

Mondo MCP 负责：

- 工作区初始化
- 工作状态读取
- Daily / 行动池 / 项目状态协议
- 安全边界内的 Markdown 写入
- 给普通 Agent 的上下文导出
