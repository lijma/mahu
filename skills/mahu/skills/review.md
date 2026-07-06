# Mahu Review Subskill

Use for publishing artifacts, collecting reviewer feedback, reading comments,
resolving comments, and creating review loops.

Owner: `floop-client`.

## Prerequisites

Required CLI: `floop`

Check before execution:

```bash
floop --help
# or
mahu doctor --subskill review
```

Install if missing:

```bash
pip install floop
```

If `floop` is missing and you do not have permission to install packages, stop
and ask the user. Do not manually zip/upload review artifacts without
floop-client unless the user explicitly asks for a planning-only fallback.

## SOP

1. Identify the local floop project and intended floop-server project.
2. Run `floop projects --json-output`.
3. Verify the local project has the correct `serverProject` binding.
4. If missing or wrong, run `floop review set --project <project>`.
5. Create a local version container with `floop versions create`.
6. Let the artifact owner copy files into the version directory.
7. Verify the entrypoint exists.
8. Upload with `floop review upload --project <project> --version <version> --json-output`.
9. Treat upload as successful only if `shareUrl` exists.
10. Fetch comments with `floop comments --project <project>`.
11. Route fixes to fppt, fdesign, testboat, or floop-client.
12. Resolve only comments that were actually addressed.

## Guardrails

- `.floop/floop.env` is not a project selector.
- Do not upload unvalidated artifacts.
- Do not upload an empty version.
- Do not resolve comments before the fixed version is published.
