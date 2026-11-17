# Theme catalogue

Pick one theme, copy its tokens, and follow its habits. Each theme is based on a public design system or a well-known visual tradition, so the result looks designed by people rather than averaged by a model.

Values are given for the light mode. Dark tokens are listed where the source system documents them. Use open fonts from the "Fonts" line; never ship a restricted brand font or logo.

## Which theme for which project

| Project | Good fits |
|---|---|
| Data tools, dashboards, enterprise apps | Carbon, Fluent 2, Primer |
| Developer tools, docs, CLIs with a web UI | Primer, Plain web, Carbon |
| Scientific tools, simulators, research demos | Lab report, Carbon, Instrument panel |
| Hardware, audio, physical-device control UIs | Instrument panel, Carbon, Swiss |
| Public services, forms, anything for a broad audience | USWDS, GOV.UK style, Material 3 |
| Consumer apps, mobile-first | Material 3, Apple HIG, Fluent 2 |
| Blogs, essays, long reading | Editorial paper, Lab report, Swiss |
| Portfolios, posters, event pages | Swiss, Editorial paper, Plain web |
| Office or productivity tools | Google Workspace, Fluent 2 |

When offering choices, pick three from different rows or families, for example: "Carbon (dense, square, very legible for numbers)", "Lab report (reads like a paper, figures with captions)", "Instrument panel (looks like real hardware, light and tactile)".

---

## IBM Carbon
Source: carbondesignsystem.com (Apache 2.0).
- **Fonts**: IBM Plex Sans for UI, IBM Plex Mono only for code and numeric readouts, IBM Plex Serif optional for long text.
- **Colours**: background `#ffffff`, layer `#f4f4f4`, layer-02 `#e0e0e0`, text `#161616`, text secondary `#525252`, border subtle `#e0e0e0`, border strong `#8d8d8d`, interactive/link `#0f62fe`, focus `#0f62fe`, error `#da1e28`, success `#24a148`, warning `#f1c21b`.
- **Dark (g100)**: background `#161616`, layer `#262626`, text `#f4f4f4`, secondary `#c6c6c6`, border `#393939`, interactive `#4589ff`, link `#78a9ff`.
- **Type**: body 14px/20px with 0.16px tracking, headings 20/28, 28/36, 42/50 in weight 400 (light-ish headings, not bold). Sentence case everywhere.
- **Shape**: 0 radius on buttons, inputs, tiles. No shadows except menus and modals.
- **Spacing**: 2, 4, 8, 12, 16, 24, 32, 40, 48px.
- **Habits**: buttons are full-height rectangles with label left and icon right; inputs have a bottom border on a `#f4f4f4` fill; tabs use an underline; data lives in tables with 48px rows; tiles are flat grey blocks; 2px inset focus outline in blue.

## GitHub Primer
Source: primer.style (MIT).
- **Fonts**: `-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif`; code in `ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", monospace`.
- **Colours**: canvas `#ffffff`, canvas subtle `#f6f8fa`, text `#1f2328`, muted `#59636e`, border `#d1d9e0`, accent `#0969da`, success `#1a7f37`, danger `#d1242f`, attention `#9a6700`, done `#8250df` (only for "done/merged" states).
- **Dark**: canvas `#0d1117`, subtle `#151b23`, text `#f0f6fc`, muted `#9198a1`, border `#3d444d`, accent `#4493f8`.
- **Type**: 14px body, 1.5 line height, headings 600 weight, 20/24/32px.
- **Shape**: 6px radius, 1px borders, almost no shadow.
- **Habits**: boxes with a grey header row and bordered list rows; buttons are bordered with a light fill, primary is green `#1f883d`; labels are small rounded pills with 1px borders; counters in grey pills; tabs with an orange underline `#fd8c73`.

## Microsoft Fluent 2
Source: fluent2.microsoft.design.
- **Fonts**: `"Segoe UI Variable", "Segoe UI", system-ui, sans-serif`. Open fallback: Noto Sans or Open Sans.
- **Colours**: brand `#0f6cbd` (hover `#115ea3`, pressed `#0c3b5e`), text `#242424`, secondary `#424242`, tertiary `#616161`, background `#ffffff`, background 2 `#fafafa`, background 3 `#f5f5f5`, stroke `#d1d1d1`, error `#c50f1f`, success `#107c10`.
- **Type**: body 14/20, subtitle 20/28 semibold, title 28/36 semibold.
- **Shape**: 4px radius on controls, 8px on cards and dialogs. Shadow-4: `0 0 2px rgba(0,0,0,.12), 0 2px 4px rgba(0,0,0,.14)`.
- **Habits**: command bars of icon+label buttons; subtle (borderless) buttons for secondary actions; focus is a 2px black-and-white double ring; left navigation rail.

## Google Workspace (classic Google product UI)
Based on Gmail, Drive and Docs.
- **Fonts**: Roboto for body; "Google Sans" only where licensed, otherwise Roboto or an open alternative like Figtree for headings.
- **Colours**: background `#ffffff`, surface `#f8f9fa`, text `#202124`, secondary `#5f6368`, border `#dadce0`, blue `#1a73e8`, selected background `#e8f0fe`, red `#d93025`, green `#188038`, yellow `#f9ab00`.
- **Type**: 14px body, 22px titles, weight 400 or 500, never heavy.
- **Shape**: 4px on inputs, 8px on cards, fully rounded pill buttons and chips.
- **Habits**: white canvas, thin grey borders instead of shadows, blue text buttons for secondary actions, chips for filters, a left nav with the selected item in a pill highlight.

## Material 3
Source: m3.material.io (Apache 2.0 components).
- **Fonts**: Roboto or Roboto Flex.
- **Colours**: generate the scheme from a **seed colour that fits the project** with Material Theme Builder or `@material/material-color-utilities`. Do not use the baseline purple `#6750A4`; that is exactly the AI default.
- **Type**: display 57/64, headline 32/40, title 22/28, body 16/24, label 14/20 weight 500.
- **Shape**: 4px (extra small), 8px, 12px (cards), 16px, 28px (dialogs, FABs), full (buttons, chips).
- **Habits**: tonal surfaces instead of shadows; filled pill buttons for the main action, tonal or outlined for others; top app bar; navigation bar or rail; state layers on hover (8% overlay).

## Apple HIG
Source: developer.apple.com/design.
- **Fonts**: `system-ui, -apple-system` (SF Pro on Apple devices). Fallback: Inter is acceptable only here because it stands in for SF; better open alternative is "Public Sans".
- **Colours**: label `#000000`, secondary label `rgba(60,60,67,.6)`, grouped background `#f2f2f7`, cell `#ffffff`, separator `rgba(60,60,67,.29)`, blue `#007aff`, green `#34c759`, red `#ff3b30`, orange `#ff9500`.
- **Dark**: background `#000000`, grouped `#1c1c1e`, cell `#2c2c2e`, blue `#0a84ff`.
- **Type**: large title 34 bold, title 28, headline 17 semibold, body 17, footnote 13.
- **Shape**: 10–12px on grouped lists, 8px on buttons, continuous corners.
- **Habits**: inset grouped lists with hairline separators; plain text buttons in blue; segmented controls; toggles; large bold page titles left-aligned.

## USWDS (U.S. Web Design System)
Source: designsystem.digital.gov (public domain).
- **Fonts**: Public Sans (open) for UI, Merriweather for long text if wanted, Roboto Mono for code.
- **Colours**: primary `#005ea2`, primary dark `#1a4480`, text `#1b1b1b`, base `#71767a`, border `#dfe1e2`, background light `#f0f0f0`, secondary `#d83933`, accent warm `#fa9441`, accent cool `#00bde3`, success `#00a91c`, focus `#2491ff`.
- **Type**: 17px body (1.06rem) at 1.5 line height, headings bold 22–40px.
- **Shape**: 4px radius on buttons, 0 on inputs.
- **Habits**: plain bordered inputs with labels above, step indicators, alert boxes with a thick left border, generous reading measure (66ch).

## GOV.UK style
Source: design-system.service.gov.uk (MIT code; GDS Transport font and crown are for UK government only).
- **Fonts**: `Arial, Helvetica, sans-serif` (do not use GDS Transport).
- **Colours**: text `#0b0c0c`, secondary `#505a5f`, link `#1d70b8`, visited `#4c2c92`, border `#b1b4b6`, light grey `#f3f2f1`, button green `#00703c`, error `#d4351c`, focus yellow `#ffdd00` with a black underline.
- **Type**: 19px body, bold headings at 48/36/24px, very large and plain.
- **Shape**: 0 radius; buttons have a 2px darker bottom "shadow" edge.
- **Habits**: one thing per page, big question as the H1, radios and checkboxes at 40px, error summary box at the top with a red border.

## Swiss / International Typographic Style
A visual tradition (Müller-Brockmann, Vignelli), not a component library.
- **Fonts**: `"Helvetica Neue", Helvetica, Arial, sans-serif`; open alternatives Archivo or Public Sans.
- **Colours**: white `#ffffff`, black `#111111`, one signal red `#d6001c`, mid grey `#6f6f6f`. No other hues.
- **Type**: big contrast in size (14px body against 64–120px headlines), tight headline leading (1.0), flush left, ragged right.
- **Shape**: 0 radius, no shadows, 1px black rules.
- **Habits**: a strict 12-column grid that is visible in the alignment; lots of white space; numbers and dates set large; asymmetric layouts; no cards, just type and rules.

## Editorial paper
Inspired by printed newspapers, especially the salmon-paper financial press.
- **Fonts**: headings in a serif (Source Serif 4, Newsreader or Georgia), UI and captions in a sans (Source Sans 3 or system).
- **Colours**: paper `#fff1e5`, text `#33302e`, secondary `#66605c`, rule `#ccc1b7`, claret `#990f3d`, teal `#0d7680`, slate blue `#0f5499`.
- **Type**: 18–20px body serif at 1.6 line height, a measure of 60–70ch, small caps or bold sans kickers above headlines.
- **Shape**: 0 radius, rules instead of boxes.
- **Habits**: multi-column front page, kicker + headline + standfirst, bylines and dates, pull quotes with a thick top rule, charts with a title, subtitle and source line.

## Lab report
Inspired by journal papers, LaTeX output and Tufte CSS (MIT). Strong fit for simulators and research tools.
- **Fonts**: body in Charter, Source Serif 4, STIX Two or ET Book; numbers and code in a plain mono (IBM Plex Mono); UI controls in system sans.
- **Colours**: page `#fffff8` or `#ffffff`, text `#111111`, secondary `#555555`, rule `#cccccc`, one ink colour for links and the main data series `#1f4e9c`, a second series colour `#b5462b`. Plot backgrounds white, gridlines `#e5e5e5`.
- **Type**: 17–19px serif body, section headings numbered the way papers do ("2 Method", "2.1 Gauge model") in normal case, not caps.
- **Shape**: 0 radius, no shadows, no panels; content separated by white space and thin rules.
- **Habits**: figures with numbered captions ("Figure 1. Rain rate and cumulative depth for a 60 s storm."), parameters shown as a table with units in their own column, equations or formulas inline, side notes in the margin, a short abstract-style summary at the top.

## Instrument panel
Inspired by Dieter Rams-era Braun hardware and lab equipment front panels. A light, tactile alternative to the neon HUD for device and audio tools.
- **Fonts**: `"Helvetica Neue", Arial, sans-serif` or Archivo; numeric readouts in a tabular-figure sans (`font-variant-numeric: tabular-nums`), not neon mono.
- **Colours**: body `#e9e7e2`, panel `#f6f5f1`, text `#1d1d1b`, secondary `#6b6a66`, engraved line `#c9c6be`, one signal orange `#e3540f` for the main action and "on" states, green `#3c7d3a` for OK, readout window `#2b2b28` with off-white digits `#f2efe6` (no glow).
- **Type**: small, sentence-case labels printed above controls like silkscreen; units always shown.
- **Shape**: 6px radius on controls, 10px on panels; controls look pressable (1px darker bottom border), panels are flat.
- **Habits**: controls grouped on panels like a real device; a single accent colour; round knob-like sliders or plain range inputs styled in grey; readouts in a recessed dark window, numbers only.

## Plain web
The early, unstyled web done on purpose. Good for small tools, personal sites and docs.
- **Fonts**: `Georgia, "Times New Roman", serif` or the browser default; code in the default monospace.
- **Colours**: background `#ffffff`, text `#000000`, link `#0000ee`, visited `#551a8b`, rule `#888888`.
- **Type**: 16–18px, max width 70ch, headings bold and close to body size.
- **Shape**: native form controls, unstyled buttons, `<hr>` rules, `<table border>` for data.
- **Habits**: a single column, real headings and lists, no cards, no icons, no animation.

---

## Applying a theme
1. Put the theme's tokens in `:root` (or the framework theme file) under semantic names: `--color-bg`, `--color-text`, `--color-accent`, `--radius`, `--font-body`, and so on.
2. Delete any colour, radius or shadow value in the code that is not a token.
3. Build components following the theme's "Habits" line.
4. If the user asked for dark mode, use the theme's dark tokens. If the theme has none, darken the surfaces to warm or neutral greys (`#1b1b1b`, `#262626`), keep the same accent at lower saturation, and never add glow.
