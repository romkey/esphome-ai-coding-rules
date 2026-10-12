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

`main` is protected: every change arrives through a squash-merged PR whose
**CI passed** and **Lint** checks pass, so `main` is always releasable.
Releases are cut from `main`. The only other long-lived names are
`release/vX.Y.Z` branches, which exist just until their release PR merges.
If an old major ever needs a fix, branch from its tag then.

## Cutting a release

**From GitHub (easiest):** Actions tab → **Release** → **Run workflow**,
choose the bump and run. Patch is the default; minor resets patch to 0;
major resets minor and patch to 0 (1.4.2 → 1.4.3, 1.5.0 or 2.0.0). The
workflow:

1. refuses to run from anything but `main`; waits up to 30 minutes for
   CI on that commit to finish (so you can run it right after merging),
   and stops if CI didn't pass;
2. runs `scripts/bump-version.sh` on a new `release/vX.Y.Z` branch: it
   finds the latest `vX.Y.Z` tag (none yet means 0.0.0), computes the next
   version, refuses if `## [Unreleased]` is empty, moves those entries
   under the new version with today's date, and sets every
   `project_version`;
3. opens a **Release vX.Y.Z** PR with the release notes, and approves the
   PR's CI and Lint runs (GitHub holds runs on PRs opened by a workflow
   until someone approves them). If it can't, the run shows a warning: open
   the PR and click **Approve and run workflows**.

Review the PR and merge it when the checks pass. Merging tags the merge
commit `vX.Y.Z` and runs the release steps below. To abandon a release,
close the PR; nothing is tagged.

**With Claude Code:** `/esphome-rules:release` proposes the bump from the
Unreleased entries, runs the workflow, and tells you when the PR is ready
to merge.

**By hand** (on a branch, through a PR like any other change):

1. Start from an up-to-date, green `main`.
2. Pick the bump from the Unreleased entries using the table above.
3. `scripts/bump-version.sh <patch|minor|major>` updates CHANGELOG.md and
   every `project_version` and prints the new version. Update any pinned
   `@vX.Y.Z` self-references in README/docs yourself.
4. Check: `scripts/changelog-section.sh X.Y.Z` and
   `docker compose run --rm validate`.
5. Commit on a `release/vX.Y.Z` branch, push, and open a PR titled
   `Release vX.Y.Z`. Merging it tags and publishes, as above.

## What the release workflow does

`.github/workflows/release.yaml`, once the release PR merges (or on a tag
you pushed):

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
CI's dummy secrets, and a published image must contain none and work on
anyone's Wi-Fi. Firmware configs instead:

- configure Wi-Fi after flashing: the web installer asks for it over USB,
  a phone can set it over Bluetooth, or the device opens a fallback hotspot
  with a captive portal (all Improv or ESPHome built-ins; ESPHome doesn't
  support ESP RainMaker);
- close those setup paths if the device isn't set up within 30 minutes of
  power-on (`provisioning:`), until it's power-cycled;
- have the API key provisioned when Home Assistant adopts the device
  (`dashboard_import`);
- set `name_add_mac_suffix` so several devices can share one image;
- carry `project:` name and version, so Home Assistant shows what's
  installed and ESPHome can offer updates.

## If a release goes wrong

- Release PR's checks fail: fix on a normal PR to `main`, close the release
  PR, delete its branch, and run the Release workflow again.
- Tagged, but the Release wasn't created: fix the cause, then re-run the
  failed jobs of that Release run from the Actions tab.
- A bad release is already public: don't rewrite it. Release a patch
  (`X.Y.Z+1`) with the fix, and mark the bad one in its notes.
