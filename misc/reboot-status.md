
<!--

  # reboot-status: Status of project reboot
  # active-files: Most active files
  # todos: TODOs
  # whitespace-rules: SPEC_ISSUE: re-assess the whitespace rules in spec-syntax
  # digit-short-opts: SPEC_ISSUE: first-char spec does not allow short options like `-1`
  # conflict-quantifiers: SPEC_ISSUE: variant vs opt-spec conflicts: quantifiers
  # opt-spec-conflicts: SPEC_ISSUE: conflicts among opt-specs
  # conflict-parameters: SPEC_ISSUE: variant vs opt-spec conflicts: parameters
  # conflict-choices: SPEC_ISSUE: variant vs opt-spec conflicts: choices

-->

# reboot-status: Status of project reboot

The road-map.md file is the project's main status and TODO file.

This reboot-status.md file is focused on rebooting the Argle project after a long
delay. We are using it to get Monty's brain back up to speed and Claude Code's
understanding up to snuff. In the process, we are also reorganizing the
documentation and policy documents a lot.

# active-files: Most active files

    reboot-status.md
    policies.md
    scenario-mockups.md
    spec-syntax.md
    notes.txt

# todos: TODOs

- Edit policy-clarifications.md:
  - See __HERE__ and the file's TODOs.

- Create scenario-mockups.md

- Address other spec-syntax issues (see SPEC_ISSUE).

- Add IDs to all headings in the new .md files.

- Flesh out the `Opt.spec` attribute. What does it contain?

- Conduct another full review of the spec-syntax to spot any problems, gaps,
  lack of clarity, etc. That last review raised several important issues, so
  we'll keep repeating the review process until we stop finding crucial stuff.

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

# whitespace-rules: SPEC_ISSUE: re-assess the whitespace rules in spec-syntax

Pushing toward further relaxation, I think we still have some overly strict
rules that lack a strong rationale.

Pushing the other way, one of our whitespace examples (ipconfig or ifconfig?)
used a `KEY VALUE` style where the keys functioned basically as options
without the `--` prefix. One of Argle's future goals will be to allow users to
set the option-prefixes (defaults are `-` and `--`). Conceivably, an
ifconfig-style use case would want a prefix of empty string, right? Is
supporting that type of use case a situation where we might want to tighten
the whitespace rule for named-groups?

# digit-short-opts: SPEC_ISSUE: first-char spec does not allow short options like `-1`

Current code: `short_option` is `-` followed by `\w`, so the lexer already
accepts `-1`. It also accepts non-ASCII letters, since Python's `\w` is
Unicode-aware. Only the doc is out of step.

Suggested doc change for bare-option:

      - first-char
      -- valid-name

      - Where first-char here is a letter, digit, or underscore.
      - An Opt needs a valid name/dest. A digit short option like -1 is
        fine as long as the Opt also has a long form.

Two follow-ons to decide:

  - Should `\w` become `[A-Za-z0-9_]`, to match the ASCII-only valid-name?

  - At parse time, `-1` collides with negative-number arguments (argparse's
    long-standing headache). If digit short options are allowed, we need a
    policy for how `-1` vs a negative value is read at end-user parse time.
    That's not a spec-syntax issue, but it should go on the TODO list.

