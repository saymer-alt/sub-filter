# AGENTS.md — sub-filter fork: small agent startup rules

**Read this, not every reference file.** This is `saymer-alt/sub-filter`, a fork of `Viktor45/sub-filter`. The original project is upstream and is **not in scope** for this task. Use a task branch and Draft PR targeting the fork's `main`; never change upstream, merge into `main`, sync upstream, publish GHCR images, release, or deploy without specific **owner GO**.

## What matters

`sub-filter` is a Go 1.26+ HTTP/CLI subscription filtering tool. `main.go` selects mode; `pkg/config` parses nested and legacy config; `pkg/service` handles HTTP/CLI, filtering, YAML formatting and merging; `internal/validator`, `internal/utils`, and protocol packages handle validation, URL normalization and dedupe. Protocols include VLESS, VMess, Trojan, SS and Hysteria2/Hy2.

Before modifying anything, check branch/HEAD SHA, existing code/tests and requested scope. Favor minimal reversible changes and actual user outcomes, not wholesale refactors. For complex work consult the [common task contract](https://github.com/saymer-alt/saymer-alt/blob/main/AGENT-TASK-CONTRACT.md); for major systems compare the existing/manual path, smallest safe change, and a justified architecture using [Proof Before Build](https://github.com/saymer-alt/saymer-alt/blob/main/PROOF-BEFORE-BUILD.md). Do not turn a small fix into a new platform.

## Non-negotiable correctness and security

- **SSRF protection:** preserve `config.IsIPAllowed`, URL/source validation, DNS re-resolution/pinned-IP rules, redirect/IP-family restrictions and private/forbidden destination blocking. `ip=4|6` must not weaken these guards.
- **HTTP abuse and input protections:** preserve User-Agent allowlist, per-IP rate limiting, source ID validation and bounded processing. Never log or commit subscription credentials, tokens, private URLs, customer data or untracked `tmp/` samples.
- **Output fidelity:** keep normalized proxy URI semantics, REALITY and transport parameters, Hysteria2 password interpretation, YAML quoting (`yamlQuote`), `format=` plain/YAML/base64 combinations and safe response headers. Unknown schemes must be skipped instead of invented as other proxy types.
- **Compatibility:** preserve nested and legacy flat YAML configuration, country filters, source ID aliases, dedupe via `NormalizeLinkKey`, merge winner selection and caching/singleflight segregation across `ip=4|6`. Changes require negative and positive regressions.
- Do not widen GitHub Actions permissions, alter external image/release destinations, Docker networking/volumes or CI security on a docs-only task. Never treat Go unit tests as production verification.

## Efficient execution

1. Read only relevant source and a **task-matched guide** below. For Go-only edits, the concise [Go instructions](.github/instructions/go.instructions.md) apply; Docker, Actions and Markdown instructions are scoped by `applyTo`. Generic reference archives are **not required reading**.
2. Preserve the smallest working change; document new observable behavior. Update relevant English `docs/`, Russian `docs/ru/` and Chinese `docs/zh/` material when user-facing docs change, not on unrelated tasks.
3. For code changes run `go test ./...`, `go vet ./...`, `go build .`; for concurrent code consider `go test -race ./...`. Require exact-head CI and targeted security regression evidence.
4. Check diff/commit SHA and report PASS / FAIL / BLOCKED / NOT TESTED. Propose Draft PR; never merge, publish or deploy automatically. Separate discovery of technical debt from authorization to fix it.

## Read only when needed

- [01 — owner policy, workflow and tests](docs/agent-guidance/01-project-policy-and-development.md) — task planning or process work.
- [02 — architecture, packages and deployment](docs/agent-guidance/02-architecture-and-entrypoints.md) — entry points, CLI, Docker or structural changes.
- [03 — HTTP/SSRF, filtering, YAML, caching and dedupe](docs/agent-guidance/03-http-validation-and-data-contracts.md) — remote sources, request handling or output generation.
- Archived generic examples: [Go](docs/agent-guidance/reference/go-original.md), [Docker](docs/agent-guidance/reference/docker-original.md), [Actions](docs/agent-guidance/reference/actions-original.md), [Markdown](docs/agent-guidance/reference/markdown-original.md). **Manual reference only**, never preload all.
