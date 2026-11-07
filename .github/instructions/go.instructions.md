---
description: 'Scoped idiomatic Go rules for sub-filter fork.'
applyTo: '**/*.go,**/go.mod,**/go.sum'
---

# Go — concise rules

Use the Go toolchain in `go.mod` (currently 1.26.0). Minimal changes, idiomatic error propagation, contexts/timeouts and concurrency-safe shared state; `gofmt` only touched files.
- Keep `pkg/config` nested/legacy compatibility, `pkg/service` security protections and protocol-specific URI normalization.
- Preserve `config.IsIPAllowed` SSRF checks, DNS/IP family semantics, User-Agent allowlist, rate limiting and safe output formatting.
- Preserve VLESS, VMess, SS, Trojan, Hysteria2 transport fields, `NormalizeLinkKey`, YAML conversion and cache/singleflight correctness. Avoid untrusted secret logging.
- Add behavior regressions; run `go test ./...`, `go vet ./...`, `go build .` and `go test -race ./...` for concurrency changes.
- Legacy generic reference (optional): [archived Go guide](../../docs/agent-guidance/reference/go-original.md).
