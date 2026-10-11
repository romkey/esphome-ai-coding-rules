---
name: release
description: Cut a release of the current ESPHome project following the esphome-ai-coding-rules release process.
argument-hint: "[major|minor|patch|X.Y.Z]"
disable-model-invocation: true
---

Prepare a release. Arguments: `$ARGUMENTS` (bump type or exact version;
optional). The process is in `${CLAUDE_PLUGIN_ROOT}/docs/releasing.md`;
read it first.

1. Check: on `main`, working tree clean, up to date with `origin/main`, and
   the latest CI and Lint runs on `main` passed
   (`gh run list --branch main --limit 5`). Stop and report if not.
2. Read `## [Unreleased]` in CHANGELOG.md. If it's empty, stop: nothing to
   release.
3. Choose the version. If not given, propose one from the entries using
   RULES.md §9 (breaking → major, or minor before 1.0.0; new features →
   minor; fixes → patch) and explain why. Confirm with the human.
4. Edit: move the Unreleased entries under `## [X.Y.Z] - YYYY-MM-DD` (today),
   leaving an empty `## [Unreleased]`; set every `project_version` to
   `"X.Y.Z"`; bump `version` in `.claude-plugin/plugin.json` if present;
   update pinned `@vX.Y.Z` references to this repo in README/docs.
5. Verify: `scripts/changelog-section.sh X.Y.Z` prints the notes, and
   `docker compose run --rm validate` passes.
6. Commit `Release vX.Y.Z` and create an annotated tag
   `git tag -a vX.Y.Z -m "vX.Y.Z"`.
7. Show the human the commit and tag, and push only when they confirm:
   `git push origin main vX.Y.Z`. Then watch the Release workflow
   (`gh run watch`) and report the release URL.
