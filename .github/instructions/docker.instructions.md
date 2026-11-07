---
applyTo: '**/Dockerfile,**/Dockerfile.*,**/*.dockerfile,**/docker-compose*.yml,**/docker-compose*.yaml,**/compose*.yml,**/compose*.yaml'
description: 'Scoped Docker and compose safety for sub-filter.'
---

# Docker — concise rules

This fork uses a multi-stage Go build and minimal `scratch` runtime image. `Dockerfile`, `docker-compose.yml` and `subfilter.container` are different deployment surfaces. Inspect real files.
- Preserve binary path, `SUBFILTER_CONFIG`, mounted config/data, ports, runtime UID/file permissions and Go module/toolchain compatibility.
- No credentials/subscription secrets in layers or logs. Minimize build image, keep reproducibility; don't create new orchestrators for a one-service repo.
- Do not change published image name, networks, privilege model, volumes or deploy without explicitly reviewed scope. No live restart/push on docs tasks.
- Optional background: [archived Docker guide](../../docs/agent-guidance/reference/docker-original.md).
