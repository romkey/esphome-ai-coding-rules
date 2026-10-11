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
3. If this repo hasn't been set up with these rules before (no AGENTS.md
   pointing at them), ask the owner whether to use MIT or keep/choose
   another license before changing `LICENSE` (RULES.md §11). Check every
   file in `datasheets/` has its `-license.txt` and the README says the
   datasheets aren't covered by the repo's license.
4. If the tools are available, run `docker compose run --rm validate` and
   `docker compose run --rm lint`.
5. Report findings grouped by RULES.md section, most important first, each
   with the file and a one-line fix. Note anything that is deliberately
   different (e.g. a library without firmware/) as fine, not a finding.
6. With `fix`: apply the fixes, re-run validate and lint, update
   CHANGELOG.md under Unreleased, and summarize. Ask before anything
   destructive, such as deleting or renaming files that users may reference
   (packages, substitutions, entity names are breaking changes).
