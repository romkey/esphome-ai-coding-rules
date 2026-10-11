# Configuration guide

What each file in [`templates/`](../templates/) is for and what to change
when starting a project. `/esphome-rules:new` does all of this for you.

## Placeholders

| Placeholder | Replace with | Where |
|-------------|--------------|-------|
| `REPO` | GitHub repo name | README, docs, `romkey.REPO`, firmware/ |
| `PROJECT` | Human-readable title | README, docs/overview.md |
| `example-device` | Lowercase device name | firmware/*.yaml |
| year in `LICENSE` | Current year | LICENSE |

## Files

| File | Purpose | Change |
|------|---------|--------|
| `packages/example.yaml` | Example sensor package showing package conventions | Replace with real packages |
| `packages/status-led.yaml` | Example UI package with a required pin substitution | Keep, replace or delete |
| `examples/esp32*.yaml` | ESP32, ESP32-C3, ESP32-S3 configs: board + pins only | Boards and pins for the real hardware |
| `examples/common/base.yaml` | Shared: project version, esphome-lib packages, api/ota, Wi-Fi, recovery | `romkey.REPO`; add `i2c-scan` if there's I2C |
| `examples/secrets.yaml.example` | Valid dummy secrets for CI | Add any new `!secret` names |
| `compose.yaml` | `validate`, `build`, `lint`, `dashboard`, `esphome` | Nothing |
| `scripts/list-configs.sh` | Lists buildable configs for CI, release and compose | Nothing |
| `scripts/changelog-section.sh` | Prints a version's changelog notes; release check | Nothing |
| `scripts/bump-version.sh` | Next version from the latest tag; updates CHANGELOG and `project_version` | Nothing |
| `scripts/collect-firmware.sh` | Gathers firmware images + web installer manifest | Nothing |
| `.github/workflows/ci.yaml` | Builds every config; weekly beta build; unit tests | Nothing |
| `.github/workflows/lint.yaml` | Runs pre-commit | Nothing |
| `.github/workflows/release.yaml` | Run from the Actions tab (patch/minor/major) or on a tag; GitHub Release; firmware if `firmware/` exists | Nothing |
| `.pre-commit-config.yaml` | yamllint, actionlint, clang-format, ruff, hygiene | Nothing |
| `renovate.json` | Keeps actions, hooks, images and `github://` tags current | Nothing |
| `.yamllint.yaml` | yamllint rules relaxed for ESPHome | Nothing |
| `.clang-format` | ESPHome's C++ style | Nothing |
| `.gitignore` | Build output, secrets, `local*` configs | Nothing |
| `README.md`, `CHANGELOG.md`, `docs/`, `AGENTS.md` | Skeletons in the required order | Fill in |
| `optional/firmware-publishing/` | Firmware + web installer for apps | Copy `firmware/` and `web/` to the root if wanted, then delete `optional/` |

## One-time GitHub setup

- Install the [Renovate GitHub App](https://github.com/apps/renovate) on the
  repo. Without it `renovate.json` does nothing.
- Optional: set a repository variable `ESPHOME_VERSION` to pin CI to one
  ESPHome release.
- Apps publishing firmware: enable Pages with GitHub Actions as the source
  (see the kit's README).

## Local commands

```bash
cp examples/secrets.yaml.example examples/secrets.yaml
docker compose run --rm validate
docker compose run --rm build
docker compose run --rm lint
docker compose up dashboard
```

Or install the git hook so lint runs on every commit (needs
[uv](https://docs.astral.sh/uv/)): `uvx pre-commit install`.
