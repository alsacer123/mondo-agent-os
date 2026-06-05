# Mondo Agent OS｜蒙多 AI 工作系统

一个给个人和小团队使用的 AI 工作系统协议与工具包。

它不是笔记美化模板，也不是新的聊天客户端。它的长期目标是：

> 帮客户把混乱的工作变成一个 AI 能持续接手的工作现场。

用户不需要先理解 MCP、API、Agent 架构或文件系统。理想体验是：用户说清楚自己的长期方向和当前项目，Mondo 帮他建立工作现场；之后每天继续说人话，Agent 能围绕 Daily、行动池、项目状态和下一步持续推进。

## 为什么要用它

大多数人不是不会用 AI，而是每次都要重新给 AI 解释：

- 这个项目是什么；
- 现在做到哪一步；
- 哪些文件能读；
- 什么不能碰；
- 做完应该写回哪里；
- 明天怎么接着推进。

Mondo Agent OS 把这些信息变成一套固定的工作现场。你不需要先学复杂工具，也不需要等完整自动化系统搭好，只要先让 AI 读得到项目规则、当前状态和唯一下一步，它就能开始稳定参与真实工作。

客户体验目标：

1. 第一天：被引导完成长期方向和项目现场录入。
2. 初始化后：看到自己的项目、状态、下一步和行动池。
3. 每天早上：不用从零想今天做什么，系统能接上昨天和项目状态。
4. 白天：随口说的新事项不会丢，会被判断归属和写回。
5. 晚上：不是写日记，而是把完成、未完成、项目变化和明天第一步收口。

当前版本包含四层：

- Markdown OS：项目规则、当前状态、唯一下一步、决策日志、Daily、行动池。
- CLI Runtime：初始化、扫描、诊断、 loose input 路由和角色包列表。
- MCP Server：让 Cherry Studio 这类图形化 AI 客户端把 Mondo 当成本地工作系统工具使用。
- Onboarding Flow：先采集长期方向和项目现场，确认后再生成工作区，而不是从分流一句话开始。
- Agent Skill：让 Codex/Claude 这类 Agent 能按同一套规则生成和维护工作区。
- Role Packs：按角色加载不同工作协议，当前先内置内容生产型个人品牌和工作推进型雏形。

## 适合谁

- 正在用 ChatGPT、Claude、Codex、Cursor、DeepSeek 等 AI 工具推进真实项目的人。
- 项目很多、上下文分散、经常需要反复给 AI 解释背景的人。
- 想把个人工作、内容生产、项目管理或客户交付接入 AI 的个人或小团队。
- 不想学复杂项目管理软件，只想让 AI 真正接得住工作现场的人。

## 核心思想

AI 真正缺的通常不是 prompt，而是项目现场。

这个模板把每个项目拆成 5 个固定入口：

- `_项目规则.md`：这个项目里 AI 必须遵守的边界和写回规则。
- `_总览.md`：项目长期定位、目标、结构和背景。
- `_当前状态.md`：项目现在到了哪一步，哪些判断已经成立。
- `_next.md`：当前唯一下一步，避免 AI 和人同时开太多线。
- `决策日志.md`：重大转向和不可逆取舍，避免以后反复争论。

再配合全局入口：

- `_索引.md`：AI 进入整个工作区时先读的总索引。
- `40_Daily/_行动池.md`：跨项目动作、灵感、等待事项的缓冲区。
- `40_Daily/days/YYYY-MM-DD.md`：只安排今天真正要做的事。

## 免费模板和陪跑服务的边界

这个仓库公开的是基础骨架和运行规则，不保证复制后立刻适合每个人。

真正让系统变好用的，不是文件名本身，而是把你的真实工作场景接进来：

- 哪些项目应该进入系统？
- 哪些信息应该留在项目里，哪些应该放外部工作区？
- 每天从行动池抓什么，不抓什么？
- 当前唯一下一步怎么写，AI 才能真的推进？
- 项目完成后结果应该写回状态、决策日志，还是沉淀成方法？

这些需要结合真实业务判断。模板解决“系统应该长什么样”，AI 赋能陪跑解决“你的工作应该怎么接进去”。

## 你可以怎么使用

这个仓库适合：

- 了解 AI 工作系统的基本结构。
- 自己搭一个最小可用版本。
- 让 Agent/AI 读到项目规则和下一步。
- 体验 Daily、行动池、项目状态写回的基础流转。
- 在自己的真实项目里逐步调整和扩展。

## 第一天怎么开始

如果你是第一次使用，不需要先读完所有技术文档。

先看：

- `docs/user-first-day-guide.md`

你只需要准备一个 AI 客户端、一个空工作区和至少 2 个真实项目，然后从这句话开始：

```text
请开始帮我建立个人 AI 工作系统，工作区放在 D:/MondoWorkOS。
```

第一天的目标不是学会 Mondo 的文件结构，而是把你的长期方向和当前项目说出来，让 AI 帮你生成一个以后能继续接手的工作现场。

## 联系与合作

如果你想把自己的真实业务场景接入 AI，可以先通过 GitHub Issues 描述你的场景：

- 你现在用 AI 卡在哪一步？
- 你希望 AI 接手哪一类工作？
- 你的项目、Daily、行动池或文档现在是怎么组织的？
- 你希望系统最终帮你节省什么时间或提升什么交付？

我会优先回复和真实业务场景、AI 赋能陪跑、Agent 工作系统相关的问题。

推荐使用仓库内置的 Issue 模板：

- `真实工作场景接入`：描述你希望 AI 接住的工作现场。
- `第一位内测执行任务`：跟踪第一位真实用户初始化建模内测。
- `第一轮内测反馈`：记录初始化建模内测结果。

准备跑第一位用户时，可以直接创建：

- [第一位内测执行任务](https://github.com/alsacer123/mondo-agent-os/issues/new?template=first-beta-run.md)

如果 GitHub Issue 创建、浏览器授权或网络权限暂时卡住，先生成本地第一位内测执行包：

```bash
python scripts/prepare_first_beta_pack.py
```

然后用 `.mondo/first-beta-run-pack.md` 按一次完整现场内测执行。第一位用户内测不应该被 Issue 提交动作阻断，Issue 可以内测后再补建。
安装后也可以运行：

```bash
mondo-os beta-pack
```

筛选第一位候选用户时，可以先生成触达清单，再生成一份可填写的准入记录：

```bash
mondo-os beta-outreach
```

```bash
mondo-os beta-intake
```

Issue 和任务描述口径见：

- `docs/github-task-guide.md`

选择第一位内测用户前，先看：

- `docs/beta-candidate-outreach.md`
- `docs/beta-user-selection.md`
- `docs/beta-user-intake-template.md`

也可以通过以下方式联系：

- Email: 17610006129a@gmail.com
- WeChat: mondoagentos

## 推荐目录结构

```text
your-vault/
  _索引.md
  00_Inbox/
  20_Insights/
  30_Projects/
    示例项目/
      _项目规则.md
      _总览.md
      _当前状态.md
      _next.md
      决策日志.md
  40_Daily/
    _行动池.md
    days/
      YYYY/
        YYYY-MM-DD.md
```

## 快速开始

### 方式一：使用 CLI 初始化

```bash
pip install -e .
mondo-os init --root ./my-work-os --project 第一个AI赋能项目
mondo-os doctor --root ./my-work-os
mondo-os scan --root ./my-work-os
mondo-os route "今天把客户项目的下一步写回"
mondo-os packs
mondo-os live --root ./my-work-os
mondo-os context --root ./my-work-os
```

### 方式二：接入 Cherry Studio

普通用户推荐使用 Cherry Studio 作为图形界面，Mondo 作为 MCP 工具接入。

```bash
python scripts/mondo_mcp.py
```

或安装后：

```bash
mondo-mcp
```

配置说明见：

- `docs/cherry-studio-mcp.md`

### 方式三：手动复制模板

1. 复制 `templates/` 里的文件到你的 Obsidian vault 或普通文件夹。
2. 先写 `_索引.md`，告诉 AI 你的全局规则和读取入口。
3. 给每个项目复制一套项目文件。
4. 每次让 AI 进入项目时，先让它读取 `_项目规则.md` 和 `_next.md`。
5. 完成动作后，让 AI 把结果写回 `_next.md`、`_当前状态.md` 或 `决策日志.md`。

## Runtime 能力

```bash
mondo-os init --root <path> --project <name>
```

初始化一个最小工作系统，包括全局索引、AGENTS.md、Daily、行动池、Insights、Inbox 和第一个项目的五个运行文件。

```bash
mondo-os doctor --root <path>
```

检查工作区是否具备可运行结构：根入口是否缺失、项目运行文件是否缺失、Markdown/JSON/YAML 中是否出现疑似 secret。

```bash
mondo-os scan --root <path>
```

输出工作区结构图，供 Agent 或外部自动化读取。

```bash
mondo-os route "一段口述输入"
```

把一句 loose input 初步路由到 Daily、行动池、项目、Insights 或 Inbox。它不是最终判断，只是中控 Agent 的第一层分流器。

```bash
mondo-os packs
```

列出可用角色包。角色包不是固定模板，而是一组工作类型、建议文件和 Agent 运行协议。

```bash
mondo-os live --root <path>
```

生成 `.mondo/live-state.json`。Daily、行动池、项目下一步和项目状态会汇总成一个实时状态文件，方便普通 Agent、轻量 Dashboard 或外部自动化读取。

```bash
mondo-os live --root <path> --watch --interval 30
```

持续刷新实时状态。用户不需要等到晚上复盘才看到系统变化，今天的任务、行动池和项目下一步一改，状态层就能跟着更新。

```bash
mondo-os context --root <path>
```

生成 `.mondo/agent-context.md`。这是给普通对话 Agent 看的简化入口：它不用理解完整技术架构，也能知道先读什么、今天发生了什么、哪些项目有下一步。

## 这个模板不做什么

- 不保存密钥、token、密码、私钥、服务器 IP。
- 不把视频、图片、PDF、依赖、缓存、大文件塞进 vault。
- 不鼓励一次整理完整个知识库。
- 不把 AI 当全自动员工，而是把它当能读项目现场的协作者。

## 方法论

详见：

- `docs/customer-outcome.md`
- `docs/user-first-day-guide.md`
- `docs/execution-roadmap.md`
- `docs/github-task-guide.md`
- `docs/first-beta-start-here.md`
- `docs/beta-candidate-outreach.md`
- `docs/beta-user-selection.md`
- `docs/beta-user-intake-template.md`
- `docs/beta-config-preflight.md`
- `docs/beta-session-notes-template.md`
- `docs/beta-test-checklist.md`
- `docs/beta-feedback-form.md`
- `docs/beta-retro-guide.md`
- `docs/beta-invitation-message.md`
- `docs/beta-host-runbook.md`
- `docs/methodology.md`
- `docs/personal-ai-enablement.md`
- `docs/security.md`
- `docs/setup-guide.md`
- `docs/technical-architecture.md`

## Agent Skill

如果你希望 Agent 自动初始化这套系统，可以使用 `skill/` 目录：

- `skill/SKILL.md`
- `skill/references/operating-flow.md`
- `skill/scripts/init_work_os.py`

脚本示例：

```bash
python skill/scripts/init_work_os.py --root ./my-work-os --project 第一个AI赋能项目
```

## 开发验证

内测前推荐先跑完整自检：

```bash
python scripts/verify_all.py
```

它会依次运行文档引用、runtime、MCP、beta flow 和第一位内测执行包验证。

如果要在第一位用户加入前生成本地执行包，运行：

```bash
python scripts/prepare_first_beta_pack.py
```

它会生成 `.mondo/first-beta-run-pack.md`，包含 Issue 模板、邀请话术、用户第一天说明、配置自检、主持人 runbook、现场记录、反馈和复盘入口。
安装后同样可以运行：

```bash
mondo-os beta-pack
```

生成候选用户触达清单和准入记录：

```bash
mondo-os beta-outreach
```

```bash
mondo-os beta-intake
```

```bash
python scripts/verify_runtime.py
```

验证内容包括：初始化工作区、结构诊断、扫描输出、输入路由、角色包读取、实时状态生成和普通 Agent 上下文导出。

```bash
python scripts/verify_mcp.py
```

验证 MCP stdio server 能初始化、列出工具、导出上下文并追加 Markdown。

```bash
python scripts/verify_beta_flow.py
```

按第一轮内测 checklist 跑一段模拟用户口述，验证 onboarding 能生成长期方向、行动池、当天 Daily、初始化项目五件套和 Agent context。

```bash
python scripts/verify_docs.py
```

检查 README、docs 和 GitHub Issue 模板里引用的本地文档、脚本和模板路径是否存在，避免内测入口断链。
