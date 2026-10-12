# Upgrading repos that follow these rules

These rules change, and repos set up under an older version don't pick up
fixes on their own. Each entry below is a change that **existing repos
must apply**, newest first.

**AI assistants re-scanning a repo** (for example with
`/esphome-rules:check`): read the version in the repo's `AGENTS.md`
("Follows esphome-ai-coding-rules vX.Y.Z"; treat a missing one as v0.0.0),
apply every entry newer than it (and any `Unreleased` ones, if you're
working from `main`), then update that line to the current release. Check each entry against what's actually there; a repo may have
diverged deliberately, so ask before overwriting customizations.

**Anyone changing these rules**: when a change means existing repos must
update something, add an entry here in the same PR, headed
`## Unreleased: <what changed>`. Don't guess the version: cutting a release
(`scripts/bump-version.sh`) renames `Unreleased` to it. An entry is only
needed for something a release shipped; a bug fixed before its release
needs none.

## v0.6.1: record the rules version

Repos didn't record which version of these rules they follow, so there was
no way to tell which entries here they still need.

- **Check:** no "Follows esphome-ai-coding-rules vX.Y.Z" line in
  `AGENTS.md`.
- **Fix:** add it, in the wording of `templates/AGENTS.md`, set to the
  version you're upgrading the repo to. Before that, work out which
  entries below the repo already has by checking each one.

## v0.6.1: compose file is docker-compose.yaml

Do this before the other entries from the same release, which refer to the
new name.

- **Check:** the repo has `compose.yaml`, `compose.yml` or
  `docker-compose.yml`.
- **Fix:** `git mv <old name> docker-compose.yaml`, then update every
  reference to the old name (README, docs, AGENTS.md, comments in
  `scripts/`, `renovate.json` descriptions). Commands don't change:
  `docker compose` finds `docker-compose.yaml` on its own.

## v0.6.1: compiled firmware unreachable from the host

`docker-compose.yaml` keeps builds in the `esphome-build` volume, so the
`.factory.bin` needed for a first flash with web.esphome.io (the documented
path on macOS) never reaches the host.

- **Check:** `docker-compose.yaml` mounts `esphome-build:/build` but has no
  `firmware` service, or the repo has no `scripts/export-firmware.py`.
- **Fix:** copy `scripts/export-firmware.py` and the `firmware` service
  from `templates/docker-compose.yaml`; make sure `dist/` and `*.bin` are
  gitignored; point the README's flashing steps at
  `docker compose run --rm firmware` and `dist/<name>.factory.bin`.

## v0.6.1: release workflow can publish the same release twice

`.github/workflows/release.yaml` grouped concurrency by event name, so a
run for a merged `release/vX.Y.Z` PR and a run for the `vX.Y.Z` tag it
pushes didn't serialize, and both called `gh release create`. Harmless
while the tag job pushes with `GITHUB_TOKEN` (those pushes start no
workflows), but the second run fails if it ever pushes with a PAT or App
token.

- **Check:** `concurrency: group: release-${{ github.event_name }}` in
  `release.yaml`, or no "Skip if already released" step.
- **Fix:** take from `templates/.github/workflows/release.yaml`: the
  per-version concurrency group, the `release` job's `if` that skips tag
  pushes by `github-actions[bot]`, the "Skip if already released" step with
  `if: steps.exists.outputs.exists != 'true'` on the steps after it, and
  `firmware: ${{ steps.check.outputs.firmware || '[]' }}`.

## v0.6.0: secret protection

- **Check:** no `esphome-secrets`, `gitleaks` or `no-firmware-images` hooks
  in `.pre-commit-config.yaml`; no `.gitleaks.toml`; `*.bin` not ignored.
- **Fix:** copy `scripts/check-secrets.py`, `.gitleaks.toml`, the three
  hooks, the `.gitignore` firmware lines, the history scan in `lint.yaml`
  (with `fetch-depth: 0`) and the `secrets` compose service from
  `templates/`. Run `docker compose run --rm secrets`; if it finds a real
  secret, tell the owner to rotate it.

## v0.5.0: device defaults and USB logging

- **Check:** `web_server:` missing, without `version: 3`, without
  `ota: false`, or with `auth` but no `type: digest`; ESP32-C3/S3 examples
  on boards with a USB-to-UART bridge without `logger: hardware_uart:
  UART0`; no `factory_reset` button, `time:`, `min_version` or `comment`.
- **Fix:** follow `templates/examples/common/base.yaml` and RULES.md §1/§3.
  The UART0 fix matters most: without it, logs and Improv serial never
  reach the USB port on those boards. Published firmware: add the
  `update: http_request` block, and use the current `collect-firmware.sh`
  so manifests include the OTA image and md5.

## v0.4.0: published firmware Wi-Fi setup

- **Check:** a `firmware/` config without `esp32_improv:` (or
  `improv_ble:`) or `provisioning:`.
- **Fix:** follow `templates/optional/firmware-publishing/firmware/esp32.yaml`.

## v0.3.0: protected main and PR-based releases

- **Check:** no "Protect main" ruleset; a CI workflow with `paths` or
  `paths-ignore`; no "CI passed" job; a release workflow that pushes to
  `main` or starts CI with `gh workflow run` instead of approving the
  release PR's held runs; no `datasheets/*-license.txt` for datasheets.
- **Fix:** copy `ci.yaml`, `lint.yaml`, `release.yaml`, `SECURITY.md`,
  `scripts/setup-github.sh` and `scripts/bump-version.sh` from
  `templates/`, then ask the owner before running `setup-github.sh` (it
  changes repo settings). Add datasheet license files.
