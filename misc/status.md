# Status

Last updated: 2026-10-09

## Done

- Extracted `spec-syntax` and `syntax-examples` sections into
  `misc/spec-syntax.md` and `misc/spec-examples.md`.

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

- Extract `terminology` (likely `misc/glossary.md`) and
  `classes-and-attributes` (`misc/classes.md`; drop `Variant.ntimes`) from
  the Specification section of notes.txt.

- Then survey the remaining notes.txt sections (`argle-notes` at the top,
  `discussion`, `reference`) and decide what to extract.

- Decide whether to continue from the existing `src/argle/` code or restart.
