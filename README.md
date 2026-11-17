# remove-ai-look

A Claude skill that stops frontends from looking AI-generated. It audits a project for stock defaults, makes the agent pick a real, documented design system as its theme before writing styles, and enforces that theme at the source.

Made by [rdjarbeng.com](https://rdjarbeng.com/about/) by [RDjarbeng](https://github.com/RDjarbeng)

## What it does

Models reproduce the most common public code, so the "AI look" is really the look of unconfigured defaults. There are two main versions:

- **The SaaS template**: stock indigo accents, purple-to-blue gradients, big radii and shadows on every card, Inter for everything, and copy that promises to "empower your team".
- **The mission-control HUD**: what models fall back to when told to avoid the first one. Near-black navy panels, glowing neon cyan and green, monospace uppercase labels with wide letter-spacing, "01." numbered sections, "ENGINE ACTIVE" badges and emoji buttons.

Asking the model to "be original" just moves it from one to the other. So instead of inventing a palette, the skill makes the agent choose a theme from a catalogue of real design systems and visual traditions, and follow its tokens and habits exactly.

It covers an audit, picking a theme (or offering you three to choose from), writing the tokens down, enforcing them in the build, a copy pass, a visual check and a CI check. Your own direction and any existing design system always take priority.

## Themes

[`references/themes.md`](skills/remove-ai-look/references/themes.md) has tokens (colours, fonts, type scale, radius, spacing) and component habits for:

| Theme | Feel |
|---|---|
| IBM Carbon | Square, dense, Plex type, very legible numbers |
| GitHub Primer | Bordered boxes, system fonts, quiet and practical |
| Microsoft Fluent 2 | Soft 4px controls, command bars, Segoe |
| Google Workspace | White canvas, thin grey borders, pill chips |
| Material 3 | Tonal surfaces from a seed colour (not the baseline purple) |
| Apple HIG | Inset grouped lists, large bold titles |
| USWDS | Public Sans, plain forms, built for everyone |
| GOV.UK style | Big plain type, one question per page, yellow focus |
| Swiss | Black, white, one red, a strict grid, huge type |
| Editorial paper | Salmon paper, serif headlines, rules instead of boxes |
| Lab report | Reads like a journal paper, numbered figures and captions |
| Instrument panel | Light, tactile hardware look, one orange signal colour |
| Plain web | Default HTML on purpose |

The skill tells the agent to default to a light theme, and to use a theme's own dark tokens (grey surfaces, muted accents, no glow) when dark mode is wanted. To choose a theme yourself, just name it in your prompt, for example "use the Carbon theme".

## Install

**Claude Code, as a plugin:**

```
/plugin marketplace add RDjarbeng/remove-ai-look-skill
/plugin install remove-ai-look@remove-ai-look-skill
```

**Claude Code, as a personal skill:** copy `skills/remove-ai-look` into `~/.claude/skills/`.

**claude.ai or the desktop app:** download `remove-ai-look.skill` from the [latest release](https://github.com/RDjarbeng/remove-ai-look-skill/releases/latest) and upload it under your skills settings.

**Antigravity, Codex, Gemini CLI and other agents:** copy the whole `skills/remove-ai-look` folder (including `references/` and `scripts/`) into the agent's skills folder, or point them at [`skills/remove-ai-look/SKILL.md`](skills/remove-ai-look/SKILL.md).

## The audit script

Python 3, no dependencies:

```
python skills/remove-ai-look/scripts/check_ai_defaults.py path/to/project
```

It reports each finding as `file:line: rule: matched text` and exits 1 if it finds any, so it can run in CI.

| Rule | Catches |
|---|---|
| `stock-accent` | Tailwind indigo, violet and purple utilities |
| `stock-gradient` | Purple-to-blue/pink gradients |
| `reflex-card` | `rounded-2xl`/`3xl` with `shadow-lg`/`xl` |
| `stock-font` | Inter as the font family |
| `stock-copy` | Marketing phrases and fake status text ("supercharge your", "engine active") |
| `neon-color` | Saturated neon cyan, green and magenta; `--neon`/`--glow`/`--phosphor` variables |
| `glow` | Zero-offset coloured shadows, glow `drop-shadow`, canvas `shadowBlur`, Tailwind coloured shadows |
| `dark-navy` | Near-black blue backgrounds, reported only when the file also uses neon |
| `glass` | `backdrop-filter: blur` glassmorphism |
| `gradient-text` | `background-clip: text` |
| `emoji-ui` | Emoji in buttons, links, headings and labels |
| `hud-type` | Uppercase letter-spaced labels or monospace used all over a file |

Zero findings does not prove a page looks designed; the skill also asks the agent to check a screenshot by eye.

## License

MIT. See [LICENSE](LICENSE).

## Credit

Based on ideas from ["How to fix the 'AI-generated' look in your frontend"](https://dev.to/alanwest/how-to-fix-the-ai-generated-look-in-your-frontend-1ahh) by Alan West.
