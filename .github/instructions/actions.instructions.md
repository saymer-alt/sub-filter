---
applyTo: '.github/workflows/*.yml,.github/workflows/*.yaml'
description: 'Scoped sub-filter fork GitHub Actions safety rules.'
---

# GitHub Actions — concise rules

This is a fork: only change `saymer-alt/sub-filter` workflows for authorized work. Preserve event triggers and Go version from `go.mod`. `test.yaml` runs tests, vet, build.
- Keep `permissions: contents: read` in test workflows, and least privilege on publishing jobs. Do not expose secrets or expand write permissions and `pull_request_target` without review.
- Protect existing tag/release and GHCR publishing conditions; verify fork-safe publication destinations before any change.
- No release, deploy or container push as a side effect of a docs/code PR. Prefer small CI diffs and check exact workflow results.
- Read legacy broad guidance only when necessary: [archived Actions guide](../../docs/agent-guidance/reference/actions-original.md).
