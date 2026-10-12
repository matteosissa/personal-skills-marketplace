# Personal Skills Marketplace

A personal Claude Code plugin marketplace.

## Use it

```
/plugin marketplace add <path-or-github-user/repo>
/plugin install deep-explainer@personal-skills-marketplace
```

For a local checkout, use its path, e.g. `/plugin marketplace add C:\Users\Matteo\Desktop\personal-skills-marketplace`.

## Layout

```
.claude-plugin/marketplace.json     # catalog of plugins
plugins/<plugin>/
  .claude-plugin/plugin.json        # plugin manifest
  skills/<skill>/SKILL.md           # skills (also: commands/, agents/, hooks/, .mcp.json)
```

## Plugins

| Plugin | What it does |
| --- | --- |
| deep-explainer | Learn topics from zero: `ground-up-explainer` (dependency graph) and `socratic-ground-up` (question-driven) |
| live-tutorial | User-driven, hands-on guided tutorials |
| knowledge-base | Obsidian vault skills; currently `validate-knowledge-base` |

## Add a new plugin

1. Create `plugins/<name>/.claude-plugin/plugin.json` (`name`, `version`, `description`).
2. Add skills under `plugins/<name>/skills/<skill>/SKILL.md` (or commands, agents, hooks, MCP config).
3. Add an entry to `.claude-plugin/marketplace.json` with `"source": "./plugins/<name>"`.
4. Validate with `claude plugin validate .`, then `/plugin marketplace update`.

External plugins can be listed too, with a source such as `{"source": "github", "repo": "owner/repo"}`.
