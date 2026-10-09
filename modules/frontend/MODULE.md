# Module: frontend

**Applies when** the project has a user interface someone looks at (web pages, a desktop UI, a device screen). Not for a headless bridge, CLI or library.

## What setup asks
- **Do looks matter here?** Either a personal tool where function beats form, or something Finn wants to look good.
- If looks matter: any design system or CSS framework, and any look Finn is after. Never pick one for him.
- Whether counts and numbers are rendered both server-side and updated live (the thousands-separator rule only bites when both exist).

## What it adds
A `## Frontend` section at the `flow:modules` marker in CLAUDE.md, built from the bullets below — the first bullet is one of the two variants, the rest apply to both.

- Function over form: "- **Function over form.** This is a personal tool; a plain page that does everything I want beats a pretty, half-finished one. Don't spend effort on visual polish unless I ask."
- Looks matter: "- **Looks matter here.** {{DESIGN_DIRECTION, as Finn stated it}}. Keep new UI consistent with what's already there rather than inventing a fresh style per page; ask before introducing a new visual pattern."
- "- **Never let red vs green alone carry meaning.** I'm red-green colourblind (deuteranomaly), so a red/green pair reads as one colour to me. Pair colour with an icon, label, shape or position, and prefer palettes that separate on blue/orange or on lightness."
- "- **Any count that can exceed 999 renders with thousands separators**, on both halves of the path — where it's rendered server-side and wherever script updates it live. Getting only one half is the failure mode to watch for: it silently strips or adds commas on the first live update, and it has happened in both directions."
- "- **A count in prose is rendered from the data, or it isn't stated.** A page once claimed \"the 36 playlists\" while the table held 37 — wrong silently, and nothing could have caught it. Either render the number or write the sentence without one."
- With a CSS framework: "- **{{FRAMEWORK}} is the design system**, {{vendored under … / loaded from …}}. Its defaults are the guide; local decisions are recorded in the spec that made them, not in a separate style guide. Our own stylesheet loads *after* the framework and holds only what is genuinely this project's."
- With a CSS framework that exposes custom properties: "- **Override the framework by feeding its CSS custom properties, never by out-specifying its selectors.** A colour *declared* on an element beats one *inherited* from its parent at any specificity, so a parent-level rule that looks correct can silently do nothing; feeding the variable the framework already reads wins with no fight and stays theme-aware."
