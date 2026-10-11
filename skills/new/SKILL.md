---
name: new
description: Scaffold a new ESPHome project that follows romkey's ESPHome AI coding rules.
argument-hint: "[repo-name] [library|app]"
disable-model-invocation: true
---

Create a new ESPHome project from the esphome-ai-coding-rules templates.
Arguments: `$ARGUMENTS` (repo name, then `library` or `app`; both optional).

1. Read `${CLAUDE_PLUGIN_ROOT}/RULES.md` in full. Everything below follows it.
2. Work out the repo name and kind. Default the name to the current
   directory's name. If the kind isn't given, ask: a **library** provides
   packages/components for other projects; an **app** is a device people
   flash. For an app, also ask whether to publish installable firmware.
3. Ask what the project does and what hardware it uses (boards, sensors,
   buses). Don't invent hardware details; leave TODOs for anything unknown.
4. Target directory: the current directory if it is empty or already named
   after the repo, otherwise `./<repo-name>`. Never overwrite an existing
   file without asking.
5. Copy `${CLAUDE_PLUGIN_ROOT}/templates/.` (dotfiles included) into the
   target, then delete `optional/` from the copy. If publishing firmware,
   first copy `optional/firmware-publishing/firmware` and `.../web` to the
   target root.
6. Fill in placeholders everywhere: `REPO` → repo name, `PROJECT` → title,
   `romkey.REPO` → `romkey.<repo-name>`, the LICENSE year → current year.
   Replace `packages/example.yaml` and the README/docs prose with the real
   project, or leave them clearly marked as TODO if details are missing.
7. Look up current versions (RULES.md §8): the latest esphome-lib tag and
   the actions in `.github/workflows/`. Update any that are stale.
8. `git init`, `ln -s AGENTS.md CLAUDE.md`, then
   `cp examples/secrets.yaml.example examples/secrets.yaml` and run
   `docker compose run --rm validate` and `docker compose run --rm lint`.
   Fix failures.
9. Report what you created, what is still TODO, and what you didn't test.
   Don't create a GitHub repo, commit, or push unless asked.
