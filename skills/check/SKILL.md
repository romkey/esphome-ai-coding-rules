---
name: check
description: Audit the current ESPHome project against romkey's ESPHome AI coding rules and report or fix what doesn't comply.
argument-hint: "[fix]"
disable-model-invocation: true
---

Audit this repository against esphome-ai-coding-rules. Arguments:
`$ARGUMENTS` (`fix` to apply fixes; otherwise only report).

1. Read `${CLAUDE_PLUGIN_ROOT}/RULES.md` in full, and compare against the
   files in `${CLAUDE_PLUGIN_ROOT}/templates/`.
2. Check each section of RULES.md against this repo: layout, YAML
   conventions, examples (ESP32 + C3 + S3, base.yaml contents), Home
   Assistant conventions, components, compose.yaml, .gitignore, pre-commit,
   workflows (including stale action versions: look them up), Renovate,
   release setup, README order/badges/AI disclosure, CHANGELOG, docs/,
   AGENTS.md, LICENSE.
3. If the tools are available, run `docker compose run --rm validate` and
   `docker compose run --rm lint`.
4. Report findings grouped by RULES.md section, most important first, each
   with the file and a one-line fix. Note anything that is deliberately
   different (e.g. a library without firmware/) as fine, not a finding.
5. With `fix`: apply the fixes, re-run validate and lint, update
   CHANGELOG.md under Unreleased, and summarize. Ask before anything
   destructive, such as deleting or renaming files that users may reference
   (packages, substitutions, entity names are breaking changes).
