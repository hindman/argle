# Argle

A command-line argument parser for Python. The grammar is configured mainly
through a text "spec" based on familiar usage syntax (variants, opt-specs,
groups, alternatives, quantifiers), with a programmatic API for everything else
(convert, validate, dispatch, defaults, help-text layout).

Collaboration model: Claude writes most of the code; Monty guides the design
and may be more hands-on with the Python than usual.

## Sources of truth

In priority order:

- `misc/spec-syntax.md`: the spec grammar. Authoritative.

- `misc/spec-examples.md`: index of example programs, plus the example files it
  points to under `misc/examples/` (blort.py is the most thorough). Authoritative.

- `README.md`: vision and motivation. Mostly accurate, but it is a planning
  doc and will be rewritten after v1. Defer to the spec docs where they differ.

- `misc/notes.txt`: large legacy notes file, mix of current and outdated
  material. Useful for "why" questions (the discussion sections record
  rejected approaches). Being decomposed (see below).

- `src/argle/`: code left mid-work (most recent work was spec parsing). Not
  authoritative. We may continue from it or restart; TBD. Don't fix it
  unless asked.

Archival, ignore unless asked: `misc/archive/`.

## Decomposing notes.txt

- Move material out of `misc/notes.txt` into topic .md files under `misc/`.

- Never delete from notes.txt. When a section is copied out, add a paragraph
  `COPIED_OUT: misc/<file>.md` at the top of that section in notes.txt.
  Monty will delete notes.txt himself once decomposition is done.

- Copy verbatim first (formatting-only changes are fine). Content edits come
  afterward as separate steps, so the original stays comparable.

- .md style: wrap at ~80 columns; no bold/italics; headings, lists, and
  4-space-indented blocks for syntax (not fenced code, which blurs with the
  spec syntax visually).

## Current status

See `misc/status.md` for what has been done, decisions made, and next
candidates. Read it at the start of a session; update it as work lands.

## Tooling

- Tests: `pytest tests` (spec-parser tests use `tests/data/specs/` and
  `tests/data/exp/`). `tasks.py` has invoke tasks (`inv test`, `inv tags`).

- Git is read-only for Claude; Monty does all commits.
