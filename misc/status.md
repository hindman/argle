# Status

Last updated: 2026-10-16

## Done

- Started the work of breaking `notes.txt` into smaller, more focused files.

      notes.txt

      status.md
      road-map.md
      dev-notes.md

      spec-syntax.md
      spec-examples.md
      terminology.md
      classes.md

- Resolved a review of spec-syntax issues. Decisions:
    - Quantifier ranges: `{m-n}`, `{m}`, `{m+}`; non-negative integers. The
      old regex-style `{m,n}` is gone (comma reserved for future use).
    - Markers appear once: `section` is `any-section-title ::`;
      `section-scope` is just `query-path`.
    - Section titles are required (the usage-section is the only untitled
      section; its display title defaults to "Usage").
    - Bundled flags (`-abc`) are not spec syntax, but end-user argument
      parsing must support them.
    - Named groups display in usage text with angle brackets:
      `[<general-options>]`.
    - Prog name is not part of the spec; it is an API attribute, inferred
      from the script name by default.
    - Variant vs opt-spec: variants are parsed greedily at the start of the
      usage-section; a trailing colon marks an opt-spec that could otherwise
      be read as a variant. Continuation lines must be indented more than the
      first line and be contiguous.
    - Choices: in a variant they make a literal input that selects the
      variant (one or many choices, same mechanism); in an opt-spec they
      configure the Opt's choices.
    - Variants are never quantified; repetition is done by wrapping a
      partial in a quantified group (see neck-diagram, nab).

## Next candidates

Planned order: env setup, then `notes.txt`, then the code assessment.

- First step on restart (Monty): create a fresh `argle-3.14.8` virtualenv
  (the old `argle-3.9.4` is out of date). Then verify with `pytest tests` and
  `misc/scripts/spec-check tests/data/specs/blort.txt -t`. Open questions:
  whether to include `mhutils`; whether to add `pyperclip` (used by
  `misc/scripts/`) to the `dev` extras in `setup.py`.

- Continue extracting and organizing the remaining `notes.txt` sections.
  Do this before the code assessment, so our conceptual understanding is
  solid first.

- Decide whether to continue from the existing `src/argle/` code or restart.

- Examine the material under `misc/examples/` to decide what we keep vs move
  to `misc/archive/`. Defer until more of `notes.txt` is processed and the
  overall vision is clearer. (spec-vs-api was once labeled archival, but the
  basis for that is unknown.)

