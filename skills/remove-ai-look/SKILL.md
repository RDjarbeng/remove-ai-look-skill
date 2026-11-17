---
name: remove-ai-look
description: Eliminate the generic, templated "AI-generated look" from web frontends. Covers both the purple-gradient SaaS look and the dark neon "mission control" look (near-black panels, glowing cyan/green accents, monospace uppercase labels, HUD badges), plus glassmorphism, gradient text and emoji buttons. Grounds every design in a chosen, documented theme (Material, IBM Carbon, GitHub Primer, Fluent, USWDS, Swiss, editorial, lab-report and others) instead of the model's averaged taste. Use whenever building, restyling, or reviewing a frontend, including landing pages, dashboards, tools, simulators and web components, and whenever a user says a page looks generic, AI-made, templated, "techy", glowing or like ChatGPT made it. Do not use for backend tasks or standalone charts.
---

# Remove AI Look

## Why this happens
Models output the statistical average of public code. There is not one AI look but a few, and banning one only pushes the model into the next. Ban purple gradients and you get a near-black dashboard with neon cyan, monospace caps and a status badge that says "SYSTEM ONLINE". Asking the model to "be original" does not help, because its idea of original is also averaged.

What works is to **borrow a real, documented design system** whose decisions came from people with taste and constraints, and follow its tokens exactly. A page that looks like IBM Carbon, GitHub or a printed lab report does not look AI-made, because AI output does not look like those.

## Precedence
1. Direct user instructions always win, including a request for dark mode or neon.
2. An existing brand or project design system comes next.
3. This skill applies third.

If the user wants "a blue theme", take a blue from one of the themes in `references/themes.md`, not Tailwind `blue-500`.

## Workflow

### 1. Audit
Run `python scripts/check_ai_defaults.py <path>` from the skill folder. Read every finding. **Zero findings does not mean the page is fine**: the script only catches what regex can see. Also check the page by eye against the fingerprint list below.

### 2. Pick a theme before writing any CSS
Open `references/themes.md` and choose one theme. Do not invent a palette from scratch.
- If the user named a theme or brand, use it.
- If you can ask the user, offer **three themes from different families** (for example one systematic, one editorial, one product), each with one sentence on why it suits this project, and let them pick.
- If you cannot ask, pick the theme that best fits the domain (the table at the top of `themes.md` maps domains to themes) and state the choice and reason in your reply.
- **Default to a light theme.** Use dark only if the user asked, the existing project is dark, or the use is genuinely low-light (media playback, astronomy, night use). When dark, use the theme's own dark tokens: grey surfaces and desaturated accents, never neon on navy.

### 3. Write the tokens down
Copy the chosen theme's tokens into CSS custom properties (or the framework's theme config) before styling any component: colours, font stack, type scale, radius, spacing, border and elevation rules. Replace framework defaults rather than extending them, so stock tokens fail to compile.

### 4. Build with the theme's habits, not just its colours
Each theme in `themes.md` lists how its components behave (button shape, how sections are separated, how headings look, how data is shown). Follow those. A Carbon page with rounded glowing cards is not a Carbon page.

### 5. Write plain copy
Read every heading and label aloud. Use sentence case for headings and labels unless the theme says otherwise. Cut marketing verbs ("empower", "unlock", "supercharge", "elevate") and fake system chatter ("ENGINE ACTIVE", "SYSTEM ONLINE", "NEURAL CORE"). Labels should say what the thing is: "Rainfall rate (mm/h)", not "PEAK DROPLET FLUX".

### 6. Look at the result
Render the page and take a screenshot if you can. Ask: *if I removed the product name, would a designer guess an AI made this?* If the screenshot matches any fingerprint below, fix it before finishing. Re-run the audit script.

### 7. Lock it in
Add the audit script or an equivalent lint rule to CI so the look does not drift back.

## Fingerprints to eliminate

### The SaaS template look
- Tailwind indigo, violet, purple or slate as the accent.
- Purple-to-blue or purple-to-pink gradient heroes.
- Hero, then three identical icon cards, then three pricing tiers, then an FAQ accordion.
- `rounded-2xl`/`rounded-3xl` plus `shadow-lg`/`shadow-xl` on every box.
- Inter for everything at default tracking; everything centred.

### The mission-control look (dark neon HUD)
This is what models produce when told to avoid the SaaS look. Avoid all of it unless the user explicitly asks for it:
- Near-black blue-tinted backgrounds (`#0b0e14`, `#0f172a`, `slate-900/950`) with slightly lighter "panel" boxes.
- Neon accents: saturated cyan (`#00e5ff`, `#22d3ee`), electric green (`#00e676`, `#39ff14`), hot magenta, often called "phosphor", "glow" or "neon" in variable names.
- Glow of any kind: `box-shadow`/`text-shadow` with zero offset and a coloured blur, `drop-shadow` filters, canvas `shadowBlur`, gradient progress bars fading into the accent.
- Monospace used for labels, buttons and headings, not just numbers.
- UPPERCASE labels with wide letter-spacing on most text.
- Numbered section headers ("01. CASING MATERIAL").
- Status pills and fake telemetry: "ENGINE ACTIVE", "SYSTEM READY", spec strings like "FS: 44.1 kHz | 16-BIT PCM" in the header.
- A grid of small "stat tiles" each with a tiny caps label and a big coloured number.
- Science or engineering words used as decoration ("telemetry deck", "chassis", "flux").

### Other common tells
- Glassmorphism: `backdrop-filter: blur` panels over gradient blobs.
- Gradient text (`background-clip: text`).
- Emoji as icons in buttons and headings ("📊 Export", "🚀 Get started").
- Bento grids of mismatched rounded tiles.
- The "warm editorial" default: cream background, a serif heading font and a terracotta or orange accent used by itself without a real editorial structure.
- A different accent colour on every tile or metric.

## Guardrails
- **Contrast**: text and controls meet WCAG AA in every theme.
- **Focus**: keep visible focus indicators; use the theme's own focus style.
- **Two modes**: if both light and dark are needed, use the theme's documented dark tokens; do not invert.
- **Usability first**: dashboards and tools stay dense and scannable. A theme is a constraint, not an excuse for decoration.
- **No impersonation**: borrow a design system's tokens and habits, not its logos, product names, or restricted fonts (for example GDS Transport is for UK government services only). Use the open-source fallbacks listed in `themes.md`.

## Credit
Based on ideas from the article ["How to fix the 'AI-generated' look in your frontend"](https://dev.to/alanwest/how-to-fix-the-ai-generated-look-in-your-frontend-1ahh) by Alan West.

Made by [rdjarbeng.com](https://rdjarbeng.com/about/) by [RDjarbeng](https://github.com/RDjarbeng)
