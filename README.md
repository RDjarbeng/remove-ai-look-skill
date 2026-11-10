# remove-ai-look

A Claude skill that stops frontends from looking AI-generated. It audits a project for stock defaults, makes the agent commit to its own design vocabulary before writing styles, and enforces that vocabulary at the source.

Made by [rdjarbeng.com](https://rdjarbeng.com/about/) by [RDjarbeng](https://github.com/RDjarbeng)

## What it does

Models reproduce the most common public code, so the "AI look" is really the look of unconfigured defaults: stock indigo accents, purple-to-blue gradients, big radii and shadows on every card, Inter for everything, and copy that promises to "empower your team". This skill removes those defaults instead of asking the model to be more creative.

It covers an audit, a written design vocabulary, enforcing that vocabulary in the build, a copy pass, and a CI check. Your own direction and any existing design system always take priority.

## Install

**Claude Code, as a plugin:**

```
/plugin marketplace add RDjarbeng/remove-ai-look-skill
/plugin install remove-ai-look@remove-ai-look-skill
```

**Claude Code, as a personal skill:** copy `skills/remove-ai-look` into `~/.claude/skills/`.

**claude.ai or the desktop app:** download `remove-ai-look.skill` from the [latest release](https://github.com/RDjarbeng/remove-ai-look-skill/releases/latest) and upload it under your skills settings.

**Other agents:** point them at [`skills/remove-ai-look/SKILL.md`](skills/remove-ai-look/SKILL.md).

## The audit script

Python 3, no dependencies:

```
python skills/remove-ai-look/scripts/check_ai_defaults.py path/to/project
```

It reports each finding as `file:line: rule: matched text` and exits 1 if it finds any, so it can run in CI. The rules are `stock-accent`, `stock-gradient`, `reflex-card`, `stock-font` and `stock-copy`.

## Credit

Based on ideas from ["How to fix the 'AI-generated' look in your frontend"](https://dev.to/alanwest/how-to-fix-the-ai-generated-look-in-your-frontend-1ahh) by Alan West.
