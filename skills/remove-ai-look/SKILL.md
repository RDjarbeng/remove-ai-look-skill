---
name: remove-ai-look
description: Eliminate the generic, templated "AI-generated look" from web frontends. Strip stock framework defaults, purple-blue gradient heroes, cookie-cutter card grids, and hollow marketing boilerplate whenever building, restyling, or reviewing a frontend—including landing pages, marketing sites, dashboards, app UIs, and web components. Activate when a user complains that a page looks generic, cookie-cutter, robotic, templated, or "like ChatGPT made it", or demands intentional, bespoke design with character. Do not use for backend tasks or standalone charts.
---

# Remove AI Look

## Why This Happens
Generative models output the statistical average of public repositories, which means they churn out the default settings of popular CSS frameworks and component libraries. What users call the "AI aesthetic" is not machine imagination; it is simply unconfigured scaffolding. Asking a model to "be creative" produces superficial variations. To genuinely break the pattern, strip the framework defaults directly out of your build configuration so uncurated tokens cannot compile.

## Precedence
Follow this hierarchy when styling any interface:
1. Direct user instructions and explicit preferences always take top priority.
2. An established brand identity or existing project design system comes second.
3. This skill applies third to prevent default creep.

When a user requests a broad direction, such as a blue theme, honor that choice by engineering a distinct, bespoke blue palette rather than falling back onto a vendor default like Tailwind `blue` or `indigo`. Never apply this skill by swapping one fashionable default for another stock clone.

## Workflow
Follow these sequential steps on any frontend task:

1. **Audit first**: Run `python scripts/check_ai_defaults.py <path>` from the skill folder to identify telltale defaults and stock copy across the project, and inspect every reported finding.
2. **Commit to a written vocabulary**: Before authoring styles, define a compact token set:
   - A cohesive palette constructed around a chosen base hue rather than standard utility presets.
   - A deliberate typographic pairing specifying line heights and letter spacing.
   - A uniform corner radius and elevation rule applied consistently across the entire site.
   - A singular layout concept customized specifically to this page.
3. **Enforce it at the source**: Replace the framework theme instead of extending it. Overriding the default palette completely ensures that stock utility tokens trigger build failures if used. Define component variants once in shared abstractions to prevent ad-hoc inline styling drift.
4. **Disrupt standard page rhythm deliberately**: Break away from predictable section stacking only where the content genuinely justifies it. Usability remains paramount: an operations dashboard, portal, or productivity tool must remain scannable, dense, and intuitive rather than become an art experiment.
5. **Audit copy aloud**: Read every heading and paragraph out loud. Cut stock marketing verbs (such as "empower", "unlock", "transform") and two-abstract-noun headings (such as "Seamless Integration"). Require at least one concrete, verifiable claim or specific metric.
6. **Enforce continuity**: Lock the design in place with a custom linter rule or CI workflow check that flags banned class patterns and catches regressions before review.

## Fingerprints to Eliminate
Scan for and remove these common markers:
- Stock accent colors: framework indigo, violet, purple, and slate.
- Purple-to-blue or purple-to-pink gradient hero backgrounds.
- Monotonous structural sequences: full-width hero, followed by three identical icon cards, followed by a three-tier pricing table, followed by an accordion FAQ.
- Oversized border radii (`rounded-2xl`, `rounded-3xl`) combined with diffuse drop shadows (`shadow-lg`, `shadow-xl`) on every container.
- A single sans-serif typeface (such as Inter) applied to both headings and body at default tracking and line height.
- Uniform center-aligned layouts across every block.
- Vacuous marketing prose and placeholder taglines.

## Guardrails
- **Maintain accessible contrast**: Ensure text and interactive controls strictly meet WCAG AA contrast standards regardless of the custom palette chosen.
- **Keep keyboard focus visible**: Never remove focus rings or compromise keyboard navigation.
- **Support both themes intentionally**: When the project requires light and dark themes, design both states with purpose rather than relying on automated color inversion.
- **Clarity over novelty**: Never sacrifice usability, responsiveness, or readability for visual eccentricity.

## Credit
Based on ideas from the article ["How to fix the 'AI-generated' look in your frontend"](https://dev.to/alanwest/how-to-fix-the-ai-generated-look-in-your-frontend-1ahh) by Alan West.

Made by [rdjarbeng.com](https://rdjarbeng.com/about/) by [RDjarbeng](https://github.com/RDjarbeng)
