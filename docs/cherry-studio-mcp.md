# Cherry Studio MCP 接入指南

这个接入方式面向普通用户：用户继续使用 Cherry Studio 的图形界面和模型配置，Mondo 只作为本地工作系统工具接入。

## 用户会得到什么

接入后，Cherry Studio 里的 Mondo 助手可以：

- 引导用户完成第一轮个人工作系统初始化访谈。
- 采集长期方向、当前项目、AI 边界和本周主线。
- 生成初始化草稿，等用户确认后再写入工作区。
- 初始化一个 Mondo 工作区。
- 检查工作区是否缺关键文件。
- 扫描 Daily、行动池和项目状态。
- 把一句口述输入初步分流到 Daily、行动池、项目、沉淀区或 Inbox。
- 生成 `.mondo/live-state.json`，让系统状态尽快更新。
- 生成 `.mondo/agent-context.md`，让普通对话 Agent 读到最新工作现场。
- 生成第一位内测执行包，让主持人不用打开命令行也能准备候选用户准入、邀请、配置自检、现场记录、反馈和复盘材料。
- 生成第一位候选用户准入记录，让主持人在图形界面里直接填写 5 个准入问题和结论。
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
1. 新用户不要先做 loose input 分流，先调用 mondo_start_onboarding，带用户完成初始化建模。
2. 初始化阶段先采集长期方向、当前项目、AI 可做/不可做边界、本周主线和当前卡点。
3. 采集长期方向后调用 mondo_collect_identity；采集项目口述后调用 mondo_collect_projects。
4. 生成草稿后，先让用户确认长期方向、项目归属、主线项目和第一步动作。
5. 用户确认后，才调用 mondo_confirm_onboarding 写入工作区。
6. 进入 active_daily_flow 后，再使用 mondo_scan、mondo_export_context、mondo_route_input 和 mondo_append_markdown 做日常流转。
7. 准备第一位真实用户内测时，可以调用 mondo_prepare_beta_pack 生成本地执行包，并调用 mondo_prepare_beta_intake 生成候选用户准入记录；再按 `docs/beta-user-selection.md` 和 `docs/beta-user-intake-template.md` 先筛选候选用户。
8. 需要写入文件前，先用自然语言说明将写入哪个文件、写入什么内容，并等待用户确认。
9. 用户确认后，才调用 mondo_append_markdown 写入。
10. 不写入密钥、token、密码、私钥、服务器 IP、客户隐私或完整登录命令。
11. Daily 只放今天要执行的动作；跨天动作放行动池；项目进展写回项目文件；重大转向写决策日志。
12. 不要试图替用户一次性整理完整个知识库，每次只推进一个清晰动作。
```

## 内测用户第一步

第一轮内测不验证“分流一句话”，而是验证用户能不能被带着建立完整工作现场。

用户可以在 Cherry Studio 里直接说：

```text
请开始帮我建立个人 AI 工作系统，工作区放在 D:/MondoWorkOS。
```

助手应该先问：

```text
你长期想把工作和生活变成什么样？
未来 3-6 个月最重要的方向是什么？
你现在手上有哪些项目？
每个项目现在做到哪一步？
哪些是本周主线，哪些只是保活或等待？
AI 可以帮你做什么，不能自动做什么？
```

用户说完后，助手应该生成初始化草稿，让用户确认，再写入工作区。

内测记录重点：

- 用户是否知道自己该说什么。
- 用户是否能一次讲出长期方向和当前项目。
- 用户是否理解系统生成的项目状态和下一步。
- 用户是否能接受“先建模，再日常流转”的节奏。
- 用户是否会卡在安装、MCP 配置、工作区路径或模型权限上。

## 初始化之后怎么日常使用

早上用户可以说：

```text
帮我做今天早间整理。
```

助手应该读取行动池、当天 Daily 和项目 `_next.md`，只抽今天能执行的动作。

白天用户可以说：

```text
我刚和客户聊完，下周要给他看方案。
```

助手应该先判断这是项目状态、下一步动作、等待事项还是 Daily 临时事项，再说明写入建议。

晚上用户可以说：

```text
帮我晚间收口。
```

助手应该引导用户确认：

- 今天完成了什么。
- 未完成动作回流哪里。
- 哪些项目状态变化需要写入 `_当前状态.md`。
- 哪些重大取舍需要写入 `决策日志.md`。
- 明天第一步是什么。

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
