# 第一轮内测配置自检

这份清单给主持人使用。目标是在用户加入前，把技术入口先检查完，避免第一轮内测还没进入口述建模就卡住。

第一轮内测真正要验证的是：

> 用户能不能把混乱工作说出来，并让 AI 建立一个能持续接手的工作现场。

配置只要够用，不要在现场追求完美自动化。

## 1. 仓库状态

在仓库根目录确认：

```bash
git status --short --branch
```

预期：

```text
## main...origin/main
```

如果本地有未提交变更，不要带用户直接内测。先确认这些变更是否会影响 onboarding。

## 2. Runtime 自检

在仓库根目录运行：

```bash
python scripts/verify_runtime.py
python scripts/verify_mcp.py
python scripts/verify_beta_flow.py
```

预期：

- runtime smoke test passed
- mcp smoke test passed
- beta flow verification passed

如果 `verify_beta_flow.py` 失败，不要开始内测。第一轮要先保证初始化建模能跑通。

## 3. Cherry Studio MCP 配置

如果直接使用源码目录，MCP 配置示例：

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

检查：

- 路径已经替换成当前机器上的真实仓库路径。
- `scripts/mondo_mcp.py` 文件存在。
- Cherry Studio 能看到 `mondo-agent-os` MCP server。
- 助手能调用 `mondo_start_onboarding`。

更完整配置见：

- `docs/cherry-studio-mcp.md`

## 4. 工作区准备

建议给用户准备一个空文件夹：

```text
D:/MondoWorkOS
```

检查：

- 文件夹路径不要包含密钥、客户资料或旧项目文件。
- 不要直接拿用户已有 Obsidian vault 做第一轮测试。
- 如果用户要换路径，先确认路径可以被本机读写。

第一轮最好用干净工作区，避免用户误以为系统会自动理解全部历史资料。

## 5. 助手提示词

Cherry Studio 助手需要使用 `docs/cherry-studio-mcp.md` 里的推荐提示词。

重点检查这些规则是否存在：

- 新用户先调用 `mondo_start_onboarding`。
- 不先做 loose input 分流。
- 写入前先让用户确认。
- 不写入密钥、token、密码、私钥、服务器 IP、客户隐私或完整登录命令。
- Daily 只放今天要执行的动作，跨天事项进入行动池。

如果助手一开始就在解释 MCP/API/命令行，说明提示词没有对齐普通用户体验。

## 6. 给用户看的材料

内测前发给用户：

- `docs/beta-invitation-message.md`
- `docs/user-first-day-guide.md`

不要先发完整技术文档。第一位用户只需要知道：

- 准备一个 AI 客户端。
- 准备一个空工作区。
- 准备至少 2 个真实项目。
- 从“请开始帮我建立个人 AI 工作系统……”开始。

## 7. 现场最小流程

主持人现场只按这个顺序走：

1. 用户说启动句。
2. 助手采集长期方向。
3. 助手采集当前项目。
4. 助手生成初始化草稿。
5. 用户确认。
6. 助手写入工作区。
7. 用户复述 Daily、行动池、项目下一步。
8. 主持人记录反馈。

不要在第一轮现场展开高级自动化、定时任务、角色包或多 Agent 调度。

## 8. 如果配置失败

如果用户已经进场但配置失败：

- 不要让用户现场排查太久。
- 记录失败发生在哪一步。
- 用 `docs/beta-feedback-form.md` 标记“不通过：安装/配置阶段阻塞”。
- 复盘时按 `docs/beta-retro-guide.md` 归类为配置问题。

配置失败也是有效内测结果。它说明第一位用户还没到“工作现场”之前就被技术入口挡住了。
