# Operating Flow Reference

## The System Is a Loop

This work OS has four loops:

1. Capture loop: inbox and action pool catch loose inputs.
2. Daily loop: today selects only executable actions.
3. Project loop: each project advances through one current next action.
4. Learning loop: repeated patterns become methods, templates, and SOPs.

## Capture Loop

Inputs can come from voice, chat, notes, meetings, or sudden ideas.

Routing:

- unclear ownership -> `00_Inbox/`
- cross-project action -> `40_Daily/_行动池.md`
- today action -> today Daily
- specific project action -> project `_next.md`
- reusable idea -> `20_Insights/`

## Daily Loop

Morning:

1. Read `40_Daily/_行动池.md`.
2. Read active project `_next.md` files only when needed.
3. Choose a small number of today-sized actions.
4. Write them into `40_Daily/days/YYYY/YYYY-MM-DD.md`.

During the day:

- Daily holds execution focus.
- Project context stays in projects.
- Do not copy full project context into Daily.

Evening:

- completed -> keep in Daily summary
- unfinished project item -> return to project `_next.md`
- future/cross-project -> return to `_行动池.md`
- decision -> project `决策日志.md`
- reusable method -> `20_Insights/`

## Project Loop

Project start:

1. Create `_项目规则.md`.
2. Create `_总览.md`.
3. Create `_当前状态.md`.
4. Create `_next.md`.
5. Create `决策日志.md`.

Project execution:

1. Read rules.
2. Read current next action.
3. Execute.
4. Archive old action.
5. Write new action.
6. Update state or decisions only if needed.

## Decision Rules

Use `_当前状态.md` for facts that are currently true.

Use `决策日志.md` for:

- positioning changes
- irreversible tradeoffs
- scope changes
- product/service strategy changes
- rules that future agents must respect

Use `_next.md` for:

- the current action
- completion archive
- short operational notes

## AI Enablement Flow

When using this system for AI enablement:

1. Diagnose the real work scene.
2. Split the workflow.
3. Decide what AI can handle.
4. Build context files.
5. Run a first project action.
6. Write back state.
7. Extract reusable method.

