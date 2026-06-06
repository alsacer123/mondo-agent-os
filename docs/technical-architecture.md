# 技术架构

Mondo Agent OS 的目标不是替代 OpenHands、Dify、n8n、Khoj 或 Letta，而是在个人真实工作上方提供一个可运行的操作底座。

## 当前层次

```text
User input / voice / inbox
  -> Agent understands the work
  -> Agent reads Mondo OS rules and local files
  -> Agent writes Daily / Action Pool / Project / Insights according to the OS
  -> Work execution by Codex, Claude, OpenHands, n8n, browser-use, or other tools
  -> State, next action, decision, and reusable method write-back
```

## 四个核心部件

### 1. Markdown OS

负责长期状态和工作现场：

- `_索引.md`
- `AGENTS.md`
- `40_Daily/_行动池.md`
- `40_Daily/days/YYYY/YYYY-MM-DD.md`
- project `_项目规则.md`
- project `_总览.md`
- project `_当前状态.md`
- project `_next.md`
- project `决策日志.md`

### 2. Agent Entry

负责执行任务的是 Agent 本身，而不是 Mondo 的分流器。Codex、Claude Code、Cherry Studio、Cursor、Cline 或其他具备本地文件能力的 Agent 都可以读取同一套 Mondo OS。

Agent 负责：

- 理解用户的自然语言输入；
- 拆分真实项目；
- 判断写入层级；
- 读写本地 Markdown 文件；
- 在写入前向用户确认关键变更；
- 根据 OS 规则做早间整理、白天推进和晚间收口。

### 3. Runtime CLI

负责把工作区变成可检查、可初始化、可导出状态的系统：

- `init`: 生成最小工作区
- `doctor`: 诊断缺失文件和疑似 secret
- `scan`: 输出结构图
- `route`: 初步路由 loose input，仅作为轻量辅助，不替代 Agent 判断
- `packs`: 列出角色包
- `live`: 导出实时状态
- `context`: 导出简化 Agent 上下文

### 4. Optional MCP Helpers

MCP 是可选增强，不是主体流程。对于 Cherry Studio 这类具备本地文件读写能力的客户端，优先让 Assistant 直接读写 Mondo 工作区；Mondo MCP 主要用于：

- workspace diagnosis;
- workspace scanning;
- live state export;
- compact context export;
- role-pack listing.

### 5. Agent Skill

`skill/` 目录让支持 Skill 的 Agent 可以按 Mondo 的规则初始化或维护工作区。

### 6. Role Packs

角色包描述不同人的工作类型和建议文件。它不应该把用户锁死在固定模板里，而是给 Agent 一个可微调的起点。

当前内置：

- `content-personal-brand`: 内容生产型个人品牌
- `work-progress`: 工作推进型

## 后续技术补齐方向

- Memory/RAG: 接入 Obsidian 或本地 Markdown 的语义检索。
- Workflow: 接入 n8n/Dify 等确定性自动化工具。
- Browser/Desktop: 接入 browser-use 或 computer use sandbox。
- Evaluation: 建立真实任务评测集，检查归属判断、写回正确率、上下文恢复和安全边界。
- Update Channel: 为用户工作区提供可审计的规则更新包，而不是远程强制覆盖。
