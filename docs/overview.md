# esphome-ai-coding-rules overview

**What:** rules + templates for AI assistants writing romkey's ESPHome
projects, and a Claude Code plugin that applies them.

## Files

- `RULES.md`: the rules. The one file an AI must read.
- `templates/`: a complete, buildable example project (packages, ESP32/C3/S3
  examples, compose.yaml, workflows, pre-commit, Renovate, docs skeletons).
  New projects copy it.
- `templates/optional/firmware-publishing/`: add-on for apps that publish
  installable firmware and a web installer.
- `skills/`: Claude Code plugin skills `new`, `check`, `release`, `rules`.
- `.claude-plugin/`: plugin + marketplace manifests.
- `docs/releasing.md`: release strategy. `docs/claude-code.md`: plugin use.
  `docs/configuration.md`: what each template file is and what to change.
- `scripts/sync-ci.py`: generates `.github/workflows/ci.yaml` from the
  template's, so this repo's CI builds `templates/`.

## Conventions

- This repo follows RULES.md where it applies (it is a library of rules, not
  firmware): README order and badges, CHANGELOG, pre-commit, Renovate,
  release workflow, MIT.
- Changing a template means testing it: `docker compose -f
  templates/compose.yaml run --rm build` and `docker compose run --rm lint`.
- Plugin version in `.claude-plugin/plugin.json` equals the release tag.
