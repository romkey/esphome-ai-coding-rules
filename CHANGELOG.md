# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.6.0] - 2026-10-11

### Added

- Secret protection. A pre-commit check (`scripts/check-secrets.py`) fails
  if a value from your local `secrets.yaml` appears in a committed file, if
  an ESPHome config hard-codes a password, SSID or key instead of
  `!secret`, or if a published firmware config uses `!secret`; it never
  prints the value. gitleaks checks staged changes, and the Lint job and a
  new `secrets` compose service scan the whole history. Firmware images
  (`.bin` etc., which contain the Wi-Fi credentials they were built with)
  are gitignored and rejected. `setup-github.sh` also turns on generic
  secret patterns and validity checks where available (they need GitHub
  Secret Protection) and reports when they aren't. RULES.md: never expose
  secrets; rotate any that leak.

## [0.5.0] - 2026-10-11

### Added

- Examples include web server version 3 (set explicitly; ESPHome defaults
  to 2) with digest auth from secrets and its unencrypted upload page off,
  Home Assistant time, a factory reset button, `min_version`, and a
  `comment`.
- Rules for board facts: `flash_size` from the module's documentation, and
  `logger: hardware_uart: UART0` on ESP32-C3/S3 boards whose USB goes
  through a USB-to-UART bridge (ESPHome logs to built-in USB by default, so
  logs and Improv serial would never reach the port).
- Published firmware checks for updates from GitHub releases
  (`update: platform: http_request`); release manifests now include the OTA
  image, its md5 and the release URL. Published firmware also logs at INFO
  and has a factory reset button.

### Fixed

- The ESP32-C3 and ESP32-S3 examples now log over their USB-to-UART ports.

## [0.4.0] - 2026-10-11

### Added

- Published firmware can be set up on anyone's Wi-Fi from a phone over
  Bluetooth (Improv BLE), alongside the web installer (Improv serial) and
  fallback hotspot, with a 30-minute setup window (`provisioning:`) that
  closes setup on unconfigured devices. RULES.md notes ESPHome doesn't
  support ESP RainMaker and Improv is its equivalent.

## [0.3.0] - 2026-10-11

### Added

- Datasheets live in `datasheets/`, each with a `<name>-license.txt`
  crediting the manufacturer; a pre-commit hook enforces it, and README
  License sections say datasheets aren't covered by the repo's license.
- On first use, ask the owner whether to use MIT or another license, and
  use the chosen license's official text instead of MIT.
- Protected `main`: changes only through squash-merged PRs with "CI passed"
  and "Lint" green. `scripts/setup-github.sh` applies the ruleset plus
  secret scanning with push protection, Dependabot alerts, private
  vulnerability reporting, CodeQL and read-only workflow tokens.
- SECURITY.md.

### Changed

- The Release button opens a release PR instead of pushing to `main`, and
  approves the PR's CI and Lint runs, which GitHub holds on PRs opened by
  a workflow; merging it tags and publishes.
- CI always runs so its required check reports, skips firmware builds for
  docs-only changes, and ends with a stable "CI passed" job. Beta failures
  are warnings. A manual CI run can opt into the beta build.

## [0.2.0] - 2026-10-11

### Added

- Release workflow can be run from the Actions tab with a patch, minor or
  major bump (default patch); it updates CHANGELOG.md and `project_version`,
  commits, tags and publishes. New `scripts/bump-version.sh` does the edits
  and is shared by the workflow, the release skill and humans.

### Fixed

- Firmware publishing: release jobs no longer get skipped on tag pushes,
  and the kit README explains allowing release tags to deploy to Pages.

## [0.1.0] - 2026-10-11

### Added

- RULES.md: AI conduct, layout, YAML, examples, Home Assistant conventions,
  custom components, Docker, git and pre-commit, GitHub workflows, releases,
  documentation, license.
- Buildable template project with ESP32, ESP32-C3 and ESP32-S3 examples,
  example sensor and UI packages, and shared base config with encrypted
  API/OTA, fallback hotspot and safe mode.
- compose.yaml with validate, build, lint and dashboard services, using the
  ESPHome image's /cache and /build volumes for incremental builds.
- CI with uv, ccache, toolchain and build caches, weekly ESPHome beta build,
  and unit tests; lint via pre-commit; release workflow driven by
  CHANGELOG.md.
- Optional firmware publishing kit: release images and an ESP Web Tools
  installer on GitHub Pages, from secret-free firmware configs.
- Renovate config that also updates `github://` package tags.
- shellcheck, bundled into the actionlint hook so workflow shell is
  checked the same way locally and in CI.
- Claude Code plugin `esphome-rules` with `new`, `check`, `release` and
  `rules` skills, and its marketplace.
- Release strategy, Claude Code, configuration and overview docs.
