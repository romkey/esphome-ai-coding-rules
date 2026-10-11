---
name: release
description: Cut a release of the current ESPHome project following the esphome-ai-coding-rules release process.
argument-hint: "[patch|minor|major]"
disable-model-invocation: true
---

Prepare a release. Arguments: `$ARGUMENTS` (bump type; optional). The process is in `${CLAUDE_PLUGIN_ROOT}/docs/releasing.md`;
read it first.

1. Check: on `main`, working tree clean, up to date with `origin/main`, and
   the latest CI and Lint runs on `main` passed
   (`gh run list --branch main --limit 5`). Stop and report if not.
2. Read `## [Unreleased]` in CHANGELOG.md. If it's empty, stop: nothing to
   release.
3. Choose the bump (`patch`, `minor` or `major`). If not given, propose
   one from the entries using RULES.md §9 (breaking → major, or minor
   before 1.0.0; new features → minor; fixes → patch) and explain why.
   Confirm with the human.
4. If pinned `@vX.Y.Z` references to this repo in README/docs need the new
   version, commit and push that first.
5. Preferred: run the Release workflow, which bumps, commits, tags and
   publishes: `gh workflow run release.yaml -f bump=<bump>`, then watch it
   (`gh run watch`) and report the release URL.
6. If the workflow can't push (e.g. branch protection): run
   `scripts/bump-version.sh <bump>`, check
   `scripts/changelog-section.sh X.Y.Z` and
   `docker compose run --rm validate`, commit `Release vX.Y.Z`, tag
   `git tag -a vX.Y.Z -m "vX.Y.Z"`, show the human, and push only when
   they confirm: `git push origin main vX.Y.Z`.
