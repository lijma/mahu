# Mahu Presentation Subskill

Use for decks, slides, PPT, HTML presentations, talks, training, and narrative
communication.

Owner: `fppt`.

## Prerequisites

Required CLI: `fppt`

Check before execution:

```bash
fppt --help
# or
mahu doctor --subskill presentation
```

Install if missing:

```bash
pip install fppt
```

If `fppt` is missing and you do not have permission to install packages, stop
and ask the user. Do not replace fppt with ad hoc deck generation unless the
user explicitly asks for planning-only output.

## SOP

1. Capture topic, audience, goal, must-cover points, and density preference.
2. Ask the user to approve the MECE outline before full slide generation.
3. Ask the user to choose theme direction or provide a custom theme prompt.
4. Let AI fill slide content after outline approval.
5. Use diagrams, charts, code/demo blocks, and visual hierarchy when useful.
6. Build authored HTML presentation UI, not a toy manifest renderer.
7. Validate deck YAML and check rendered presentation behavior.
8. Iterate on user feedback through the same validate loop.

## Guardrails

- Do not make every slide from a generic template.
- Do not put speaker prompts into end-user slide content.
- Do not skip rendered UI checks after AI-authored presentation changes.
- For review upload, finish fppt checks first, then load `skills/review.md`.
