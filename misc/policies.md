
<!-- TOC-SLUG

  # todos                                 | TODOs
  # argle-policies                        | Policies
    ## grammar                            | Grammar and identity
      ### grammar-opt-independence        | P0: Strict Opt independence in the grammar
      ### grammar-vs-surfaces             | P13: Terminology: grammar vs surfaces
      ### surface-unification             | P101: Opts are generally unified at surfaces
      ### opt-path-property               | P17: Add an Opt.path property
    ## opt-specs                          | Opt-specs and matching
      ### opt-spec-matching               | P16: Opt-spec matching
      ### opt-spec-matching-compatibility | P21: Opt-spec matching and compatibility generally
      ### opt-spec-matching-names         | Opt-spec matching: names and aliases
      ### opt-spec-matching-uniqueness    | P19: An Opt cannot be matched more than once
      ### opt-spec-matching-no-match      | P20: Opt-specs that match nothing
      ### opt-spec-matching-quantifier    | Opt-spec matching: quantifier compatibility
      ### opt-spec-matching-parameters    | Opt-spec matching: parameter compatibility
      ### opt-spec-matching-choices       | Opt-spec matching: choice compatibility
    ## help-text                          | Help text
      ### documenting-choices             | P9: Documenting choices
      ### help-text-autogen-opt-descs     | Help text: auto-generated opt-descs
      ### help-text-slots                 | P11: Help-text slots
      ### sub-specs                       | Sub-specs policy
    ## api                                | API
      ### api-reads                       | P14: API reads
      ### query-result-repr               | P18: Query-result repr
    ## anonymous-parameters               | Anonymous parameters are supported
    ## dispatch-opt-independence          | P15: Dispatch and Opt independence
  # other-material                        | Other material to edit, move, delete

-->

This document is the home for Argle's policy decisions: how Argle interprets,
resolves, or reacts when a situation admits more than one plausible behavior.

How the document relates to other key documents:

  - `terminology.md`: basic definitions.

  - `spec-syntax.md`: defines the form of a spec.

  - `classes.md`: lists classes and their attributes, methods. Will eventually
    be obsolted by the Python code.

  - `policies.md`: a place to state Argle policies that do not otherwise
    belong in the more focused documents noted above.

  - Other documents. These can cover more discursive topics: rationale,
    discussion, examples, rejected alternatives, etc.

We will use slug-style references to avoid repetition and to keep the
most-focused documents as tight and readable as possible. For example,
spec-syntax.md can delegate details to policies.md, which can delegate to the
more discursive documents.

# todos: TODOs

Edit the policies: initial pass.

Fill in gaps marked with `__` (eg, with policy cross-references).

Move details out: __DETAILS_TO_MOVE__

Deal with these: __ASSESS__

# argle-policies: Policies

## grammar: Grammar and identity

### grammar-opt-independence: P0: Strict Opt independence in the grammar

Each Opt occurrence in the spec/grammar is a distinct Opt:
  - No unifying by name/dest.
  - Includes Opts with choices, reversing prior policy.

__DETAILS_TO_MOVE__:

  - Argument parsing:
    - Strict independence probably simplifies parsing: no need to reason about
      Opt(foo) at position 3 vs the one at position 7.
    - Challenging examples under opt-unification: naval-fate, EX_NAB.
    - No known examples where independence leads to incorrect parsing.
    - Same-named Opts competing for the same input (eg two `--bar` in one
      variant with differing N of parameters) need no special rule: first
      success wins.

  - Rejected alternative:
    - Opt unification by name, plus position metadata.
    - Probably feasible, but it adds bookkeeping.

  - Multiple Opts with same name are rare:
    - Rarer still: multiple same-name Opts requiring differing configurations.
    - Advanced use cases can be expected to use the API.

### grammar-vs-surfaces: P13: Terminology: grammar vs surfaces

Grammar:
  - The list-tree of Variants, Opts, Groups, etc.
  - Analogous to the "model" layer in other domains.

Surfaces:
  - The areas where users and end-users encounter Opts.
  - Analogous to the "views" layer in other domains.
  - But the concept in Argle is broader:
    - Mostly outputs (eg help text, parsed-args Result).
    - But also inputs (eg spec or API for configuration).
    - And sometimes behaviors (eg dispatch).

### surface-unification: P101: Opts are generally unified at surfaces

Policy summary of Opt independence/unification, by surface:

    Surface        | Policy summary
    ------------------------------------------------------------
    Opt-specs      | Unified via broadcast
    Help text      | Unified by default; independence via scopes
    Error msgs     | __
    Result         | Purpose is to unify by Opt.dest
    API Opt writes | Unified via broadcast; independence via query-path
    API Opt reads  | Unified by default, with API workarounds
    Dispatch       | Unified by (OPT-NAME, FUNC, RESULT)
    ------------------------------------------------------------
    Usage text     | Not unified: independence helps
    Opt repr()     | Purpose is technical; unification unhelpful
    Tab-completion | Not unified: independence helps
    ------------------------------------------------------------
    Version output | No relevance
    Warn/exit msg  | No known relevance

__DETAILS_TO_MOVE__:

  - Most CLI use cases want Opt unification at surfaces:

    - The degnerate case:
      - The issue never arises, because Opt names are unique.
      - Represents the vast majority of CLI programs.

    - Typical subcommand program:
      - Usage variants are selected via a command/action Positional.
      - Unification is the user's intent.
      - Example: git.

    - Same-name Opts across multiple variants:
      - The user wants the same-name Opts configured identically.
      - Example: --verbose flag.

### opt-path-property: P17: Add an Opt.path property

__ASSESS__:
  - This probably belongs in classes.md, not here.

Add Opt.path as @property:
  - Returns query path to exactly select the Opt.
  - Example use cases:
    - Opt repr().
    - Spec parsing error messages.
    - Debugging by users or Argle devs.
  - Must be an on-demand property:
    - Subsequent API changes, even to other Opts, can affect what an Opt.path
      requires for uniqueness.
  - Not the same as a scope:
    - A scope can select a context/universe -- more than one Opt.

## opt-specs: Opt-specs and matching

### opt-spec-matching: P16: Opt-spec matching

An opt-spec is a broadcast configuration mechanism:

  - It is applied to every matching Opt from variants.

  - Matching criteria:
    - Opt.name (see __).
    - Opt type: Positional or Option (see __).
    - The opt-spec's scope, if any (see __).

  - Matches must be compatibility along these dimensions:
    - Quantifier (see __).
    - Parameters (see __).
    - Choices (see __).

  - Argle will raise if there are incompatible matches.

### opt-spec-matching-compatibility: P21: Opt-spec matching and compatibility generally

When analyzing compatibility Argle will usually allow:
  - Silence: saying nothing specific about a dimension.
  - Equality: between the opt-spec and each matched Opt from variants.

Either side can carry the details about quantifiers, parameters, or choices:
  - Compact variants and fleshed out opt-specs.
  - Or the reverse.
  - But explicit inequality is not allowed.

The test for silence is syntactic:
  - Does the user supply explicit spec syntax related to the dimension.
  - Example: `--foo` and `(--foo)` define a required Option, but only the
    first is silent on quantification.

Compatability is analyzed for the whole dimension, not its sub-components:
  - For example: `--foo{2-3}` and `--foo{2-3}?` are incompatible (there is no
    separate "greediness dimension").

No mixed bags:
  - An opt-spec can match multiple Opts from variants.
  - The silent-or-equality test requires the latter to be consistent:
    - If an opt-spec matches 3 Opts, all of them can be silent on a dimension
      or their configuration can equal that in the opt-spec.

__DETAILS_TO_MOVE__:

  - For opt-spec matching compatibility, why allow silence?
    - It does mean that one part of the spec (either variants or opt-specs)
      can mislead in isolation (ie the silent part).
    - But that bit of tension -- at least for some users -- is a worthwhile
      tradeoff because it buys them the convenience of configuring details
      only once, in the place of their choosing.
    - But taking the next step toward flexibility -- allowing explicitly
      incompatible/different configurations in variants vs opt-specs -- leads
      to ambiguity about user intent, both for Argle and the users themselves.

  - For opt-spec matching compatibility, why disallow mixed bags?
    - Uniform variants signal clear intent (all compact, or all fully
      specified).
    - A mixed bag sends mixed signals: the silent Opt may be deliberate or an
      omission, and Argle cannot tell which.

### opt-spec-matching-names: Opt-spec matching: names and aliases

Positionals:
  - The name-match is simple, because they have only one name.

Options:
  - The name-match can be based on the Option name or any alias.
  - Aliases can be short or long.

__DETAILS_TO_MOVE__:

  - An opt-spec should be able to add aliases and/or a long name to a variant
    Option. This gives the user flexibility in expressing the variant grammar
    either explicitly (using long names) or compactly to emphasize grammar
    structure (using short aliases).

  - Why aliases can be short or long: prior art (eg tar: `-x --extract --get`).

  - The Opt-spec's last Option name is the Opt.name. The rationale: the form
    closest to the parameters (if any) reads as the most important.

        -x --blort --fubb <a> <b> : Help text for Option(fubb)

  - Ordering of aliases and option name in an opt-spec affects, but might not
    dictate, the ordering/presentation in generated help text (the latter can
    be configured).

### opt-spec-matching-uniqueness: P19: An Opt cannot be matched more than once

An Opt cannot be matched by multiple opt-specs.
  - Sub-specs exempt: the parent opt-spec does the matching.

__DETAILS_TO_MOVE__:

  - Why an Opt cannot be matched by multiple opt-specs:

    - A user might want an opt-desc to appear in multiple spots in help text.
      Why not allow that?

    - It opens a new problem domain: conflicts among opt-specs:

          # Identity conflict: what is the Opt.name?
          -i --ignore-case
          -i --invert

          # Content conflict: which help text is canonical?
          --foo : Help blah
          --foo : Help blah blah

    - Showing an opt-desc in multiple spots is a display concern:
      - Tentative mechanism: slots (see P11).

    - Keeping Opt configuration single-source:
      - Simplifies Argle policy.
      - Provides clarity to users.

    - Alternative considered:
      - A bare opt-spec acting as an opt-spec mention.
      - Rejected:
        - The mechanism adds policy rules to solve a specific problem.
        - The same problem can be solved with slots, a more powerful
          mechanism.

### opt-spec-matching-no-match: P20: Opt-specs that match nothing

An opt-spec that matches no Opt declares a new Opt:

  - The new Opt is appended to a target.
  - The target must be a single partial or variant.
  - The target much be unambiguous.
  - If not, Argle raises.

  - The append is simple:
    - The new Opt is added to the end of the target.
    - It is not added inside of group (even if group is last element).

  - Target situations:
    - Zero user-defined variants: appended to Argle-generated variant.
    - One variant: appended to it.
    - Multiple variants: opt-spec scope must point to one partial or variant.

__DETAILS_TO_MOVE__:

  - Alternatives considered for opt-spec-matching-no-match:

    - Forbid no-match opt-specs in the single-variant case:
      - Why? To help user in typo-detection.
      - But we found contrary use case example;
        - A CLI grammar with some grammatical complexity, plus a routine and
          long list of other Opts.
        - The complex part:

              ( (<x> <y> --style <json|yaml>) | (<a> <b> <c> [--fast]) )

        - And the user would rely on opt-specs to document all of the Opts,
          both those in the compex part and the long list of other Opts.
        - Argle generally favors flexibility and power over rigorous policy to
          guard against every conceivable mistake.

    - A spec-level placeholder:
      - Examples: `[<other-opts>]`,or `__OTHER_OPTS__`.
      - It would mark where unmatched opt-specs go.
      - Not helpful or needed: partials plus scopes cover the use case.

    - Use named groups (plus scopes) to specify where unmatched Opts go.
      - Named groups serve other purposes (Result data structure and
        usage-text readability).
      - Overloading the mechanism with another purpose seemed unwise.

### opt-spec-matching-quantifier: Opt-spec matching: quantifier compatibility

How to determine quantifier compatibility:

  - Opt-spec silence is allowed:
    - The variant can supply the quantifier.
    - The opt-spec can present the Opt without explicit quantification.
    - Silence means the absence of explicit syntax: `()`, `[]`, `{}`, `?`.

  - Otherwise, equality is required:
    - Comparison made after dropping any degenerate group.
    - Comparison is done with own-quantifier (not quantification coming from
      enclosing groups/variant).

  - This analysis applies to the Opt's quantifiers; parameters are a separate
    dimension.

__DETAILS_TO_MOVE__:

  - Why allow opt-specs to be silent regarding their own-quantifier? Why not
    be strict and say that the opt-spec and variant must fully agree?

    - If a user needs variant(s) in their spec, they must be the authoritative
      place for quantification. A single opt-spec cannot express all of the
      quantification implications that can come from an enclosing
      group/variant.

    - But in a spec with variants, it is a user convenience to be able to list
      their opt-specs simply without the noise of quantifiers already
      expressed in variants.

    - In addition, Argle's default help text will likely follow the precedent
      of other libraries in presenting opt-descs as unquantified.

  - Why not allow a looser policy regarding quantifier compatibility --
    something less than own-quantifier equality? Some rejected alternatives:

    - Allow only widening or narrowing:
      - There's no principled direction.
      - Adding `?` (non-greedy) adds syntax but narrows what is accepted.
      - And it does not address blatant conflicts: `{2-4}` vs `{7-8}`?

    - Last config wins:
      - Here the opt-spec would override the variant.
      - Adds spec ambiguity (for the user) and gains them nothing.

    - Variant is authoritative:
      - This rule has some logic: the variants can express the full
        quantification picture, while opt-specs cannot.
      - But allowing outright conflicts between variant and opt-spec is a real
        cost for the user -- one that comes with no obvious convenience (unlike
        the real convenience provided by the silence-allowed policy noted
        above).

  - Why not require opt-specs to be silent on quantification?

    - Because the most common usage pattern will be a spec with only
      opt-specs, where users will necessarily need to supply explicit
      quantifiers.

### opt-spec-matching-parameters: Opt-spec matching: parameter compatibility

Opt-spec matching and parameter compatibility:

  - The opt-spec's parameters and those of the matching Opts must be equal or
    one side can be silent (see P21).
    - This analsysis is also subject to the mixed-bag rule.

  - The equality test:
    - Covers the full parameter structure (count, order, names, groups,
      alternation, and quantifiers).
    - Comparison is after normalization (degenerate groups dropped).

  - The silence test:
    - Requires no use of parameter syntax (ie, just a bare option).

  - Choices within a parameter are a separate dimension (see __).

__DETAILS_TO_MOVE__:

  - Why allow parameter silence for the matched Options from the variants?
    - It allows a user to express variants compactly and fill in details in
      one place -- the opt-specs. Or the reverse.
    - This kind of logic for the equal-or-silence appears in various places.

  - Clean-ups elswhere:

    - The three cases in `conflict-parameters` (`misc/policies.md:454`) are
      all errors under this draft, so that raw note could be marked resolved.

### opt-spec-matching-choices: Opt-spec matching: choice compatibility

Choice compatibility analysis:

  - General policies for choices are similar to those of other dimensions:

    - Silence or equality.
      - Silence: based on presence of explicit choice syntax.
      - Equality: set-equality (between S and V below).

    - No mixed bags.
      - The relevant VarInputs from the matched Opts must be consistent:
        choice-free or choice-bearing.

  - Positional:
    - S: opt-spec choices.
    - V: union of choices from the matched Positionals.

  - Parameter:
    - S: opt-spec choices.
    - V: union of choices across relevant Parameters from matched Options.
      - Relevance is straighforward, based on position.

__DETAILS_TO_MOVE__:

  - For choice compatibility in opt-spec matching, why does Argle unify
    (create a union of) the choices from the variants?

    - Under the previous opt-independence policy, the lone exception was
      unification for Opts with choices.

      - The main driver of the exception: typical subcommand program (eg git).

        - The primary `<command>` positional seems like it should be a unified
          Opt: it drives variant-based grammar.

        - And one would want behavioral consistency between these two:
          - Separate variants: `<step=start>` and `<step=stop>`.
          - One variant: `<step=start|stop>`
          - If the second is a unified Opt, shouldn't the first be?

    - But strict opt-independence has real benefits.

      - The union of choices from the variants allows Argle to be strict and
        still support a common use case.

## help-text: Help text

### documenting-choices: P9: Documenting choices

How choices are documented in grammatical parts of Argle help text:

  - Relevant parts:
    - Usage text.
    - The grammatical portion of opt-descs.

  - Multiple choices:
    - Display the VarInput.name, not the choices.
    - Document choices by appending them to the opt-desc help text.

  - Single choice:
    - Display the choice as a literal.
    - Common example: the action in a subcommand program.

__DETAILS_TO_MOVE__:

  - README.md:427 and README.md:447 show `<red|green|blue>` in usage and `<>`
    in the opt-desc, with choices as `red, green, blue`.

### help-text-autogen-opt-descs: Help text: auto-generated opt-descs

Auto-generated opt-descs:

  - If no opt-specs, Argle will auto-generate opt-descs.

  - If user supplies some opt-specs, but not an exhaustive list, Argle will
    append an "Arguments" section listing the missing opt-descs.

  - Via the API, user can request:
    - No auto-generation of missing opt-descs.
    - Raise if the user's opt-descs are not exhaustive.

__DETAILS_TO_MOVE__:

  - Why does Argle auto-generate opt-descs by default?

    - It is probably the behavior most users want.

    - It is the only mechanism by choices will be documented, given Argle's
      defaults.

### help-text-slots: P11: Help-text slots

User need ways to control placement of Argle-generated documentation:
  - Program info:
    - Program name.
    - Version.
  - Opt attributes within an opt-desc's help text:
    - Choices.
    - Default.
    - Type.
  - Auto-generated opt-descs.

The mechanism to support that: slots:

  - Spec syntax for slots:
    - Name in braces: `{SLOT_NAME}`
    - Braces alone do not signal a slot: the full constuct is required.
    - To include literal text in a spec that looks like a slot, backslash the
      construct: `\{literal}`

  - Some built-in slots:

        {usage}       | Usage text
        -----------------------------------------------
        {opts}        | All Opts
        {options}     | Options
        {positionals} | Positionals
        {opts_other}  | Other Opts (not in opt-specs)
        -----------------------------------------------
        {default}     | Opt default
        {choices}     | Opt choices
        {prog}        | Program name
        {version}     | Program version

Slots will be inserted blockwise or inline:
  - Some slots will require one or the other.
  - Others might be flexible, depending on context within the spec:
    - Slot on its own line.
    - Slot inside a line of text.

User can register:

  - Custom slots.
    - With various mechanisms for supplying data needed by the slot:
      - Blob of text.
      - List of relevant Opts.
      - Etc.

  - Slot hooks:
    - A function to be called when a slot needs its data.

    - Takes:
      - Context instance (same as dispatch).

    - Returns:
      - Relevant data to fulfill the slot.
      - Can vary by slot:
        - `str`: text with default handling (wrapped).
        - Text object: text plus instructions (eg `wrap=False`).
        - Opts selection: a query result or query-path.
    
    - Key point:
      - Slot hooks do not munge generated help text.
      - They receive context and return data.

### sub-specs: Sub-specs policy

__HERE__

We do want to support per-choice help text.

Per-choice help text must be done via sub-specs. Applies to both parameters
(the old policy) and now positionals (the new policy to make things consistent
and to ensure that this help text has sufficient context for end-users).

- A per-choice sub-spec must name exactly one choice.
  - If the VarInput allow multiple choices synonyms, the user can either
    document each choice via individual sub-specs.
  - Or the user can document one choice in a sub-spec and mention the synonyms
    in the help text for that sub-spec.

- Per-choice help for a parameter requires a named parameter (eg
  `<c=red|green>`). A choices-only parameter (`<red|green>`) cannot be
  reached by a sub-spec, because `<red>` reads as a parameter name.

Sub-specs and opt-spec matching compatibility:

  - The parent opt-spec is analyzed for matching compatibility.

  - Sub-specs do not affect that analysis. Rather, if an opt-spec is valid and
    matches some Opts, and if it also has sub-specs, then each sub-spec is
    checked for validity -- not for matching compatibililty. The check
    involves choices and other matters, but it is not a matching analysis.

  - A sub-spec does select within the matches. For example, in a typical
    subcommand program where the parent opt-spec matched various `<cmd=foo>`
    Opts from the variants, each sub-spec selects the relevant Opts, based on
    the choices it documents.

  - A sub-spec must be compatible with the parent opt-spec and, indirectly,
    with the variant Opts matched by the parent.

  - Choices compatibility:

    - Call C the set of choice(s) documented in the sub-spec.
    - C must be a subset of E, the set of choices from the parent opt-spec and
      the Opts matched by it.
    - With several matched Opts, the sub-spec attaches to the Opts whose
      choices include those in C.

## api: API

### api-reads: P14: API reads

Reading an attribute from a query result unifies across its OptNodes: the
distinct union of values, in spec order.

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

### query-result-repr: P18: Query-result repr

A repr is a diagnostic, so it shows the raw Opts, each with its path (P17),
not the unified view. Eg:

    Opts([
        Positional(cmd, choices=[search], path=search.cmd),
        Positional(cmd, choices=[list], path=list.cmd),
    ])

- The unified view remains available via attribute reads (P14).

## anonymous-parameters: Anonymous parameters are supported

Anonymous parameters are supported:

  - The are allowed in spec syntax:
    - In a choices-only situation: `--color <red|green|blue>`.
    - Or purely anonymous: `--point <> <>`.

  - But they are displayed in usage/help text via first-letter of Option.name;
    - Spec: `--point <> <>`.
    - Usage/help:
      - Default: `--point <p> <p>`
      - Optional: `--point <> <>` (if user requests via API).

  - Internally, the Parameter instance remains anonymous:
    - The first-letter is a display policy, not a default Parameter.name.

__DETAILS_TO_MOVE__:

  - Why does Argle allow anonymous parameters at all?

    - After all, we searched and found no prior art for anonymous parameters
      among a variety of Unix commands and Git subcommands.

    - In Argle, they are a logical consequence of something we do want to
      support: choices-only parameters, which are anonymous by construction.

    - And choices-only parameters does have precedence in other libraries (eg,
      argparse) and programs (eg, `git diff --diff-algorithm` and several
      other git commands).

  - Why does Argle allow anonymous parameters as spec input but use
    first-letter of Option.name as the default display in help text output?

    - Precisely because the device has no prior art.

    - Anonymous is a logical alternative within the Argle spec syntax, but is
      quite out in left field as a device in help text.

    - And Argle defaults to first-letter of Option.name because the argparse
      use of the full Option.name (shown below) is repetitive, verbose, and a
      bit illogical: if "point" refers to the whole Option, the parameter
      values should have a different display.

          # Spec.
          --point <> <>
          --color <red|blue|green>

          # Default help text.
          --point <p> <p>
          --color <c>

          # Help styles available as configuration options.
          --point <point> <point>   # Full name (argparse style).
          --point <> <>             # Anonymous, for the bold.
          --color <red|blue|green>  # Choices as display.

  - Why does Argle allow anonymous parameters, but not positionals?

    - Because a top-level Opt requires a name: Positional is an Opt; Parameter
      is a child of one.

## dispatch-opt-independence: P15: Dispatch and Opt independence

- Default: dispatch unifies Opts by name. Argle calls a dispatch
  function at most once per (NAME, FUNC, RESULT): the matched Opt's
  name, its dispatch function, and the Result holding the Opt's value
  (the innermost Result, when groups have dests).

- Example: `<x> <x>` yields two Opts in the grammar. With dispatch
  configured on `<x>`, both matches share NAME, FUNC, and RESULT, so
  the function is called once.

- Example: in EX_NAB, each repetition of the `commands` group has its
  own inner Result. Matches of `<cmd>` differ in RESULT, so dispatch
  occurs once per repetition.

- NAME is in the key so that different Opts sharing a function (eg
  `--foo` and `--bar` both using `blort()`) are still called
  separately.

# other-material: Other material to edit, move, delete

- `misc/spec-syntax.md:173` and `misc/spec-syntax.md:176` need rewording to
  match. Line 176 currently reads as permitting the repeats that P19 forbids.

- P20 assumes variants and partials can be scope targets by name. The
  variant-naming form (`clone : ...`, from
  `misc/examples/argle-mock-ups/argle-repo.py:47`) is not yet in
  `misc/spec-syntax.md`.

misc/notes.txt:2013 — sub-specs configure "a choice of a Positional or Parameter"
- ok

misc/notes.txt:2058 — positional sub-spec example (`<speed=fast|slow>`)
- ok

misc/notes.txt:4489 — positional sub-spec example (`<action=go|stop>`)
- ok

misc/spec-syntax.md:418 — the doc's endorsement of unscoped per-choice opt-specs
- would need adjustment

misc/examples/argle-mock-ups/argle-repo.py:61 — `Commands :::`, no parent line
- help text would be better if we changed policy

misc/examples/spec-vs-api/job-client-argle:37 — no parent line
- ditto

misc/examples/argle-mock-ups/blort.py:201 — NOTE_810, no parent line
- ditto

misc/examples/argparse-vs-argle/wrangle:85 — parent `<task>` line already present
- is consistent with a revised policy

README.md:324 — same as wrangle
- ditto

