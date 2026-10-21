
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

  99. Trim "## opt-spec" in spec-syntax.md to essentials. It is becoming
      policy dicussion, not a syntax doc.

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

- opt-spec [MATERIAL DROPED FROM spec-syntax.md]

  - Determining the parent(s):

    - If non-empty scope:

      - Parent(s) are the matching Opts from the variants.

      - Purpose of the marker: connect opt-spec configuration to Opts declared
        in variants.

    - If empty scope:

      - Purpose: configure the parameters or choices of the nearest Opt above,
        and state the presentation order for those items in the generated help
        text.

      - Parent: the immediately preceding opt-spec that does not itself have
        an empty scope. Anything else in between (heading, block-quote)
        breaks the run.

      - The child must match the parent's Opt or an element within it.
        Matching works as for any opt-spec:

        - Same name and kind.
        - Scope agreement.
        - Child's configuration must be additive.
        - See opt-independence.
        - In practice, the child will be:
            - Parameter (parameter-specific help text).
            - Choice of a Positional/Parameter (declaring a choice and/or help
              text for it).

    --------
    opt-spec-scopes: Opt-spec scopes
    --------

    Two kinds of scope, two purposes:

        - Non-empty scope: disambiguation.
            - Connects opt-spec configuration to the correct Opts declared
              in the variants, when several Opts share a name.
            - A section-scope is shorthand for applying the scope to every
              opt-spec in the section.

        - Empty scope: help-text layout.
            - Configures a Parameter or choice of the parent opt-spec.
            - Opt-descs display children nested under their parent, in
              spec order.

    Non-empty scope:

        - The scope is a query-path, so it can match multiple Opts.

        - Example: -x Opts needing different help text, by index.

            --foo [-x] | --bar [-f] [-x] | --blort [-x]

            x.2 >> [-x] : blah x-for-blort
            x.0 >> [-x] : blah x-for-foo
            x.1 >> [-x] : blah x-for-bar

        - Example: --point in two variants, with shared and distinct
          parameter help.

            var1 >> --point <x> <y> <z> : help-text1
            var2 >> --point <x> <y>     : help-text2
            point >> <x>                : help-text3 (both)
            var1 >> <y>                 : help-text4
            var2 >> <y>                 : help-text5

        - No match: error.

    Empty scope:

        - Parent: the immediately preceding opt-spec that does not itself
          have an empty scope.

        - Children of one parent are contiguous. Siblings stack, and nested
          children work too:

            --mode <speed=fast|slow> : Blah mode
            >> <speed>               : Blah mode-speed
            >> <speed=fast>          : Blah mode-speed-fast
            >> <speed=slow>          : Blah mode-speed-slow

        - Anything else in between (heading, block-quote) breaks the run.

        - The child must match the parent's Opt or an element within it,
          using the usual matching rules (see opt-independence). No match:
          error.

        - Singular by construction: one parent per child.

        - In practice the child is:
            - A Parameter of an Option (parameter-specific help text).
            - A choice of a Positional or Parameter. A child can add a
              choice (additive), not just document an existing one.

        - Why so strict: the opt-desc layout. A child separated from its
          parent would either be moved under the parent in the generated
          help text or appear out of place. Either way, the spec and the
          output would diverge.

    Unscoped opt-specs and Parameters:

        - An unscoped <x> matches Positional(x) Opts, not Parameters.
          Parameters are reached through a scope (empty or non-empty).

    Rejected alternatives (2026-10 spec-syntax review):

        - "Parent: preceding non-scoped opt-spec." The original wording.
          In a scoped section every opt-spec is scoped, so no parent could
          exist. Fixed by "not itself having an empty scope."

        - Nearest preceding matching opt-spec (search backward, skipping
          non-matches). More forgiving, but it lets children stray from
          their parent, which scatters the opt-desc layout.

        - Plural matches for empty scopes. Not needed: a non-empty scope
          is a query and already matches several Opts (see --point above).

        - Limiting the parent search to the same section. Moot under the
          strict rule. Scope agreement would have prevented cross-section
          mismatches anyway.

    Use case considered: documenting choices in their own section.

        --format <fmt=json|yaml|csv> : Output format

        format >> Formats ::
            <fmt=json> : Blah json
            <fmt=yaml> : Blah yaml

        - An empty scope cannot do this (the children are not adjacent).
          A section-scope can, and makes the connection explicit.

Two things in it I'm not certain about:

- In the `--point` example, `point >> <x>` assumes a scope query by an
  Option's name finds that Option and the child then matches its Parameter.
  That fits the query rules as I understand them, but we haven't settled it.

- The Formats example puts unscoped `<fmt=json>` lines under a section scope.
  That relies on the section scope letting them reach Parameter `fmt`,
  consistent with the "Unscoped opt-specs and Parameters" bullet.

Should I add the section, and make the two fixes to the spec-syntax text above?

