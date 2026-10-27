
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

# conflict-quantifiers: SPEC_ISSUE: variant vs opt-spec conflicts: quantifiers

Table of relevant attributes:

      Attribute  | Positional | Option | Parameter
      -------------------------------------------------
      spec       | Y          | Y      | Y
      name       | Y          | Y      | Y
      aliases    | .          | Y      | .
      help       | Y          | Y      | Y
      choices    | Y          | .      | Y
      -------------------------------------------------
      Q.m        | Y          | Y      | Y
      Q.n        | Y          | Y      | Y
      Q.required | Y          | Y      | Y
      Q.greedy   | Y          | Y      | Y

Preliminary analysis:

  - Q.m and Q.n. A conflict here is possible, at least in a strict sense. For
    example, `<x>{2-3}` in a variant and `<x>{2-4}` in an opt-spec. One could
    try to be cute and allow opt-spec configuration that *expands* the allowed
    universe (vs contracting it). But this business is making me feel queasy.

  - Q.greedy. Similar logic here. If the config from a variant says nothing
    about greediness, so the Opt assumes its Quantifer is greedy (the
    default), and if the opt-spec then adds non-greedy, how does Argle react?
    In one sense, the latter configuration is "additive" (the question mark
    was "added"), but in another sense the allowed universe of acceptable
    end-user inputs got smaller.

  - Q.required. Similar concerns here. If we allow variant and opt-spec to
    differ on this attribute, can the difference go in both directions
    (required to non-required, and vice verse) or only one way?

  - An opt-spec, by itself, cannot fully convey the quantifier-related
    attributes of an Opt because some of those characteristics come from
    parent containers (eg, `[-a -b]`). This seems to push towards treating
    quantification generally as most authoritative in the variants (if any)
    and somewhat optional in opt-specs.

# opt-spec-conflicts: SPEC_ISSUE: conflicts among opt-specs

This arose out of the variant-vs-opt-spec work. What if opt-specs conflict
among themselves (eg `-i --ignore-case` and `-i --invert`)? Maybe this problem
will go away or change if our tentative embrace of full opt-independence is
realized.

Could we deal with this problem by somehow enforcing a kind of uniqueness
among the opt-specs? Is there ever a use case for two opt-specs to "match" the
same Opts? Here match is similar to the matching logic for connecting
opt-specs to the correct variant Opt(s). But similar criteria could also be
used to make sure that -- in the case of an opt-specs-only spec file -- two
separate Opts don't resolve to the "same thing".

# conflict-parameters: SPEC_ISSUE: variant vs opt-spec conflicts: parameters

What about opt-specs that completely change the parameters of an Option?

    --bar <b1> <b2>        # In a variant
    --bar <b1> [<b2>]      # In an opt-spec
    --bar <x> <y> <z>      # Ditto -- but more divergent

# conflict-choices: SPEC_ISSUE: variant vs opt-spec conflicts: choices

A merged Opt can have separate positions in the grammar:

  - `<action=pitch> <action=balk|stop>` is one merged Opt occupying two
    positions. The Opt data model lacks the positional attributes to keep
    track of this under the prior policy of unifying Positionals having
    choices.

  - That concern is now pushing us toward a fuller embrace of opt-independence
    and instead trying to support the things drove us toward unification via
    other strategies (eg in usage/help text, arg-parsing error reporting,
    etc).

Some things that motivated unification of Opts with choices in the first place:

  - Unified help entry for a subcommand positional.

  - Behaviroal consistency among different ways of writing the same grammar.
     - In separate variants: `<step=start>` and `<step=stop>`.
     - In one variant: `<step=start|stop>`

  - Error messages that list valid choices.

  - Even if Argle perceives Opts as fully independent, users might not. For
    example, they might call get(), thinking that they will be configuring a
    single unified Opt (due to its choices), but internally Argle will think
    that the arg-variant choices (as one kind of example) are all independent.

Current work on this issue:

  - Policies: misc/policy-clarifications.md
  - Scenario mockups: misc/scenario-mockups.md

