# Architecture, entry points and deployment

> **Relocated original AGENTS.md (2026-11-07).** Source is the `saymer-alt/sub-filter` fork at `79fc48ba7813c4dbdfb71cc095e389cf71fb5d3b`; sections below are copied intact except rebased relative Markdown hyperlinks. Paths in code spans are still relative to the repository root. Historical or dated claims require checking the actual current code and tests.
>
> This is a **read-on-demand** guide, not mandatory startup content. [Root AGENTS.md](../../AGENTS.md) is the always-on contract. The former lengthy Copilot references have been archived as optional background material.

---

## Purpose

`sub-filter` is a Go CLI/service application that fetches proxy subscription sources, validates and normalizes proxy links, filters bad words, applies optional country filtering, deduplicates and merges subscriptions, and exposes results via HTTP endpoints or CLI output.

Supported protocols:

- `vless://`
- `vmess://`
- `trojan://`
- `ss://`
- `hysteria2://`
- `hy2://`

Primary behaviors:

- fetch remote or local subscription sources
- validate proxy links per protocol and policy rules
- strip/replace/delete bad-word matches
- filter entries by country markers in URL fragments
- merge multiple source IDs with deduplication
- support HTTP endpoints and CLI mode

## Entry Points

- `main.go`: parses flags, loads config, creates `service.Service`, starts HTTP server or processes CLI.
- `pkg/service/service.go`: main app logic, HTTP handlers, request protections, filtering, merge, caching, and country parsing.
- `pkg/config/config.go`: config schema, nested YAML plus legacy flat key support, runtime loading of sources/rules/bad words/countries/UA allowlist.

## Important Packages

- `pkg/service`: HTTP handlers, request validation, filtering, merge, CLI processing.
- `pkg/config`: config loading, validation, file path resolution.
- `pkg/cache`: compiled-regex cache (`RegexCache`) with hit/miss stats; used by bad-word filtering.
- `internal/validator`: generic rule engine and validation policies.
- `internal/utils`: URL normalization, host/port validation, country lookup, dedupe helpers.
- `vless`, `vmess`, `trojan`, `ss`, `hysteria2`: protocol-specific parsing/normalization.
- `pkg/errors`: typed application errors.
- `pkg/logger`: structured logging wrapper.

## Runtime Flow

1. `main.go` loads config via `config.Load` and creates `Service`.
2. `pkg/config` loads configured source map, rules, bad-word rules, countries, and optionally allowed user agents.
3. `Service` builds protocol processors and registers HTTP handlers.
4. `/filter` and `/merge` validate requests, rate-limit by IP, check User-Agent, parse country codes, and process sources.
5. Protocol packages match and normalize proxy lines, then service filters and deduplicates the output.
6. Response content is served with safe headers and optional line limiting.

## CLI Surface

Flags live in `main.go`.

- `--cli`
- `--stdout`
- `--config`
- `--country`
- `--debug`

CLI accepts source IDs as positional args or processes all configured sources if none are passed. In server mode, a single positional arg is treated as the port.

## Deployment

- `Dockerfile`: multi-stage build to a `scratch` image, binary at `/app/filter`, defaults `SUBFILTER_CONFIG=/config/config.yaml`. `docker-compose.yml` wraps it.
- `subfilter.container` is a Podman quadlet example for rootless systemd deployment; published image is `ghcr.io/viktor45/sub-filter`.
- CI lives in `.github/workflows/`: `test.yaml` (tests + vet + build on push/PR), `container.yaml` (image build/push), `release.yaml`, `ghcr-cleaner.yaml`.

## Files worth reading first

- `main.go`
- `pkg/service/service.go`
- `pkg/config/config.go`
- `internal/validator/generic.go`
- `internal/utils/utils.go`
- `config/rules.yaml`
- `config/badwords.yaml`
- `docs/README.md`
- `docs/FILTER_RULES.md`
- `docs/BADWORDS.md`
- `docs/FORMAT_PARAMETER.md`


