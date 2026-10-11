# Instructions for AI assistants

This repo holds the rules, templates and Claude Code plugin. It follows its
own [RULES.md](RULES.md) where it applies. Read [docs/overview.md](docs/overview.md)
first.

- Changing a template means testing it like a project:
  `docker compose -f templates/compose.yaml run --rm validate` (and `build`),
  plus `docker compose run --rm lint` here.
- Never edit `.github/workflows/ci.yaml` directly; edit
  `templates/.github/workflows/ci.yaml` and run `scripts/sync-ci.py`.
- After changing `skills/` or `.claude-plugin/`, run `claude plugin validate .`.
- A release bumps `version` in `.claude-plugin/plugin.json` to match the tag.
- Keep RULES.md succinct: it is read in full by every AI using it.
