# {{PROJECT_NAME}} — Roadmap

**Status: planning, not a spec.** This is the standing, ordered plan of what gets built next. Each lettered step becomes its own `/flow plan` session and its own `docs/specs/<feature>.md`. Nothing here is implementation-ready as written.

**How this doc works.** It's append-only in spirit: finished steps stay, marked ✅ DONE and pointing at the spec that is authoritative for what actually shipped. New work is added as a new lettered step (continue the letters — they're labels, not an order; the order is the diagram below). Anything measured goes under *Verified facts* with the date it was measured, so a later session can trust it or re-measure it deliberately. Loose ideas that aren't commitments yet live in `feature_ideas.md` beside this file.

---

## Spec index

What each spec in `docs/specs/` actually covers, and the code it's authoritative for. This table exists so "which spec introduced X?" is a lookup rather than a re-derivation.

**Every new spec gets a row here as it is written** (the Plan phase's second commit). Verify corrects the row if what shipped differs.

| spec | scope | primary code | step |
|---|---|---|---|

---

## Verified facts

Measurements a later session should trust rather than re-derive — each under a dated subsection. Don't trust a number that contradicts one of these without re-measuring it deliberately.

---

## Order

```
(no steps yet)
```

**Nothing has landed yet.** <!-- Verify keeps this line current: "A, B and C have landed — …" -->

Reasoning about the order — dependencies, what gates what, what can be picked up on a day something else is blocked — goes here, below the diagram.

---

<!--
Step section shape. Copy for each new step; the letter is a label, not an order.

## X — Short title

**Not specced.** Own `/flow plan` session.

What it is and why, the decisions already made, anything measured (dated), and the traps already known.

When it lands, Verify rewrites the header and first line as:

## X — Short title ✅ DONE

**Specced → `docs/specs/<feature>-X.md`.** That spec is authoritative; the summary below is the shape, not the detail.
-->

---

## Cross-cutting notes

Things true across many steps that don't belong to any one of them.
