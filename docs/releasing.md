# Release strategy

How every repo that follows these rules is versioned and released. The
short version is in [RULES.md §9](../RULES.md#9-releases); this explains the
reasoning and walks through a release.

## Why release at all

People use these repos by reference:
`github://romkey/esphome-lib/lib/esp32.yml@v0.2.0`, or an
`external_components` source, or a flashed firmware image. A tag is a promise
that the thing at that reference never changes, so a device config that
builds today still builds next year. Tracking `@main` is allowed but means
accepting surprises. Renovate turns new tags into pull requests for
downstream projects, so pinning costs nothing in freshness.

## Versions

[Semantic versioning](https://semver.org/), tags `vX.Y.Z`:

| Bump | When | Examples |
|------|------|----------|
| **Major** | Something that worked stops working | Removing/renaming a package, substitution, id, entity name or required bus id; raising `min_version`; dropping a board |
| **Minor** | New things, nothing breaks | New package, option, sensor or supported board |
| **Patch** | Fixes only | Bug fixes, docs, CI, dependency bumps |

Entity names and ids count as API: Home Assistant keys history and
automations on them, so a rename silently breaks people's dashboards.

Before 1.0.0, breaking changes bump the minor (0.3.0 → 0.4.0) and everything
else bumps the patch. Go to 1.0.0 once the package interfaces have settled.

Pre-releases (`v1.2.0-rc.1`) are published as GitHub pre-releases, for
testing a big change on real hardware before committing to it.

## The changelog is the source of truth

Every change adds a line under `## [Unreleased]` in CHANGELOG.md, in the
same commit. At release time those lines become the version's section and,
verbatim, the GitHub Release notes. The release workflow refuses to publish
a version with no changelog section, so a release can't go out undocumented.

## Branches

`main` is always releasable: CI and Lint pass on every merge. Releases are
cut from `main`. No release branches; if an old major ever needs a fix,
branch from its tag then.

## Cutting a release

With the Claude Code plugin: `/esphome-rules:release`. It does the steps
below and asks before pushing. By hand:

1. Make sure `main` is clean, current and green.
2. Pick the version from the Unreleased entries using the table above.
3. In CHANGELOG.md, rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`
   and add a fresh empty `## [Unreleased]` above it.
4. Set every `project_version: "X.Y.Z"` (examples/common/base.yaml,
   firmware/) and any pinned `@vX.Y.Z` self-references in README/docs.
5. Check: `scripts/changelog-section.sh X.Y.Z` and
   `docker compose run --rm validate`.
6. Commit and tag:

   ```bash
   git commit -am "Release vX.Y.Z"
   git tag -a vX.Y.Z -m "vX.Y.Z"
   git push origin main vX.Y.Z
   ```

## What the tag triggers

`.github/workflows/release.yaml`:

1. Checks the CHANGELOG section exists and every `project_version` equals
   the tag. Fails loudly otherwise; delete the tag, fix, re-tag.
2. Creates the GitHub Release with the changelog section as its notes
   (marked pre-release if the tag has a `-suffix`).
3. **Applications with `firmware/` only:** builds each firmware config,
   attaches `<name>.factory.bin` (full image for a blank chip) and
   `<name>.ota.bin` (OTA update) to the release, and deploys a browser
   installer to GitHub Pages using
   [ESP Web Tools](https://esphome.github.io/esp-web-tools/).

Libraries stop after step 2: their consumers build from source.

## Published firmware

Optional, for applications. Copy
[`templates/optional/firmware-publishing/`](../templates/optional/firmware-publishing/)
and follow its README.

Firmware configs are separate from examples because examples are built with
CI's dummy secrets, and a published image must contain none. Firmware
configs instead:

- configure Wi-Fi after flashing: the web installer asks for it over Improv,
  or the device opens a fallback hotspot with a captive portal;
- have the API key provisioned when Home Assistant adopts the device
  (`dashboard_import`);
- set `name_add_mac_suffix` so several devices can share one image;
- carry `project:` name and version, so Home Assistant shows what's
  installed and ESPHome can offer updates.

## If a release goes wrong

- Workflow failed before the Release was created: fix on `main`, then move
  the tag: `git tag -d vX.Y.Z && git push origin :vX.Y.Z`, re-tag, push.
- A bad release is already public: don't rewrite it. Release a patch
  (`X.Y.Z+1`) with the fix, and mark the bad one in its notes.
