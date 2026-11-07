#!/usr/bin/env python3
"""Doc-only startup and scoped Copilot instructions audit (no network)."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
GUIDES=["docs/agent-guidance/01-project-policy-and-development.md","docs/agent-guidance/02-architecture-and-entrypoints.md","docs/agent-guidance/03-http-validation-and-data-contracts.md"]
HEADINGS=["## Owner-wide design gate — SIMPLICITY-FIRST (2026-10-24)","## Purpose","## Entry Points","## Important Packages","## Runtime Flow","## HTTP Surface","## CLI Surface","## Config Reality","## Deployment","## Country Filtering","## Dedupe and Merge","## Change guidance","## Tests","## Go Development Standards","## Files worth reading first","## Technical debt"]
ARCHIVES=[{"path":"docs/agent-guidance/reference/actions-original.md","bytes":51969},{"path":"docs/agent-guidance/reference/docker-original.md","bytes":35625},{"path":"docs/agent-guidance/reference/go-original.md","bytes":16274},{"path":"docs/agent-guidance/reference/markdown-original.md","bytes":3300}]
COPILOT=[".github/instructions/actions.instructions.md",".github/instructions/docker.instructions.md",".github/instructions/go.instructions.md",".github/instructions/md.instructions.md"]
REQUIRED=["Viktor45/sub-filter","Draft PR","owner GO","SSRF","IsIPAllowed","User-Agent","rate limiting","NormalizeLinkKey","yamlQuote","go test ./...","go vet ./..."]

def main():
    root=(ROOT/"AGENTS.md").read_text(encoding="utf-8")
    size=len(root.encode("utf-8"))
    assert size <= 10240, f"AGENTS.md is {size} bytes (limit 10240)"
    for item in REQUIRED:
        assert item.casefold() in root.casefold(), f"missing startup constraint: {item}"
    archive_text=""
    for guide in GUIDES:
        assert f"]({guide})" in root, f"missing guide link {guide}"
        archive_text+=(ROOT/guide).read_text(encoding="utf-8")+"\n"
    for head in HEADINGS:
        assert head in archive_text, f"missing source heading {head}"
    for entry in ARCHIVES:
        doc=(ROOT/entry["path"]).read_text(encoding="utf-8")
        assert "<!-- ORIGINAL SOURCE BEGIN -->\n" in doc
        raw=doc.split("<!-- ORIGINAL SOURCE BEGIN -->\n",1)[1].split("<!-- ORIGINAL SOURCE END -->",1)[0]
        assert len(raw.encode("utf-8"))==entry["bytes"], f"lossy archive {entry['path']}"
    for path in COPILOT:
        doc=(ROOT/path).read_text(encoding="utf-8")
        assert len(doc.encode("utf-8")) <= 3500, f"oversized scoped rule {path}"
        assert doc.startswith("---\n") and "applyTo:" in doc.split("---",2)[1]
    for path in ["AGENTS.md",*GUIDES,*COPILOT]:
        doc=(ROOT/path).read_text(encoding="utf-8")
        for href in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)",doc):
            target=href.split("#",1)[0]
            if not target or re.match(r"^(https?:|mailto:|/)",target,re.I): continue
            assert ((ROOT/path).parent/target).exists(), f"broken link {path} -> {href}"
    print(f"Agent context PASS: {size} root bytes, {len(GUIDES)} guides, {len(ARCHIVES)} preserved archives, {len(COPILOT)} scoped rules")

if __name__=="__main__":
    main()
