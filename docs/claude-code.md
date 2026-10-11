# Using the rules with Claude Code

This repo is also a Claude Code plugin, **esphome-rules**, distributed from
its own marketplace, **romkey**.

## Install

In Claude Code:

```
/plugin marketplace add romkey/esphome-ai-coding-rules
/plugin install esphome-rules@romkey
```

Or from a shell:

```bash
claude plugin marketplace add romkey/esphome-ai-coding-rules
```

```bash
claude plugin install esphome-rules@romkey
```

## Commands

| Command | What it does |
|---------|--------------|
| `/esphome-rules:new [name] [library\|app]` | Scaffolds a project from `templates/`, asks what it does and what hardware it uses, fills in placeholders, looks up current versions, validates and lints. Doesn't create a GitHub repo or push unless you ask. |
| `/esphome-rules:check [fix]` | Audits the current repo against RULES.md and reports findings by section. With `fix`, applies them and re-runs validate and lint. |
| `/esphome-rules:release [major\|minor\|patch\|X.Y.Z]` | Prepares a release per [releasing.md](releasing.md): checks CI, proposes the version, updates CHANGELOG and `project_version`, commits and tags. Pushes only after you confirm. |

There is also a **rules** skill that Claude loads by itself when it works on
ESPHome YAML, components or CI in a repo that follows these rules, so you
don't have to paste RULES.md into the conversation.

## Updating

```bash
claude plugin marketplace update romkey
```

```bash
claude plugin update esphome-rules@romkey
```

Then restart Claude Code or run `/reload-plugins`. The plugin's version
follows this repo's release tags.

## Without the plugin

Every project's `AGENTS.md` (symlinked as `CLAUDE.md`) says to follow
RULES.md, which works with Claude Code and other AI tools. Or just tell the
assistant: "Follow https://github.com/romkey/esphome-ai-coding-rules/blob/main/RULES.md".
