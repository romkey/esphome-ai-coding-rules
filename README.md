# esphome-ai-coding-rules

[![CI](https://github.com/romkey/esphome-ai-coding-rules/actions/workflows/ci.yaml/badge.svg)](https://github.com/romkey/esphome-ai-coding-rules/actions/workflows/ci.yaml)
[![Lint](https://github.com/romkey/esphome-ai-coding-rules/actions/workflows/lint.yaml/badge.svg)](https://github.com/romkey/esphome-ai-coding-rules/actions/workflows/lint.yaml)
[![Release](https://img.shields.io/github/v/release/romkey/esphome-ai-coding-rules?color=blue)](https://github.com/romkey/esphome-ai-coding-rules/releases)
[![ESPHome](https://img.shields.io/badge/ESPHome-AI%20coding%20rules-18BCF2?logo=esphome&logoColor=white)](https://esphome.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Rules for AI assistants writing my ESPHome projects, a complete template
project they start from, and a Claude Code plugin that scaffolds, audits and
releases projects that follow them.

> **AI disclosure:** This project was written by AI under human oversight,
> following [these rules](https://github.com/romkey/esphome-ai-coding-rules/blob/main/RULES.md).

## What's here

| Path | What it is |
|------|------------|
| [RULES.md](RULES.md) | The rules. Point an AI at this file. |
| [templates/](templates/) | A buildable example project: packages, ESP32/C3/S3 examples, Docker, CI, release workflow, pre-commit, Renovate, docs skeletons |
| [templates/optional/firmware-publishing/](templates/optional/firmware-publishing/) | Add-on for apps: firmware on every release plus a browser installer |
| [skills/](skills/), [.claude-plugin/](.claude-plugin/) | The `esphome-rules` Claude Code plugin |
| [SECURITY.md](SECURITY.md) | How to report a vulnerability |
| [docs/](docs/) | [Release strategy](docs/releasing.md), [Claude Code usage](docs/claude-code.md), [configuration guide](docs/configuration.md), [overview](docs/overview.md) |

## What the rules cover

- **How the AI works:** no invented pins or addresses, ask before choosing
  hardware, validate before claiming success, say what wasn't tested,
  look up current versions instead of trusting training data.
- **Structure:** board-agnostic `packages/`, UI in its own packages,
  `examples/` for ESP32, ESP32-C3 and ESP32-S3 holding all board and pin
  choices, optional custom `components/`.
- **ESPHome and Home Assistant conventions:** substitutions for every name
  and id, encrypted API/OTA, fallback hotspot and safe mode, proper
  `device_class`/`state_class`, esphome-lib diagnostics.
- **Tooling:** Docker Compose for everything, pre-commit for lint and
  formatting, GitHub Actions with aggressive caching (uv, ccache,
  toolchains, incremental builds), a weekly ESPHome beta build, Renovate.
- **Releases:** semver, changelog-driven release notes, optional firmware
  publishing with a web installer.
- **Docs:** README layout, badges, AI disclosure, CHANGELOG, configuration
  guide, a short overview for AIs.

## Using it

**With Claude Code**, install the plugin
([details](docs/claude-code.md)):

```
/plugin marketplace add romkey/esphome-ai-coding-rules
/plugin install esphome-rules@romkey
```

Then `/esphome-rules:new` starts a project, `/esphome-rules:check` audits
one, and `/esphome-rules:release` cuts a release.

**With any AI assistant**, tell it: "Follow
https://github.com/romkey/esphome-ai-coding-rules/blob/main/RULES.md", or
copy [templates/AGENTS.md](templates/AGENTS.md) into the project.

**By hand**, copy `templates/` and follow the
[configuration guide](docs/configuration.md).

## Developing this repo

The templates are tested like a real project; this repo's CI builds every
template config on ESP32, ESP32-C3 and ESP32-S3.

```bash
docker compose run --rm lint
cp templates/examples/secrets.yaml.example templates/examples/secrets.yaml
docker compose -f templates/compose.yaml run --rm build
claude plugin validate .
```

`main` is protected: changes go through pull requests, which merge once
**CI passed** and **Lint** pass. `.github/workflows/ci.yaml` is generated
from the template's: edit
`templates/.github/workflows/ci.yaml` and run `scripts/sync-ci.py`.

## License

[MIT](LICENSE)
