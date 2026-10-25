
<!--

# reboot-status : Status of project reboot
# Most active files
# TODOs
# SPEC_ISSUE: re-assess the whitespace rules in spec-syntax
# SPEC_ISSUE: first-char spec does not allow short options like `-1`
# SPEC_ISSUE: variant vs opt-spec conflicts: quantifiers
# SPEC_ISSUE: conflicts among opt-specs
# SPEC_ISSUE: variant vs opt-spec conflicts: parameters
# SPEC_ISSUE: variant vs opt-spec conflicts: choices
  ## Motivating problems and context
  ## Draft policy/goals
  ## Edit list for per-choice help text to be in sub-specs
  ## Mock-up scenarios
    ### Relevant criteria
    ### Argparse messages: reference for the mockup work
    ### Scenarios
      #### S-TEMPLATE
      #### S1: positional with choices; variants-only
      #### S2a: S1 plus a partial opt-spec and an epilogue; no slot
      #### S2b: S2a plus an `{opts}` slot
      #### OTHER

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

- Deal with spec-syntax issues (see SPEC_ISSUE below).

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

# SPEC_ISSUE: re-assess the whitespace rules in spec-syntax

Pushing toward further relaxation, I think we still have some overly strict
rules that lack a strong rationale.

Pushing the other way, one of our whitespace examples (ipconfig or ifconfig?)
used a `KEY VALUE` style where the keys functioned basically as options
without the `--` prefix. One of Argle's future goals will be to allow users to
set the option-prefixes (defaults are `-` and `--`). Conceivably, an
ifconfig-style use case would want a prefix of empty string, right? Is
supporting that type of use case a situation where we might want to tighten
the whitespace rule for named-groups?

# SPEC_ISSUE: first-char spec does not allow short options like `-1`

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

# SPEC_ISSUE: variant vs opt-spec conflicts: quantifiers

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

  - P3

# SPEC_ISSUE: conflicts among opt-specs

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

# SPEC_ISSUE: variant vs opt-spec conflicts: parameters

What about opt-specs that completely change the parameters of an Option?

    --bar <b1> <b2>        # In a variant
    --bar <b1> [<b2>]      # In an opt-spec
    --bar <x> <y> <z>      # Ditto -- but more divergent

# SPEC_ISSUE: variant vs opt-spec conflicts: choices

## Motivating problems and context

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

## Draft policy/goals

Key policy goals/decisons and findings:

  - P0. Strict Opt independence in the grammar (tentative). Each Opt
    occurrence implied by the spec is a distinct Opt. No unification by
    Opt.name, including for Opts with choices.

    - Arg-parsing: no known examples where this leads to incorrect parsing
      or unsupported use cases. Several require it (naval-fate, EX_NAB,
      `--bar` with differing parameters). First-success backtracking
      handles same-named Opts within one context.

    - What unification was meant to provide (unified help entries, full
      choice listings in errors, merged values) is handled at the output
      surfaces (help, errors, Result) by grouping same-named Opts, not by
      merging them in the grammar.

    - TBD: API calls to unify Opts in the grammar after the fact. Leaning
      no, since it could cause trouble for arg-parsing.

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

    - NOTE: I suspect some of these policies will also apply to per-parameter
      help text for options.

    - Help text on a regular opt-spec always belongs to the Opt itself,
      never to a choice, regardless of how many choices it names.

    - A per-choice sub-spec must name exactly one choice. Synonymous
      choices (eg `ls --color` accepting always|yes|force) are handled by
      documenting one and mentioning the others in its help text.
      First-class choice aliases would be a separate future feature.

    - Per-choice help for a parameter requires a named parameter (eg
      `<c=red|green>`). A choices-only parameter (`<red|green>`) cannot be
      reached by a sub-spec, because `<red>` reads as a parameter name.

  - P6. If a variant declares choices for a VarInput, they are authoritative.
    Opt-specs (regular or sub-spec) may name only those choices; naming any
    other is an error. Not every choice needs to be documented. If the variant
    declares no choices, the opt-specs supply them.

    - NOTE: this is currently under review and might change.

    - NOTE: P0 (strict Opt independence) would eliminate the merging by
      name assumed here.

    - When a VarInput with choices appears in several places in the
      variants, those occurrences are merged by name, and the
      authoritative set is the union of their choices.

    - A parent (regular) opt-spec must either restate the full
      authoritative set or say nothing about choices. A subset or superset
      is an error. Agreement means set equality, so order does not matter.

          --color <c=red|green|blue> : OK (full agreement)
          --color <c> : OK (silent about choices)
          --color <c=red|green> : Error (subset)

    - Sub-specs name choices one at a time (see P5) and need not cover all
      of them.

    - Tentative: help-text display order of choices comes from the
      sub-specs if any, otherwise from the variants.

  - P7. Merging of choice-bearing VarInputs. In the variants, Opts with
    choices that share a name are merged; Opts without choices are
    independent. Merging is a spec-parse step over the variants only:
    choices supplied later by opt-specs do not cause merging, so such Opts
    stay independent (each receiving the same choices).

    - NOTE: this is currently under review and might change.

    - NOTE: P0 (strict Opt independence) would eliminate the merging by
      name assumed here.

    - Parameters: the same rules apply within the parameters of a single
      Option. Options themselves are never merged, so same-named parameters
      in different Option instances stay independent.

  - P8. Same-named choice-bearing and choiceless Opts. Matching stays based
    on name, kind, and scope (adding choices to the matching criteria would
    turn conflicts into silent non-matches). If an unscoped opt-spec matches
    both kinds of Opt (eg `<x=A|B>` and a bare `<x>` in the variants):

    - Help only (eg `<x> : help`): allowed. Both Opts get the help text. The
      duplication is visible in the help output, and the user can fix it
      with a scope.

    - Names choices, itself or via sub-specs: error; use a scope. Otherwise
      the choiceless Opt would silently gain the choices, a behavior change
      that the help output does not reveal.

  - P9. Documenting choices. Argle is roughly following git, in not listing
    VarInput choices in usage text or in the grammatical/formal portion of the
    opt-descs. Instead, it's default will be to append choices to an Opt's
    help text (see mockups for details).

    - NOTE: this applies to plural choices. A single-choice Opt (eg an
      arg-variant like `<cmd=merge>`) displays its choice as a literal in
      usage text, as git does (`git merge [<options>]`).

  - P10. Help text defaults:

    - If user supplies only variants (no opt-specs), Argle will generate a
      typical listing of opt-descs. Why this is a helpful default:

      - Following git, we intend to display VarInput choices in opt-desc
        help-text, not in the opt-desc CLI-grammar (see P9).

      - If Argle did not generate opt-descs in this scenario, choices would
        remain undocumented. So the auto-generated opt-descs provide a home
        for the listing of choices.

    - If the user supplies some opt-descs but not an complete list of them,
      the generated help text will follow the presentation/ordering of the
      users opt-specs (and other help-text elements). Then at the end Argle
      will append an "Arguments:" section listing the opt-descs for which the
      the user did not supply corresponding opt-specs.

      - Why auto-generate and append by default? Same reason as above: it will
        be the only means of displaying choices.

      - The API will allow users to request things like:
        - Do NOT auto-generate the missing opt-descs.
        - Raise if the user's opt-descs are not exhaustive (meaning: all Opts
          in the variants were matched by an opt-spec).

  - P11. Help-text slots (tentative):

    - One mechanism for placing generated or custom content in help text:
      named slots, written `{name}`. Replaces the earlier ideas of `@`
      directives plus a separate inline-interpolation syntax.

    - Registry: Argle pre-registers built-in slots. Users register their
      own via the API, each with a hook (see P12). Built-ins are just
      slots that Argle ships.

    - Placement determines behavior, not syntax:
      - Slot alone on a line: block insertion.
      - Slot inside text (opt-help-text, block-quote): inline insertion.

    - Likely built-ins:
      - Block: `{opts}`, `{options}`, `{positionals}`, `{usage}`.
      - Inline, Opt-level: `{default}`, `{choices}`, maybe `{name}`.
      - Inline, parser-level: `{prog}`, `{version}`.

    - Validation and escaping: braces enclosing an unregistered name are an
      error (catches typos). Escape with a backslash (`\{default}`), per the
      Quoting rules. No format-spec mini-language.

    - Substitution happens inside Argle's rendering pipeline, before
      wrapping, so line widths reflect the inserted text.

    - Render-once rule: each Opt, or each data item, renders once, and
      explicit placement wins. Slots are processed in spec order. An Opts
      block includes only Opts not yet rendered; the default tail section
      (P10) is effectively a final `{opts}`. An explicit inline slot
      suppresses the auto-append of that item (eg choices per P9).

    - Corollary: to move the default tail, place an Opts slot (eg
      `{opts}` before an epilogue). Render-once leaves nothing for the
      tail, so no extra rule is needed.

    - No scoping syntax. Scoped content (eg one subcommand's opt-descs)
      comes from a user slot whose hook supplies the query.

  - P12. Slot hooks (tentative):

    - Registration, roughly: `p.slot('add_opts', func)`.

    - A hook receives context (the parser, plus the current Opt when
      there is one) and returns a description of what to insert. It does
      not munge generated help text.

    - Return types:
      - `str`: text with default handling (wrapped).
      - Text object: text plus instructions (eg `wrap=False`).
      - Opts selection: a query result or query-path. Argle renders the
        opt-descs and applies the render-once rule.
      - List of the above, for mixed content (eg heading plus Opts block).

    - An Opts selection is valid only for a block slot. Returning one
      from an inline slot is an error.

    - Render-once is resolved when Argle processes the returned value, not
      when the hook builds its query. Hooks can select broadly (eg
      `cmd=add.*`) without tracking what was already rendered.

    - Escape-hatch tiers: (1) built-in slots, no code; (2) user slots
      and the general API; (3) later: hooks that receive a structured help
      model before rendering.

    - Open:
      - Line type for a block slot in the spec (Line types needs a rule
        so `{opts}` is not read as a variant or opt-spec).
      - Per-scope generated sections (S4/S5), and whether they are common
        enough to justify spec-level scoping later.
      - Default split of positionals and options into separate sections.
      - Whether `{default}` in a per-choice sub-spec refers to the parent
        Opt or the choice.
      - Whether help text set via the API gets slot substitution.

  - P13. Grammar vs surfaces. The grammar (or model) is the tree of Opts and
    Groups built from the spec, which arg-parsing runs against. Surfaces (or
    outputs, views) are what Argle produces from, or uses to address, the
    grammar. Questions of "are these the same thing?" can be answered
    differently at each: the grammar keeps Opts independent (P0), while a
    surface may group same-named Opts.

    - Surfaces relevant to Opt independence:

      - Opt-specs (an input surface).
        - ASSESS/RESOLVE

      - Usage text.
        - Mostly not impacted by independence/unification.
        - For single-choice VarInput, we display the `choice`, not the
          `<name>`.

      - Help text (opt-descs).
        - ASSESS/RESOLVE

      - Error messages (parse-time and spec-time).
        - ASSESS/RESOLVE

      - Result.
        - No big problems.
        - The purpose of a Result is to unify by Opt.dest.

      - API: Opt configuration: query(), get(), config().
        - Config write: OK, due to our broadcast model (with scopes).
        - Config read: maybe resolvable via P14.

      - Opt repr().
        - ASSESS/RESOLVE

      - Dispatch.
        - ASSESS/RESOLVE

      - Tab-completion.
        - ASSESS/RESOLVE

    - Other surfaces:
      - Version output.
      - Runtime messages (warn, exit).

  - P14. API reads (tentative). Reading an attribute from a query result
    unifies across its OptNodes: the distinct union of values, in spec order.

    - NOTE: An OptNode is (for now) just a term being used in our current
      planning work; it is not a formal object in the Argle system. It
      represents an Opt within the grammar/variants under our tentatively
      adopted policy of strict Opt independence at the grammar level. In this
      discussion, OptNode is the truly independent Opt-thing, as distinguished
      from the unified Opt-thing that a user wants/perceives across various
      Argle outputs/surfaces.

    - List-valued attributes (eg choices, aliases): flattened, de-duped,
      always a list.

    - Scalar attributes (eg help, dest): the scalar if one distinct value,
      otherwise a list of the distinct values. Known ambiguity: a scalar
      whose value can itself be a list (eg default).

    - Structural attributes (eg parameters, position, quantifier): not
      unified; read per OptNode.

    - Raw access: iterate the query result to get its OptNodes, eg
      `list(p.query('x'))`.

    - Opt attributes (purely for reference here; DELETE EVENTUALLY):
      - kind (positional, option, parameter, literal)
      - name
      - dest
      - aliases
      - help_text
      - choices (each with per-choice help text)
      - parameters
      - nargs
      - ntimes
      - quantifier: m, n, required, greedy
      - default
      - factory
      - convert
      - validate
      - dispatch
      - priority
      - negaters
      - hide
      - anchor
      - text (literals)
      - usage_text (misc/notes.txt:3743)
      - spec (the Opt.spec TODO)
      - position and parent (implicit in the tree)

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

## Edit list for per-choice help text to be in sub-specs

  - misc/notes.txt:2013 — sub-specs configure "a choice of a Positional or Parameter"
    - ok

  - misc/notes.txt:2058 — positional sub-spec example (`<speed=fast|slow>`)
    - ok

  - misc/notes.txt:4489 — positional sub-spec example (`<action=go|stop>`)
    - ok

  - misc/spec-syntax.md:418 — the doc's endorsement of unscoped per-choice opt-specs
    - would need adjustment

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

## Mock-up scenarios

Problem solving strategy:

  - Mock up inputs and outputs for each scenario:
    - spec
    - API calls if needed
    - usage text
    - help text
    - error reporting for arg parsing

  - Then derive rules from the mock-ups.

### Relevant criteria

Criteria to consider in scenarios:

  - N choices
    - 0 choice
    - 1 choice
    - 2+ choices

  - User supplies an opt-spec:
    - yes: with sub-specs
    - yes: only opt-spec
    - no

  - Where choices are declared:
    - Variants
    - Opt-specs
    - Both

  - Role of choices:
    - Arg-variant
    - Arg validation only

  - VarInput type:
    - Positional
    - Parameter: named
    - Parameter: unnamed

  - N Opts sharing same name:
    - 1
    - 2+

  - Output style:
    - <name>
    - <A|B|C>
    - <name=A|B|C>

  - Output surface:
    - Usage
    - Opt-desc
    - Errors

  - Size of listing all choices:
    - Small: practical for help-text display
    - Large: too many values

### Argparse messages: reference for the mockup work

Error message format:

    usage: USAGE_TEXT
    PROG: error: MSG

Common messages:

    Missing required args | the following arguments are required: x, n, --user
    Invalid conversion    | argument n: invalid int value: 'abc'
    Invalid choice        | argument z: invalid choice: 'D' (choose from 'A', 'B', 'C')
    Excess positional     | unrecognized arguments: extra
    Unknown option        | unrecognized arguments: --blort
    Missing parameters    | argument --color: expected one argument
    Mutually exclusive    | argument --yaml: not allowed with argument --json
    Ambiguous abbrev      | ambiguous option: --ver could match --verbose, --verify
    Invalid subcommand    | argument cmd: invalid choice: 'fubb' (choose from 'add', 'rm')

Argle improvements:
  - Capitalize "Usage:".
  - Better lingo rather than calling everything "arguments."
  - Errors should use name (not dest) to be consistent with usage/help text.

Argparse problems: don't do these:
  - Too few parameters is misdiagnosed:
    - Input: `--point 3 --user bob`.
    - Argparse mistook `--user` as 2nd param of `--point` (invalid int).
    - Argle arg-parsing implementation does not have this problem.
    - This argparse problem is kind of unforgivable.

  - Unhelpful message when subcommand is wrong:
    - Input: `add 1 --force`.
    - Output: top-level usage and a plain "unrecognized arguments."
    - Better would be: suggest the fix: use `rm`.
    - Asses: how much fix-it advice is practical to implement reliably.

Argle messages: examples:

    # No args at all

        $ basic
        usage: basic [-h] [--point X Y] [--color {red,green,blue}] --user USER [-v]
                     [--json | --yaml] [--verify]
                     x n [{A,B,C}]
        basic: error: the following arguments are required: x, n, --user

    # Missing required positional

        $ basic xx --user bob
        usage: basic [-h] [--point X Y] [--color {red,green,blue}] --user USER [-v]
                     [--json | --yaml] [--verify]
                     x n [{A,B,C}]
        basic: error: the following arguments are required: n

    # Invalid int conversion

        $ basic xx abc --user bob
        usage: basic [-h] [--point X Y] [--color {red,green,blue}] --user USER [-v]
                     [--json | --yaml] [--verify]
                     x n [{A,B,C}]
        basic: error: argument n: invalid int value: 'abc'

    # Invalid choice: positional

        $ basic xx 1 D --user bob
        usage: basic [-h] [--point X Y] [--color {red,green,blue}] --user USER [-v]
                     [--json | --yaml] [--verify]
                     x n [{A,B,C}]
        basic: error: argument z: invalid choice: 'D' (choose from 'A', 'B', 'C')

    # Excess positional

        $ basic xx 1 A extra --user bob
        usage: basic [-h] [--point X Y] [--color {red,green,blue}] --user USER [-v]
                     [--json | --yaml] [--verify]
                     x n [{A,B,C}]
        basic: error: unrecognized arguments: extra

    # Missing required option

        $ basic xx 1
        usage: basic [-h] [--point X Y] [--color {red,green,blue}] --user USER [-v]
                     [--json | --yaml] [--verify]
                     x n [{A,B,C}]
        basic: error: the following arguments are required: --user

    # Unknown option

        $ basic xx 1 --blort --user bob
        usage: basic [-h] [--point X Y] [--color {red,green,blue}] --user USER [-v]
                     [--json | --yaml] [--verify]
                     x n [{A,B,C}]
        basic: error: unrecognized arguments: --blort

    # Option missing its parameter

        $ basic xx 1 --color --user bob
        usage: basic [-h] [--point X Y] [--color {red,green,blue}] --user USER [-v]
                     [--json | --yaml] [--verify]
                     x n [{A,B,C}]
        basic: error: argument --color: expected one argument

    # Invalid choice: parameter

        $ basic xx 1 --color pink --user bob
        usage: basic [-h] [--point X Y] [--color {red,green,blue}] --user USER [-v]
                     [--json | --yaml] [--verify]
                     x n [{A,B,C}]
        basic: error: argument --color: invalid choice: 'pink' (choose from 'red', 'green', 'blue')

    # Too few parameters (nargs=2)

        $ basic xx 1 --point 3 --user bob
        usage: basic [-h] [--point X Y] [--color {red,green,blue}] --user USER [-v]
                     [--json | --yaml] [--verify]
                     x n [{A,B,C}]
        basic: error: argument --point: invalid int value: '--user'

    # Invalid int in parameter

        $ basic xx 1 --point 3 q --user bob
        usage: basic [-h] [--point X Y] [--color {red,green,blue}] --user USER [-v]
                     [--json | --yaml] [--verify]
                     x n [{A,B,C}]
        basic: error: argument --point: invalid int value: 'q'

    # Mutually exclusive conflict

        $ basic xx 1 --json --yaml --user bob
        usage: basic [-h] [--point X Y] [--color {red,green,blue}] --user USER [-v]
                     [--json | --yaml] [--verify]
                     x n [{A,B,C}]
        basic: error: argument --yaml: not allowed with argument --json

    # Ambiguous abbreviation

        $ basic xx 1 --ver --user bob
        usage: basic [-h] [--point X Y] [--color {red,green,blue}] --user USER [-v]
                     [--json | --yaml] [--verify]
                     x n [{A,B,C}]
        basic: error: ambiguous option: --ver could match --verbose, --verify

    # Subcommand: none given

        $ subcmd
        usage: subcmd [-h] [--trace] {add,rm} ...
        subcmd: error: the following arguments are required: cmd

    # Subcommand: invalid

        $ subcmd fubb
        usage: subcmd [-h] [--trace] {add,rm} ...
        subcmd: error: argument cmd: invalid choice: 'fubb' (choose from 'add', 'rm')

    # Subcommand: missing positional

        $ subcmd rm
        usage: subcmd rm [-h] [--force] x
        subcmd rm: error: the following arguments are required: x

    # Subcommand: option from sibling

        $ subcmd add 1 --force
        usage: subcmd [-h] [--trace] {add,rm} ...
        subcmd: error: unrecognized arguments: --force

### Scenarios

Scenario info to consider adding after we have more scenarios drafted:

  - Criteria exercised.

  - Mockup alternatives that were considered:
    - I'm not sure about this one -- maybe.
    - OTOH, the mockup will express our preferred answer.
    - And we can add notes to the scenario if any alternatives are noteworthy.

  - The argparse equivalent, for comparison.
    - Maybe, if noteworthy.

  - Rules implied by the mock-up.

  - Open questions.

  - Error messages.

  - API calls:
    - Add to "Notes" sub-section only if noteworthy.

  - Result() mockup and matching end-user input:
    - Add to "Notes" sub-section only if noteworthy.

#### S-TEMPLATE

Raw notes:
  __

Description:
  - Variants: __.
  - Opt-specs: __.
  - __

Spec:

    __

Help text:

    Usage:
      PROG __

    Arguments:
      __

Notes:
  - __

#### S1: positional with choices; variants-only

Description:
  - Variants: 1.
  - Opt-specs: none.
  - Positional with choices and a default.
  - Option whose parameter has choices.

Spec:

    [<action=run|walk|rest>] [--pace <p=slow|fast>] [-n]

Help text:

    Usage:
      PROG [<action>] [--pace <p>] [-n]

    Arguments:
      <action>        [run|walk|rest] [default: run]
      --pace <p>      [slow|fast]
      -n

Notes:
  - Opt choices and default are auto-appended to an opt-desc (P9).

#### S2a: S1 plus a partial opt-spec and an epilogue; no slot

Description:
  - Variants: 1.
  - Opt-specs: some, not all.
  - Epilogue via block-quote.
  - No `{opts}` slot, so unmatched Opts listed at end.

Spec:

    [<action=run|walk|rest>] [--pace <p=slow|fast>] [-n]

    Arguments ::
    <action> : What to do

    ```Exit status is 0 on success, 1 on failure.```

Help text:

    Usage:
      PROG [<action>] [--pace <p>] [-n]

    Arguments:
      <action>        What to do [run|walk|rest] [default: run]

    Exit status is 0 on success, 1 on failure.

    Arguments:
      --pace <p>      [slow|fast]
      -n

Notes:

  - Exercises P10: user supplied only some opt-specs, so Argle lists the rest
    at the end under an "Arguments" heading. API can be used to modify that
    default heading. Also see S2b, which offers a better alternative via the
    `{opts}` slot.

#### S2b: S2a plus an `{opts}` slot

Description:
  - Same as S2a.
  - Plus `{opts}` slot to control placement of auto-generated opt-descs.

Spec:

    [<action=run|walk|rest>] [--pace <p=slow|fast>] [-n]

    Arguments ::
    <action> : What to do
    {opts}

    ```Exit status is 0 on success, 1 on failure.```

Help text:

    Usage:
      PROG [<action>] [--pace <p>] [-n]

    Arguments:
      <action>        What to do [run|walk|rest] [default: run]
      --pace <p>      [slow|fast]
      -n

    Exit status is 0 on success, 1 on failure.

Notes:

  - Exercises P11: the `{opts}` slot renders the remaining opt-descs in
    place, so no section is appended at the end.

  - Implied rule: the `{opts}` slot renders opt-descs only, with no heading.

  - Assumes a Line types rule for a block slot on its own line (see P12).

#### OTHER

    S3. S1 plus an opt-spec and sub-specs
        [<fmt=json|yaml>] : Output format
        >> <fmt=json> : JSON with 4-space indent
        >> <fmt=yaml> : YAML

        Refs:
            misc/notes.txt:2013
            misc/notes.txt:2058
            misc/notes.txt:2081
            misc/notes.txt:4451
            misc/notes.txt:4493
            misc/notes.txt:4515
            misc/notes.txt:4573
            misc/examples/argle-mock-ups/blort.py:201
            misc/examples/argle-mock-ups/blort.py:326

    S4. Subcommand program (arg-variants), zero effort
        <cmd=add> <x>
        <cmd=rm> <x> [--force]

        Refs:
            misc/notes.txt:1598
            misc/notes.txt:2921
            misc/notes.txt:2979
            misc/examples/argle-mock-ups/argle-repo.py:47
            misc/examples/spec-vs-api/job-client-argle:23
            misc/spec-examples.md:55

    S5. S4 plus an opt-spec and sub-specs (README/repo style; the
        known-good baseline)

        Refs:
            README.md:316
            README.md:324
            README.md:425
            misc/examples/argparse-vs-argle/wrangle:77
            misc/examples/argparse-vs-argle/wrangle:85
            misc/examples/argparse-vs-argle/wrangle:186
            misc/examples/argle-mock-ups/argle-repo.py:61
            misc/examples/argle-mock-ups/argle-repo.py:200
            misc/examples/spec-vs-api/job-client-argle:37
            misc/examples/argle-mock-ups/blort.py:127
            misc/examples/argle-mock-ups/blort.py:19
            misc/examples/click/click-repo.py:182

    S6. Unnamed choices-only parameter, opt-spec only (README pgrep-3)
        [--color <red|green|blue>] : Highlight matching text

        Refs:
            misc/spec-syntax.md:399
            misc/spec-syntax.md:422
            README.md:190
            README.md:243
            README.md:335
            README.md:447
            misc/examples/argparse-vs-argle/pgrep-3-enhanced:47
            misc/examples/argparse-vs-argle/pgrep-3-enhanced:69
            misc/examples/argparse-vs-argle/pgrep-3-enhanced:93
            misc/examples/argparse-vs-argle/wrangle:96
            misc/examples/argparse-vs-argle/wrangle:208
            misc/examples/help-text-styles.txt:234

    S7. Large choice set
        [--tz <tz=UTC|EST|PST|...30 more>] : Time zone

        Refs: none found

    S8. Same-named arg-variant positional, multiple choices at one position
        (naval-fate)
        <weapon=ship> <action=new> <name>...
        <weapon=mine> <action=set|remove> <x> <y>

        Refs:
            misc/examples/argle-mock-ups/argle-naval-fate.py:74
            misc/examples/argle-mock-ups/argle-naval-fate.py:98
            misc/examples/docopt-naval-fate:10
            misc/examples/click/click-naval-fate.py:108
            misc/spec-syntax.md:415
            misc/notes.txt:1733
            misc/notes.txt:4808

    S9. Same name, different validation-only choices per variant
        <cmd=a> <fmt=json|yaml>
        <cmd=b> <fmt=csv>

        Refs:
            misc/notes.txt:1656
            misc/notes.txt:1881

    S10. Same name, choices in one variant, bare in another (the P8 case)
        <cmd=a> <x=A|B>
        <cmd=b> <x>

        Refs:
            misc/notes.txt:1656
            misc/notes.txt:1774
