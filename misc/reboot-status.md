
<!--

# reboot-status : Status of project reboot
# Most active files
# TODOs
# spec-syntax-remaining-issues
# Variant vs opt-spec conflicts: draft policy
# Temp work area

-->

# reboot-status : Status of project reboot

The road-map.md file is the project's main status and TODO file.

This status.md file is focused on rebooting the Argle project after a long
delay. We are using it to get Monty's brain back up to speed and Claude Code's
understanding up to snuff. In the process, we are also reorganizing the
documentation and policy documents a lot.

# Most active files

    reboot-status.md
    spec-syntax.md
    notes.txt

# TODOs

- Deal with spec-syntax-remaining-issues (below).

- Add IDs to all headings in the new .md files.

- mhtags: get script working.

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

# spec-syntax-remaining-issues

41. Opt-spec vs variant quantity conflict.

  - In progress: see below.

42. The first-char spec does not allow short options like `-1`:

  - Current code: `short_option` is `-` followed by `\w`, so the lexer already
    accepts `-1`. It also accepts non-ASCII letters, since Python's `\w` is
    Unicode-aware. Only the doc is out of step.

  - Suggested doc change for bare-option:

        - first-char
        -- valid-name

        - Where first-char here is a letter, digit, or underscore.
        - An Opt needs a valid name/dest. A digit short option like -1 is
          fine as long as the Opt also has a long form.

  - Two follow-ons to decide:

    - Should `\w` become `[A-Za-z0-9_]`, to match the ASCII-only valid-name?

    - At parse time, `-1` collides with negative-number arguments (argparse's
      long-standing headache). If digit short options are allowed, we need a
      policy for how `-1` vs a negative value is read at end-user parse time.
      That's not a spec-syntax issue, but it should go on the TODO list.

43. Re-assess the whitespace rules in spec-syntax.

  - Pushing toward further relaxation, I think we still have some overly
    strict rules that lack a strong rationale.

  - Pushing the other way, one of our whitespace examples (ipconfig or
    ifconfig?) used a `KEY VALUE` style where the keys functioned basically as
    options without the `--` prefix. One of Argle's future goals will be to
    allow users to set the option-prefixes (defaults are `-` and `--`).
    Conceivably, an ifconfig-style use case would want a prefix of empty
    string, right? Is supporting that type of use case a situation where we
    might want to tighten the whitespace rule for named-groups?

# Variant vs opt-spec conflicts: draft policy

Key policy goals/decisons and findings:

  - P1. We do want an opt-spec to be able to add aliases or a long-name for an
    Option. That's handy, it allows the user to have super readable variants,
    and even the README does it.

  - P2. We do want to support per-choice help text. That's a feature I have
    wanted many times as a long-suffering argparse user.

  - P3. We do want opt-specs to be able to add parameters to an Option. This
    is similar to P1 because it allows for a compact/readable command-line
    grammar, leaving the fleshing out to opts-specs.

  - P4. At the level of an individual Opt, it's impossible to fully specify
    quantity/required correctly in an opt-spec because those attributes can
    derive from parent containers in the command-line grammar.

  - P5. Per-choice help text must be done via sub-specs. Applies to both
    parameters (the old policy) and now positionals (the new policy to make
    things consistent and to ensure that this help text has sufficient
    context for end-users). See the edit-list we assembled below.

  - P6. If a variant declares choices for a VarInput, they are authoritative.
    Opt-specs (regular or sub-spec) may name only those choices; naming any
    other is an error. Not every choice needs to be documented. If the variant
    declares no choices, the opt-specs supply them.

Name and aliases:

  - Options:

    - Matching: an opt-spec matches a variant Option if the variant's form (eg
      `-i`) is any of the opt-spec's option strings.

    - The opt-spec is authoritative for names. The matched Option takes its
      full set of names from the opt-spec. Indeed, a variant has no way to
      supply more than one name.

    - The last bare-option is the Opt's name (and supplies its default dest).
      The others are aliases. Rationale: the form closest to the parameters
      reads as the most important, and the typical short-then-long ordering
      makes the long form the name.

          -x --blort --fubb <a> <b> : Fubb help text # Name: fubb.

    - Aliases can be short or long (an alias is any bare-option). Real
      programs have long aliases too (eg GNU tar: `-x, --extract, --get`).

    - No variant-vs-opt-spec conflict is possible regarding names. If the
      variant's form is not among the opt-spec's option strings, the opt-spec
      does not match that Option. The variant states only one form, so it has
      nothing else to contradict.

    - Ordering of aliases and the option name in the spec syntax is somewhat
      independent of ordering/presentation in generated help text (the latter
      will be configurable in at least a couple of ways).

  - Positionals:
    
    - The name is the match key and there are no aliases, so an opt-spec
      cannot rename a positional, nor can there be variant-vs-opt-spec
      conflict as it relates to names.

# Temp work area

Issues to be decided:

  - choices [see below]

    - might be done. Check to see if any choice issues lack a resolution.

  - quantifier [see below]

  - Two opt-specs claiming the same Option with different names (eg `-i
    --ignore-case` and `-i --invert`): opt-spec vs opt-spec, not vs variant.
    Leaning: error.

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

Analysis of quantifier:

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

----

Analysis of choices:

  - Under current policy (assuming it survives our evaluation of the topic at
    hand), an Opt with choices is unified by Argle as the variants and
    opt-specs are processed. So, one might think that everything is smooth
    sailing here, because it's all inherently "additive". A happy-path example
    might be a case where the variant simply declares an Opt and the opt-specs
    flesh it out, including defining the choices.

        # From a variant.
        <fmt> <x> <y>

        # Later in an opt-spec
        <fmt> : Output format
        <fmt=yaml> : YAML with 2-space indent
        <fmt=json> : JSON with 4-space indent

  - But a less-happy-path example would be something where the choices in the
    variant and the opt-specs don't cohere at all. Argle could doggedly unify
    the Opt, I suppose. And our general approach is to give users powerful
    mechanisms and concepts that can be used to concoct ridiculous
    command-line UIs -- but that's on the users to notice and fix. This
    kind of example might not be fatal, but it is particularly perverse.

        # From a variant.
        <fmt=yaml|json> <x> <y>

        # Later in an opt-spec
        <fmt> : Output format
        <fmt=xlsx> : Excel file
        <fmt=docx> : Word file

  - Choices usage across the examples and notes.txt:

    - Arg-variants: choices in a variant select that variant.
       - naval-fate: `<weapon=ship>`, `<action=set|remove>`.
       - README/wrangle: `<task=grep>`.
       - repo: `<command=clone>`.
       - blort: `<task=configure>`.
       - job-client: `<task=...>`.
       - neck-diag: `<cmd=snum>` and `<numbering=on|off>`.
       - nab: `<cmd=chomp>`.

    - Per-choice help for arg-variants, in unscoped opt-specs. The opt-spec
      restates one choice from a variant exactly:
       - README/wrangle: `<task=grep> : Emit lines...`.
       - repo: `<command=clone> : Clones...`.
       - job-client: `<task=submit> : Submit...`.

    - Variant gives a bare positional; opt-specs supply the choices. In blort
      (NOTE_805/810), the variant has `<method>`, and three opt-specs each add
      one choice with its own help (`<method=first> : ...`, and so on).

    - Choices on an option's parameter, stated in both places. `[--color
      <red|green|blue>]` appears in the wrangle variant and again in the
      pgrep-3 opt-spec. Here the choices are only for validation.

    - Per-choice help for parameters, via sub-specs (notes.txt, around lines
      2058, 2083, and 4485–4513):

           --mode <speed=fast|slow> <vol=loud|quiet> : Blah mode
           >> <speed=fast> : Blah mode-speed-fast

    - Merging Opts that share a name (notes.txt, around lines 1733 and 1881).
      Example: `<action=pitch> <action=balk|stop>` in one variant and
      `<action=catch>` in another. The merged choices can be too broad for
      error messages, and notes.txt accepts that cost.

    - Same name, different configurations (notes.txt, around line 1656):
      `(<x=A|B> | <x>{3})`.

    - Combinations of parameter choices as arg-variants (notes.txt, around
      line 4605): `--point <x=a> <y=c> [--ac]` and its siblings.

    - Choices do two jobs (opt-choices-vs-choice, around line 1581). They
      validate input, and they're also a compact way to write alternatives:
      `<step=start|stop> other!` is the same as two variants.

  - Some tension across the examples:

    - For positionals, per-choice help uses repeated unscoped opt-specs that
      get merged (items 2 and 3).
    - For parameters, it uses `>>` sub-specs (item 5).
    - That's two mechanisms for the same job. The positional form only works
      because Opts with choices are merged by name.

  - Edit list if we decide to require per-choice help text to be in sub-specs:

    - misc/notes.txt:2013 — sub-specs configure "a choice of a Positional or Parameter"
      - ok

    - misc/notes.txt:2058 — positional sub-spec example (`<speed=fast|slow>`)
      - ok

    - misc/notes.txt:4489 — positional sub-spec example (`<action=go|stop>`)
      - ok

    - misc/spec-syntax.md:418 — the doc's endorsement of unscoped per-choice opt-specs
      - would need adjustment

    Examples using unscoped per-choice help:

    - misc/examples/argle-mock-ups/argle-repo.py:61 — `Commands :::`, no parent line
      - help text would be better if we changed policy

    - misc/examples/spec-vs-api/job-client-argle:37 — no parent line
      - ditto

    - misc/examples/argle-mock-ups/blort.py:201 — NOTE_810, no parent line
      - ditto

    - misc/examples/argparse-vs-argle/wrangle:85 — parent `<task>` line already present
      - is consistent with a revised policy

    - README.md:324 — same as wrangle
      - ditto
