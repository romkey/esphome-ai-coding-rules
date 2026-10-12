# ESPHome Project Rules for AI Assistants

Rules for AI assistants writing ESPHome projects for romkey. Follow every rule
unless the human says otherwise. Templates live in [`templates/`](templates/);
copy them and fill them in rather than inventing new ones.

Canonical URL: https://github.com/romkey/esphome-ai-coding-rules/blob/main/RULES.md

## 0. How to work

- **Never invent hardware facts.** GPIOs, I2C addresses, register values,
  timings and config keys come from a datasheet or the ESPHome docs; cite
  the source in a comment. If you can't find it, ask.
- **Ask before choosing hardware** (board, sensor, pins) that the human
  hasn't specified. Strapping pins, flash pins and input-only pins are off
  limits unless the human says otherwise.
- **Prove it before claiming it.** Run `docker compose run --rm validate`
  (and `build` for C++ changes) before saying something works. Say plainly
  what you did not test, e.g. "compiles; not tried on hardware".
- **Never trust your memory for versions.** Look up current releases of
  actions, tools, ESPHome and esphome-lib (see §8).
- **When first applying these rules to a repo**, new or existing, ask the
  owner which license to use (§11) before adding or changing `LICENSE`.
- **Never expose secrets.** Don't put real secret values in code, docs,
  commit messages, PR text, issues or chat, and don't print `secrets.yaml`.
  Configs use `!secret`. If you find a real secret in the repo or its
  history, stop and tell the owner to rotate it; rewriting history doesn't
  make it secret again.
- Small, focused commits with messages that say why. `main` is protected:
  work on a branch and open a pull request; never push to `main`. Don't
  push, merge, tag or release without being asked.

## 1. Repository layout

```
packages/          reusable ESPHome packages: board-agnostic, no pins
components/<name>/ custom C++ external components (only if needed)
examples/          buildable device configs: board + pins live here
examples/common/   config shared by examples (not built on its own)
firmware/          optional, apps only: published, secret-free configs
tests/             optional: pytest unit tests for component logic
datasheets/        manufacturer datasheets, each with a -license.txt (§5)
docs/              configuration.md, overview.md
scripts/           list-configs.sh, changelog-section.sh, bump-version.sh,
                   collect-firmware.sh, check-datasheets.sh, check-secrets.py,
                   setup-github.sh
.github/           workflows/ci.yaml, lint.yaml, release.yaml
compose.yaml  renovate.json  .pre-commit-config.yaml  .yamllint.yaml
.gitleaks.toml  .gitignore  .clang-format  README.md  CHANGELOG.md  LICENSE  SECURITY.md
AGENTS.md
```

- `packages/` holds the interesting logic. A package never names a board,
  framework, or GPIO. It takes pins, bus ids and names as substitutions or
  references ids the example declares (e.g. `i2c0`).
- Put user interface (display, LVGL, web_server pages, LEDs, buttons) in its
  own package, separate from sensing/control logic, so it can be omitted.
- `examples/` show how to use the packages. Each is a full config that
  compiles in CI and holds all board and pin choices, with a unique
  `esphome: name:` (build trees are keyed by it) and a `comment:` saying
  what the device is.
- Board facts come from the board's documentation, linked in a comment:
  - `esp32: flash_size:` is the actual module's flash. If the board ships
    with several modules, say which one the value is for.
  - Logs and Improv serial must reach the USB port people plug into. On
    ESP32-C3/S3 (and newer) ESPHome logs to the chip's built-in USB by
    default; boards whose USB port goes through a USB-to-UART bridge need
    `logger: hardware_uart: UART0`.
- `components/<name>/` sits at the repo root so `external_components` with a
  `github://` source finds it without a `path:`.
- Repos are either **libraries** (packages/components for other projects)
  or **applications** (a device people flash). Only applications may add
  `firmware/` (§9).

## 2. YAML

- Name new files `.yaml`. Humans will add `.yml` files anyway, so everything
  must accept both: `.gitignore`, yamllint, `scripts/list-configs.sh`, CI
  cache keys, Renovate patterns. Never write a pattern that matches only one.
- Secrets live in `secrets.yaml`; ESPHome reads no other name.
- Every package starts with a comment block: what it does, what the including
  config must provide (ids, buses, required substitutions), and every
  substitution with its default.
- Every entity name, id, entity category, and interval in a package is a
  substitution prefixed with the package name (`co2_sensor_name`), with a
  sensible default. Ids must stay unique if a package is included twice.
- A package that needs a newer ESPHome sets `esphome: min_version:`.
- Default to `framework: type: esp-idf` unless a dependency needs Arduino.
- Examples include local packages with `!include ../packages/<name>.yaml`.
  Docs show the remote form pinned to a tag:
  `github://romkey/<repo>/packages/<name>.yaml@vX.Y.Z`.

## 3. Examples

- At least three, so CI proves packages are board-agnostic: ESP32
  (`esp32dev`), ESP32-C3 (RISC-V) and ESP32-S3. Add ESP8266 or others only if
  supported.
- Shared settings go in `examples/common/base.yaml`, included by each example:
  - `esphome: project:` with `name: romkey.<repo>` and
    `version: ${project_version}`; `project_version` matches the release tag.
  - `esphome: min_version:` set to the ESPHome release the configs were
    tested with.
  - From [esphome-lib](https://github.com/romkey/esphome-lib), pinned to its
    latest tag: `esp32`, `wifi-diagnostics`, `restart`, and `i2c-scan` if
    the project has I2C devices (bus `id: i2c0`).
  - `logger:`, `wifi:` from secrets, encrypted `api:`, and `ota:` with a bare
    `encryption:` that reuses the api key. No OTA `password:` (deprecated).
  - Recovery: `wifi: ap:` with `!secret fallback_ap_password`,
    `captive_portal:`, a `safe_mode` button and a `factory_reset` button
    (both `entity_category: config`). Drop these only on flash-constrained
    devices, and say so.
  - `web_server:` with `version: 3` (ESPHome defaults to 2), `ota: false`
    (its upload page is unencrypted; encrypted OTA covers updates), and
    `auth:` with `type: digest` and username/password from secrets.
  - `time: - platform: homeassistant` (add `sntp` if the device must keep
    time without Home Assistant).
- Never put real credentials in the repo.

## 4. Home Assistant conventions

- Entity names don't include the device name; HA prefixes `friendly_name`.
- Sensors set `device_class`, `state_class` and `unit_of_measurement` so HA
  long-term statistics work, and sensible `accuracy_decimals`.
- Noisy sensors get default filters (e.g. `sliding_window_moving_average`),
  overridable via substitutions.
- Diagnostics use `entity_category: diagnostic`; restart, safe mode and
  settings use `config`.
- Renaming an entity or id is a breaking change (HA history is lost).

## 5. Custom components (C++)

- Follow ESPHome's own conventions: `__init__.py`/`sensor.py` codegen,
  `setup()`/`loop()`/`update()`/`dump_config()`, `ESP_LOG*` with a `TAG`.
- Format with the repo's `.clang-format` (ESPHome's own) and ruff; the
  pre-commit hooks enforce both.
- Put pure logic (CRCs, conversions, parsing) where it can be tested, and
  test it with pytest in `tests/test_*.py` (deps in `tests/requirements.txt`).
  CI runs them.
- Every component option appears in at least one example so CI compiles it.

**Datasheets** live in `datasheets/`. Each has a license file named after
it without the extension plus `-license.txt` (`SCD4x.pdf` →
`SCD4x-license.txt`) saying the manufacturer owns it, it isn't covered by
the repo's license, and where to find the manufacturer's terms, with the
source URL and retrieval date. Use the template in
[`templates/datasheets/README.md`](templates/datasheets/README.md); never
invent the URL. If the terms forbid redistribution, link instead of
committing the PDF. The pre-commit hook `datasheet-licenses` fails when a
license file is missing.

## 6. Docker

Use [`templates/compose.yaml`](templates/compose.yaml) unchanged except for
image pins. It mounts the whole repo so `../packages/` includes resolve,
keeps toolchains and the compiler cache in a named volume at `/cache` and
build trees in one at `/build` (the ESPHome image's own convention), pulls
the floating `stable` tag daily, honors `ESPHOME_VERSION`, and provides
`esphome`, `validate`, `build`, `dashboard`, `lint` and `secrets` services. Configs are
found by `scripts/list-configs.sh`, so nothing needs editing when one is
added. Docker Desktop on macOS cannot pass USB through; document flashing
via OTA or https://web.esphome.io instead.

## 7. Git and pre-commit

- Use [`templates/.gitignore`](templates/.gitignore): ignores `.esphome/`,
  `secrets.y*ml` and `local*.y*ml` anywhere, OS and editor junk.
- Commit `examples/secrets.yaml.example` with valid dummy values (the api key
  must be base64 of 32 bytes); CI copies it.
- Personal device configs go in `examples/local-*.yaml` (ignored, and
  skipped by `list-configs.sh`).
- **Secrets never reach the repo.** The pre-commit hooks enforce it:
  - `esphome-secrets` (`scripts/check-secrets.py`) fails if a value from
    your local `secrets.yaml` appears in any committed file, if an ESPHome
    config sets `password`, `ssid`, `key` and similar to a literal instead
    of `!secret` or a substitution, or if a `firmware/` config uses
    `!secret`. It names the file, line and key, never the value.
    `# not-a-secret` on a line allows it.
  - `gitleaks` checks staged changes for tokens and keys; the Lint job and
    `docker compose run --rm secrets` scan the whole history.
    [`.gitleaks.toml`](templates/.gitleaks.toml) exempts only
    `secrets.yaml.example`; accept a false positive by adding its
    fingerprint to `.gitleaksignore`.
  - `no-firmware-images` rejects `.bin`/`.elf`/`.uf2`/`.hex`: a firmware
    image contains the Wi-Fi credentials it was built with. They're also
    gitignored, with `dist/` and `site/`.
- [`.pre-commit-config.yaml`](templates/.pre-commit-config.yaml) holds every
  lint and format check (yamllint, actionlint, shellcheck, clang-format,
  ruff, whitespace, large files, private keys, secrets, firmware images,
  datasheet licenses). The same hooks run via
  `docker compose run --rm lint`, as a git hook (`uvx pre-commit install`),
  and in CI.

## 8. GitHub workflows

Start from [`templates/.github/`](templates/.github/) and
[`templates/renovate.json`](templates/renovate.json).

**Versions.** Your training data is months old and the actions you remember
are probably deprecated. Before writing or editing any workflow, look up the
latest release of every action and tool you use, e.g.
`gh api repos/actions/checkout/releases/latest --jq .tag_name`. Use the
major tag (`@v7`) only if it exists
(`gh api repos/actions/checkout/git/ref/tags/v7`); some actions, like
`astral-sh/setup-uv`, publish only full versions (`@v10.3.0`). Do the same
for pinned tool versions (pre-commit hooks, pytest, the uv image,
esphome-lib tags). A Node.js deprecation warning
in a run log means an action is out of date: fix it. Afterwards
[Renovate](https://docs.renovatebot.com/) keeps everything current,
including `github://` package tags, which Dependabot can't update.
Versions on 2026-10-11, for sanity checking only: `actions/checkout@v7`,
`actions/cache@v6`, `actions/upload-artifact@v7`,
`actions/download-artifact@v8`, `astral-sh/setup-uv@v10.3.0`.

**Protected main.** Every change reaches `main` through a pull request,
squash-merged, and only when the required checks **CI passed** and
**Lint** pass on an up-to-date branch. `scripts/setup-github.sh` applies
this as a ruleset, plus secret scanning with push protection (and generic
patterns and validity checks where GitHub Secret Protection is available),
Dependabot alerts, private vulnerability
reporting, CodeQL default setup, read-only workflow tokens and branch
deletion on merge. Run it once when the GitHub
repo is created (re-running is safe). Keep the required checks reporting:

- Never use `paths`/`paths-ignore` on a workflow that provides a required
  check; a workflow that doesn't run blocks the PR forever. Skip expensive
  jobs inside it instead.
- Required check names must be stable, so matrix jobs feed one summary job
  (`CI passed`) instead of being required themselves.
- GitHub holds the workflow runs of a PR opened by `GITHUB_TOKEN` as
  `action_required`. The workflow that opened it must approve them
  (`POST /repos/{owner}/{repo}/actions/runs/{id}/approve`); runs started
  separately with `gh workflow run` do not satisfy the PR's required
  checks.

**lint.yaml**: runs pre-commit on all files and gitleaks over the whole
git history (job **Lint**).

**ci.yaml**: finds configs with `scripts/list-configs.sh`, then a matrix
job per config runs `esphome config` and `esphome compile`, skipped when a
change touches only docs. The weekly scheduled run (or a manual run with
**beta** ticked) also builds against ESPHome beta; beta failures are
warnings, not failures. Runs `tests/` with pytest if present. Ends with
**CI passed**.

**release.yaml**: run it from the Actions tab (**Run workflow**) with a
`bump` choice of `patch` (default), `minor` or `major`: minor resets patch
to 0, major resets minor and patch. It checks CI passed, runs
`scripts/bump-version.sh` on a `release/vX.Y.Z` branch, opens a
"Release vX.Y.Z" PR and approves its CI and Lint runs. Merging that PR tags the merge commit and creates the
GitHub Release (§9). Pushing a `vX.Y.Z` tag by hand also works.

**Speed. Cache everything that can be cached:**

- Install tools with `uv` (`astral-sh/setup-uv` with `enable-cache: true`),
  not pip. Run ESPHome natively in CI, not in Docker: faster to install,
  and cache dirs aren't root-owned.
- Install `ccache`; ESPHome uses it automatically. Cache `CCACHE_DIR`.
- Cache toolchains (`~/.platformio`, `~/.cache/esphome`) keyed on config +
  ESPHome version, and build trees (`ESPHOME_BUILD_PATH`) + ccache keyed on
  config + version + source hash, with `restore-keys` falling back to the
  newest older cache so builds are incremental. Cache pre-commit hook envs.
- `concurrency` with `cancel-in-progress: true`; `fail-fast: false`.
- `paths-ignore` docs-only changes in CI (lint still runs).
- `timeout-minutes` on every job; retry flaky `compile` up to 3 times.
- Least-privilege `permissions`: `contents: read` unless a job needs more.

## 9. Releases

Full explanation: [docs/releasing.md](docs/releasing.md).

- [Semantic versioning](https://semver.org/), tags `vX.Y.Z`. Breaking
  (major): removing or renaming a package, substitution, id, entity name or
  required bus id; raising `min_version`. Minor: new packages, options,
  boards. Patch: fixes. Before 1.0.0, breaking changes bump the minor.
- `main` is always releasable. To release, run the Release workflow from
  the Actions tab, pick the bump, then merge the release PR it opens.
  `scripts/bump-version.sh <patch|minor|major>` makes the edits (moves
  `## [Unreleased]` entries under `## [X.Y.Z] - YYYY-MM-DD`, sets every
  `project_version`); a human can run it on a branch and open the PR
  themselves.
- `release.yaml` refuses to publish if the changelog section is missing or a
  `project_version` doesn't match, then creates the GitHub Release with that
  changelog section as notes.
- **Applications may also publish firmware**: copy
  [`templates/optional/firmware-publishing/`](templates/optional/firmware-publishing/).
  Then each release attaches `.factory.bin`/`.ota.bin` images and deploys a
  browser installer (ESP Web Tools) to GitHub Pages. Firmware configs live
  in `firmware/` and contain no secrets; never publish images built from
  examples. They must work on anyone's Wi-Fi without rebuilding:
  - Wi-Fi set up after flashing through Improv over USB (`improv_serial:`,
    used by the web installer), Improv over Bluetooth (`esp32_improv:`,
    `improv_ble:` from ESPHome 2026.10; skip on chips without Bluetooth),
    and the fallback hotspot (`wifi: ap:` + `captive_portal:`);
  - API key provisioned when Home Assistant adopts it (`api: encryption:`
    with no key, `dashboard_import:`);
  - a setup window (`provisioning: timeout: 30min`) that closes those paths
    if the device isn't set up within 30 minutes of power-on;
  - updates from releases: `update: - platform: http_request` reading the
    manifest the release workflow publishes to Pages (it includes the OTA
    image and its md5), with `ota: - platform: http_request`;
  - `logger: level: INFO`, a `factory_reset` button, and no `web_server:`
    (it can't ship a password).
  ESPHome doesn't support ESP RainMaker; Improv is its equivalent. Don't
  use RainMaker.

## 10. Documentation

**README.md**, in this order:

1. Title and badges (below)
2. One-paragraph introduction
3. AI disclosure (verbatim, below)
4. Project breakdown: what each package/component/example does
5. Technical details: hardware, wiring table, I2C addresses, datasheet links
6. Build and use: Docker commands, using packages remotely, flashing
   (and the web installer link, if firmware is published)
7. License: the repo's license, and, if `datasheets/` exists, that the
   datasheets belong to their manufacturers and aren't covered by it

Badges, in this order, exactly this style. Only CI/Lint status may show red,
and only because a build failed:

```markdown
[![CI](https://github.com/romkey/REPO/actions/workflows/ci.yaml/badge.svg)](https://github.com/romkey/REPO/actions/workflows/ci.yaml)
[![Lint](https://github.com/romkey/REPO/actions/workflows/lint.yaml/badge.svg)](https://github.com/romkey/REPO/actions/workflows/lint.yaml)
[![ESPHome](https://img.shields.io/badge/ESPHome-packages-18BCF2?logo=esphome&logoColor=white)](https://esphome.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
```

For another license, use its SPDX id in the license badge
(`License-Apache--2.0-yellow`; shields.io needs `--` for a literal `-`).

Use `ESPHome-external%20component` instead of `ESPHome-packages` for a
component repo. Add a release badge once tagged:
`https://img.shields.io/github/v/release/romkey/REPO?color=blue`. Any other
badge uses `blue` (info) or `lightgrey` (neutral).

AI disclosure:

```markdown
> **AI disclosure:** This project was written by AI under human oversight,
> following [these rules](https://github.com/romkey/esphome-ai-coding-rules/blob/main/RULES.md).
```

**CHANGELOG.md**: [Keep a Changelog](https://keepachangelog.com/) format,
newest first, `## [Unreleased]` at the top. Update it with every change.

**docs/configuration.md**: for each package/component: purpose, required ids
and buses, every substitution or option with default and meaning, and a
minimal working snippet.

**docs/overview.md**: under ~60 lines, for AIs and humans. What the project
is, the file map, each package in one line, required ids, conventions. No
prose padding.

**AGENTS.md** (copy to CLAUDE.md or symlink): one line telling AI tools to
follow these rules, plus anything project-specific.

## 11. License

- Default: MIT, in `LICENSE`, `Copyright (c) <year> John Romkey`.
- The first time these rules are applied to a repo, ask the owner: "MIT,
  or a different license?" If different, use that license's official text
  (`gh api licenses/<spdx-id-lowercase> --jq .body`, filling in its year
  and name placeholders) and never copy the MIT `LICENSE`. Match the
  README badge and License section to it.
- Never change an existing repo's license without the owner's explicit
  confirmation; if it already has one, ask whether to keep it.
- The license covers the repo's own work, not `datasheets/` (§5).

## 12. Keeping repos current

These rules change. When you re-scan a repo that already follows them,
read [UPGRADING.md](UPGRADING.md) and apply every entry newer than the
version in the repo's `AGENTS.md` ("Follows esphome-ai-coding-rules
vX.Y.Z"), then update that line. When you change these rules in a way
existing repos must follow, add an entry to UPGRADING.md in the same PR.

## 13. Before finishing

- `docker compose run --rm validate` passes for every config (and `build`
  for C++ or framework changes).
- `docker compose run --rm lint` passes.
- README, docs, and CHANGELOG reflect the change.
- Changes are on a branch with a PR open, not on `main`.
- You've told the human what you did not test.
