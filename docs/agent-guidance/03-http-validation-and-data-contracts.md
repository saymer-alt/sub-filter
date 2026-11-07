# HTTP security, config and output contracts

> **Relocated original AGENTS.md (2026-11-07).** Source is the `saymer-alt/sub-filter` fork at `79fc48ba7813c4dbdfb71cc095e389cf71fb5d3b`; sections below are copied intact except rebased relative Markdown hyperlinks. Paths in code spans are still relative to the repository root. Historical or dated claims require checking the actual current code and tests.
>
> This is a **read-on-demand** guide, not mandatory startup content. [Root AGENTS.md](../../AGENTS.md) is the always-on contract. The former lengthy Copilot references have been archived as optional background material.

---

## HTTP Surface

- `/filter`
- `/merge`
- `/health`

Both `/filter` and `/merge` accept a `format=` query parameter (see `docs/FORMAT_PARAMETER.md`): plain text (default), `yaml` (Clash/Mihomo proxy list), `base64`, or combinations (e.g. `yaml+base64`; note `+` decodes to a space, and `formatContent` accepts both). Invalid values return `400 Bad Request`. Formatting happens in `formatContent`/`contentToYAML` in `pkg/service/service.go` after filtering/merge; `serveFile` adjusts filename extension and Content-Type accordingly.

`ip=4|6` forces outbound source fetches onto one stack: `fetchSourceContent` re-resolves the host and dials the first address of that family that passes `config.IsIPAllowed` (SSRF check must stay — it guards against DNS rebinding). Omitted → the IP pinned at source-load time is used, behavior unchanged. Stack-specific results get separate cache files (`_ip4`/`_ip6` suffix) and singleflight keys.

YAML conversion gotchas (⚠️ easy to break):

- Builders (`buildSSYAML`, `buildVLESSYAML`, `buildVMESSYAML`, `buildTrojanYAML`, `buildHysteria2YAML`) must parse the **normalized** link forms the protocol packages emit: SS userinfo is base64 (`utils.DecodeUserInfo`), VMess is `vmess://BASE64(JSON)` with the `#fragment` stripped via `vmessPayload()`.
- Canonical Xray transport param is `type` (`network` is a fallback); REALITY fields are `pbk`/`sid`/`fp`; hy2 password comes from userinfo or `obfs-password` (never from `obfs`); legacy `allowInsecure` maps to `skip-cert-verify`; speed limits are `upmbps`/`downmbps`.
- Unknown schemes are skipped, never converted to fake `http` proxies. All string values go through `yamlQuote` (escaping).
- `TestFormatYAML_RealFile_NoLostParams` in `pkg/service/format_yaml_file_test.go` guards against parameter loss using the real subscription sample `tmp/test.txt` (test skips if the file is absent).

Request protections (⚠️ **Security-Critical**):

- **User-Agent allowlist** — validates requests against built-in prefixes and optional file; do not weaken without security review
- **per-IP rate limiting** — prevents abuse; configurable but defaults are intentional
- **strict source ID validation** — enforces `^[a-zA-Z0-9_]+$`, max length 64

## Config Reality

The code prefers nested YAML sections `server`, `cache`, `sources`, `validation`, `logging`, but also accepts legacy flat keys for compatibility.

Important nested fields:

- `sources.file`
- `cache.directory`
- `cache.ttl`
- `cache.merge_buckets` (shard count for disk-based streaming merge; more shards = lower peak memory, more temp files)
- `validation.rules_file`
- `validation.bad_words_file`
- `validation.countries_file`
- `validation.ua_file`
- `validation.max_countries`
- `validation.max_merge_ids`

`config.Load` also honors `SUBFILTER_CONFIG`, `SUBFILTER_PORT`, and `LOG_LEVEL`.

Runtime artifacts, not source (do not commit changes from them):

- `cache/` — disk cache directory created/populated at runtime.
- `tmp/` — untracked local samples; `tmp/test.txt` feeds `TestFormatYAML_RealFile_NoLostParams` when present.

## Country Filtering

- `/filter` and `/merge` use `c=` and `parseCountryCodes`.
- Only two-letter uppercase codes are accepted and validated against loaded countries.
- CLI `--country` also applies country filtering.

## Dedupe and Merge

- dedupe key from `internal/utils.NormalizeLinkKey`
- winner selection via `CompareAndSelectBetter`
- `/merge` accepts repeated `ids`, comma-separated `ids`, and legacy `id`

