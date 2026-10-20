
<!--

# reboot-status : Status of project reboot
# TODOs
# Temp work area
# reboot-status : Status of project reboot
# TODOs
# spec-syntax-remaining-issues
# Temp work area

-->

# reboot-status : Status of project reboot

The road-map.md file is the project's main status and TODO file.

This status.md file is focused on rebooting the Argle project after a long
delay. We are using it to get Monty's brain back up to speed and Claude Code's
understanding up to snuff. In the process, we are also reorganizing the
documentation and policy documents a lot.

# TODOs

- Deal with spec-syntax-remaining-issues (below).

- Create a `argle-3.14.8` virtualenv (the old `argle-3.9.4` is out of date).
  Then verify with `pytest tests` and `misc/scripts/spec-check
  tests/data/specs/blort.txt -t`. Open questions: whether to include
  `mhutils`; whether to add `pyperclip` (used by `misc/scripts/`) to the `dev`
  extras in `setup.py`.

- Continue extracting and organizing the remaining `notes.txt` sections into
  smaller, more-focused markdown files. Do this before the code assessment, so
  our conceptual understanding is solid first.

- Usage text: define its rules in one unified place. The current material is
  scattered across `notes.txt`, the mock-ups, and spec-syntax. Subtopics
  include how named groups display (the mock-ups show them as compact
  placeholders like `[<general-options>]`), choices and arg-variants,
  anonymous inputs, layout and wrapping, and auto-generated headings.

- Examine the material under `misc/examples/` to decide what we keep vs move
  to `misc/archive/`. Defer until more of `notes.txt` is processed and the
  overall vision is clearer. (spec-vs-api was once labeled archival, but the
  basis for that is unknown.)

- Assess the code base. Figure out which behaviors are implemented or not.
  Decide whether to continue from the existing code or restart fresh.

# spec-syntax-remaining-issues

Remaining issues from latest spec-syntax review:

  8. An empty opt-scope inside a scoped section. A section-scope means "apply
     the scope to all opt-specs in the section." An empty `>>` takes as its
     parent the preceding non-scoped opt-spec. In a scoped section, every
     opt-spec is scoped, so that preceding opt-spec doesn't exist. Either the
     empty scope ignores section scoping, or it's an error. Say which.

  11. `query-elem`: the note says "positive integer," but `digit...` allows 0.
      What an integer query-elem means (an index?) is never explained.

  13. Asymmetry: parameters have a `< choices >` form, but positionals don't.
      This is presumably on purpose, since a positional needs a name for its
      dest, but one line saying so would help.

  14a. The whitespace rule for `=` covers named groups but not `<name=choices>`.

  14b. Whether whitespace is allowed before the non-greedy `?` isn't stated.

  14c. `-1` style short options are excluded by `first-char`, without comment.

  15. Opt-spec vs variant quantity conflict. If a variant declares an Opt as
      required and an opt-spec declares it optional (or vice versa), does the
      opt-spec's quantity win, or is a mismatch an error? Can an opt-spec set
      quantity at all for an Opt already declared in the variants?

# Temp work area

