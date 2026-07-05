# Mahu Prototype Subskill

Use for apps, websites, UI flows, product prototypes, design systems, journeys,
tokens, components, and responsive HTML experiences.

Owner: `fdesign`.

## Prerequisites

Required CLI: `fdesign`

Check before execution:

```bash
fdesign --help
# or
mahu doctor --subskill prototype
```

Install if missing:

```bash
pip install fdesign
```

If `fdesign` is missing and you do not have permission to install packages,
stop and ask the user. Do not hand-roll fdesign workspace files or validation
logic.

## SOP

1. Understand the current product/user flow.
2. Check or create the fdesign project.
3. Update tokens only when the design needs new reusable values.
4. Update sitemap and journey map as understanding grows.
5. Check or extend components before page generation.
6. Build plain responsive journey HTML.
7. Run fdesign validations and `fdesign journey check`.
8. Preview and ask the user for feedback.
9. Snapshot approved versions when the user is satisfied.

## Guardrails

- Do not hardcode design values when tokens exist.
- Do not embed device shells inside journey HTML.
- Do not treat a prototype as complete until fdesign checks pass.
- For review upload, finish prototype validation first, then load `skills/review.md`.
