---
description: 'Scoped Markdown rules matching existing sub-filter docs.'
applyTo: '**/*.md'
---

## Markdown — concise rules

- Respect existing headings and front matter **where present**. This repo uses H1 headings and does not mandate YAML front matter for every Markdown document; do not invent validator requirements.
- Keep links, examples and commands correct relative to live source and existing docs; avoid rewrites outside scope.
- When changing documented behavior, update the relevant English (`docs/`), Russian (`docs/ru/`) and Chinese (`docs/zh/`) documentation.
- Don't preload long background guides; reference them only for a concrete need. Original generic guide: [archived Markdown rules](../../docs/agent-guidance/reference/markdown-original.md).
