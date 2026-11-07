# Owner policy, development and tests

> **Relocated original AGENTS.md (2026-11-07).** Source is the `saymer-alt/sub-filter` fork at `79fc48ba7813c4dbdfb71cc095e389cf71fb5d3b`; sections below are copied intact except rebased relative Markdown hyperlinks. Paths in code spans are still relative to the repository root. Historical or dated claims require checking the actual current code and tests.
>
> This is a **read-on-demand** guide, not mandatory startup content. [Root AGENTS.md](../../AGENTS.md) is the always-on contract. The former lengthy Copilot references have been archived as optional background material.

---

> **Обязательный контракт для всех агентов и авторов ТЗ (30.10.2026):** [подробная постановка задач без «эффекта обезьяньей лапки»](https://github.com/saymer-alt/saymer-alt/blob/main/AGENT-TASK-CONTRACT.md). Перед работой проверить исходные refs/SHA, готовые результаты, точную цель, scope/non-goals, сохранность данных и сервисов, зависимости, границы разрешений/owner GO, негативную приёмку и доказательства. Не сокращать существенные требования ради токенов. Буквальное выполнение в ущерб цели считается **FAIL**. Местные правила безопасности и архитектуры обязательны.

> **Владелец, 26.10.2026 — общее правило для всех проектов:** перед внедрением новой функции / серьёзной переделки требуется короткая «защита идеи» — доказать проблему, сравнить альтернативы (включая ничего не менять / штатную ОС / ждать upstream), оценить пользу, **ТЭО**, стоимость сопровождения, риски, измеримый тест и критерии STOP. Нет доказательства пользы — DEFER/SKIP. Мелкие исправления не требуют отдельной бюрократии. **Источник:** [Proof Before Build](https://github.com/saymer-alt/saymer-alt/blob/main/PROOF-BEFORE-BUILD.md) ([центральный PR #9](https://github.com/saymer-alt/saymer-alt/pull/9)). Существующие safety/CI/permissions сохраняются.

# AGENTS.md

## Owner-wide design gate — SIMPLICITY-FIRST (2026-10-24)

Before a new service, subsystem, manager, web panel, installer/uninstaller, or heavy CI path, apply the [common engineering contract](https://github.com/saymer-alt/saymer-alt/pull/7). First compare: (A) existing/manual route, (B) smallest safe change, (C) ambitious design. Choose A/B unless C has evidence, cost/complexity budget, and explicit owner approval. If a helper grows into another platform or expensive E2E cycles repeat without new evidence, STOP adding layers and seek an architectural decision. Preserve all verified safety boundaries and working user behavior. [KAS uninstall retrospective #225](https://github.com/saymer-alt/keenetic-auto-setup/issues/225) is an **anti-pattern**, not a best-practice pattern. This documentation change does not authorize production or release modifications.

Repository guidance for coding agents working in `sub-filter`.

**Required:** Go 1.26.0 or higher
**Test Command:** `go test ./...`
**Build:** `go build -o sub-filter .`
**Run:** `./sub-filter` or with `--cli` flag for CLI mode

## Change guidance

- New protocol: implement `ProxyLink`, add tests, register in `createProxyProcessors()`, and add a YAML builder in `parseProxyToYAML` plus a case in `format_yaml_file_test.go`.
- Validation behavior: update `config/rules.yaml`, protocol tests, and relevant docs.
- Config schema changes: update `pkg/config/config.go`, docs, and examples together.
- Docs live in three languages: English (primary) in `docs/`, Russian in `docs/ru/`, Chinese in `docs/zh/`. Keep all three in sync when changing documented behavior; each file has a language switcher line at the top. `docs/DEVELOPMENT.md` (and its translations) covers typed errors and adding new protocols.
- Preserve rate limiter and User-Agent protections unless there is a security justification.

## Tests

- `go test ./...` — run all tests
- `go vet ./...` — CI runs vet plus `go build .` alongside tests; run both before committing
- `go test ./pkg/service ./pkg/config ./internal/validator` — test core packages
- `go test ./ss ./vless ./vmess ./trojan ./hysteria2` — test protocol implementations
- `go test -race ./...` — test for race conditions
- `go test ./pkg/service/ -bench=. -benchmem -run='^$'` — benchmarks for parsing, YAML conversion, base64, bad-word filtering (`bench_format_test.go`)
- `security_test.go` (repo root) — security-focused tests: header injection, SSRF source-URL/IP validation, regex pattern limits, rate-limiter concurrency, file permissions. Changes to request protections must keep these passing.

## Go Development Standards

Refer to [.github/instructions/go.instructions.md](../../.github/instructions/go.instructions.md) for idiomatic Go practices, naming conventions, and code review standards used in this project. Sibling files `docker.instructions.md`, `md.instructions.md`, and `actions.instructions.md` cover Dockerfiles, documentation, and GitHub Actions changes respectively.

Note: code comments and some docs (e.g. `config/config.yaml`) are written in Russian; keep that convention when editing those files.

## Technical debt

- Treat technical debt as an explicit engineering risk, but do not confuse it with cosmetics, personal style preferences, or merely "ugly" working code.
- For each debt item, provide evidence first and classify its impact: **High** (breakage/security/data-loss risk or blocks operation), **Medium** (impedes development, duplicates/diverges logic, or materially increases maintenance cost), **Low** (local complexity with little current risk).
- Do not refactor for cleanliness alone. Pay down debt when the benefit and risk reduction justify the change; do not rewrite stable, verified code without a concrete reason.
- Debt fixes must keep minimal scope, preserve existing safety boundaries, and pass the project's normal regression/safety checks. If the fix creates greater risk or new debt, stop and propose a safer alternative.
- If debt is discovered outside the current task, do not silently expand scope: record the finding and recommendation, and implement it only when it is in scope or explicitly approved by the operator.
