<!--

  # todos: TODOs
  # argle-policies: Policies
    ## grammar: Grammar and identity
      ### grammar-opt-independence: P0: Strict Opt independence in the grammar
      ### grammar-vs-surfaces: P13: Terminology: grammar vs surfaces
      ### surface-unification: P101: Opts are generally unified at surfaces
      ### opt-path-property: P17: Add an Opt.path property
    ## opt-specs: Opt-specs and matching
      ### opt-spec-matching: P16: Opt-spec matching
      ### opt-spec-matching-names: Opt-spec matching: names and aliases
      ### opt-spec-matching-uniqueness: P19: An Opt cannot be matched more than once
      ### opt-spec-matching-no-match: P20: Opt-specs that match nothing
      ### opt-spec-matching-quantifier: Opt-spec matching: quantifier compatibility
      ### opt-spec-adds-parameters: P3: Opt-specs can add parameters
      ### same-name-choice-choiceless: P8: Same-named choice-bearing and choiceless Opts
      ### raw notes that need a home (were in reboot-status.md)
        #### conflict-parameters: SPEC_ISSUE: variant vs opt-spec conflicts: parameters
        #### conflict-choices: SPEC_ISSUE: variant vs opt-spec conflicts: choices
    ## choices: Choices
      ### rough notes that need a home
      ### per-choice-help: P2: Per-choice help text
      ### per-choice-help-sub-specs: P5: Per-choice help text via sub-specs
      ### variant-choices-authoritative: P6: Variant-declared choices are authoritative
      ### documenting-choices: P9: Documenting choices
    ## help-text: Help text
      ### help-text-defaults: P10: Help text defaults
      ### help-text-slots: P11: Help-text slots (tentative)
      ### slot-hooks: P12: Slot hooks (tentative)
    ## api: API
      ### api-reads: P14: API reads (tentative)
      ### query-result-repr: P18: Query-result repr (tentative)
    ## dispatch: Dispatch
      ### dispatch-opt-independence: P15: Dispatch and Opt independence (tentative)
  # other-material: Other material to edit, move, delete
    ## opt-spec-unmatched-follow-up: Follow-up notes (P19 and P20)
    ## per-choice-help-edit-list: Edit list P5: per-choice help must be in sub-specs
    ## audit-notes: notes on audit

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
    Error msgs     | TBD
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
    - A mixed bag sends mixed signals: the silent Opt may be deliberate (a
      flag) or an omission, and Argle cannot tell which.

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

  - Ordering of aliases and option name in an opt-spec affects but might not
    dictate ordering/presentation in generated help text (the latter can be
    configured).

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

    - The user's goal can be achieved in a better way oriented about the needs
      of display.

    - Keeping Opt configuration single-source:
      - Simplifies Argle policy.
      - Provides clarity to users.

    - Showing an opt-desc in multiple spots is a display concern:
      - Tentative mechanism: slots (see P11).

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
    - Multiple: opt-spec scope must point to one partial or variant.

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

  - This analysis applies to the Opt, not quantifiers on its parameters.

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

__HERE__

### opt-spec-adds-parameters: P3: Opt-specs can add parameters

We do want opt-specs to be able to add parameters to an Option. This is
similar to P1 because it allows for a compact/readable command-line grammar,
leaving the fleshing out to opts-specs.

### same-name-choice-choiceless: P8: Same-named choice-bearing and choiceless Opts

Matching stays based on name, kind, and scope (adding choices to the matching
criteria would turn conflicts into silent non-matches). If an unscoped
opt-spec matches both kinds of Opt (eg `<x=A|B>` and a bare `<x>` in the
variants):

- Help only (eg `<x> : help`): allowed. Both Opts get the help text. The
  duplication is visible in the help output, and the user can fix it
  with a scope.

- Names choices, itself or via sub-specs: error; use a scope. Otherwise
  the choiceless Opt would silently gain the choices, a behavior change
  that the help output does not reveal.

### raw notes that need a home (were in reboot-status.md)

#### conflict-parameters: SPEC_ISSUE: variant vs opt-spec conflicts: parameters

What about opt-specs that completely change the parameters of an Option?

    --bar <b1> <b2>        # In a variant
    --bar <b1> [<b2>]      # In an opt-spec
    --bar <x> <y> <z>      # Ditto -- but more divergent

#### conflict-choices: SPEC_ISSUE: variant vs opt-spec conflicts: choices

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

## choices: Choices

### rough notes that need a home

Rough text and notes:

  - Choices:

        Variant choices | Opt-spec choices | Result
        ---------------------------------------------------------------
        none            | none             | OK: no choices involved
        none            | S                | OK: opt-spec supplies S
        V               | none             | OK: opt-spec silent, so V stands
        V               | S                | OK only if S == V

        Where:
          - S is the set of choices supplied by the opt-spec.
          - V is the union of choices from matched Opts.
          - S and V are tested for set equality.

  - No mixed-bag scenarios:

    - An opt-spec with choices must match either (a) choiceless Opts, or (b)
      choice-bearing Opts, but (c) never a mixed bag.

    - Admitting that such uses cases are super rare, when we concoct mixed-bag
      scenarios, we have a hard time discerning a clear user intent, so the
      error forces the user to be specific.
      - The user can use scopes in the opt-specs (to avoid a mixed-bag match)
        or add choice(s) to the choiceless Opts in the variants (making the
        bag no long mixed)

    - The no-mixed-bag policy is not just sticklerism.
      - If same-name Opts in variants all have choices, that's a signal the
        user intends them to be unified for configuration purposes.
      - Ditto if same-name Opts in variants are choiceless.
      - But the mixed-bag situation conveys mixed signals -- hence the error
        to force some clarity from the user.

Rough notes on sub-specs:

  - NOTE: Perhaps sub-specs should be addressed in a separate policy.

  - A sub-spec attaches to the immediately preceding parent opt-spec.

  - A sub-spec must be compatible with the parent opt-spec and, indirectly,
    with the variant Opts matched by the parent.

  - Choices compatibility:

    - Call C the set of choice(s) documented in the sub-spec.
    - C must be a subset of E, the set of choices from the parent opt-spec and
      the Opts matched by it.
    - With several matched Opts, the sub-spec attaches to the Opts whose
      choices include those in C.

### per-choice-help: P2: Per-choice help text

We do want to support per-choice help text. That's a feature I have wanted
many times as a long-suffering argparse user.

### per-choice-help-sub-specs: P5: Per-choice help text via sub-specs

Per-choice help text must be done via sub-specs. Applies to both parameters
(the old policy) and now positionals (the new policy to make things consistent
and to ensure that this help text has sufficient context for end-users). See
the edit-list we assembled in a separate section below.

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

### variant-choices-authoritative: P6: Variant-declared choices are authoritative

If a variant declares choices for a VarInput, they are authoritative.
Opt-specs (regular or sub-spec) may name only those choices; naming any other
is an error. Not every choice needs to be documented. If the variant declares
no choices, the opt-specs supply them.

- NOTE: this is currently under review and might change.

- When an opt-spec matches several Opts (see P16), the authoritative
  set is the union of their choices (cf P14). Restating choices only
  validates and documents: it never changes any Opt's own choices. If
  the variants declare no choices, the opt-spec does supply them, by
  broadcast, subject to P8.

- A parent (regular) opt-spec must either restate the full
  authoritative set or say nothing about choices. A subset or superset
  is an error. Agreement means set equality, so order does not matter.

      --color <c=red|green|blue> : OK (full agreement)
      --color <c> : OK (silent about choices)
      --color <c=red|green> : Error (subset)

- Sub-specs name choices one at a time (see P5) and need not cover all
  of them. A sub-spec attaches to the matched Opt(s) whose choices
  include the named choice, not to every match.

- Tentative: help-text display order of choices comes from the
  sub-specs if any, otherwise from the variants.

### documenting-choices: P9: Documenting choices and anonymous parameters

By default, Argle does not list plural choices in usage text or in the formal
portion of opt-descs. Instead, it appends them to the Opt's help text (see
scenario-mockups.md).

  - A single choice displays as a literal in usage text (eg an arg-variant
    like `<cmd=merge>`, as in `git merge [<options>]`).

Anonymous parameters are supported:

  - They follow from supporting the choices-only form (`<red|green>`), which
    is anonymous by nature. The bare form (`<>`) is not forbidden.

  - Display default: the first letter of Option.name (the derived name, eg
    `-x --extract <>` displays as `--extract <e>`). Applies to anonymous
    parameters that are choiceless or have plural choices.

  - Usage text and opt-descs show the same placeholder.

  - The letter is a display element only, not a Parameter.name or dest. No
    uniqueness or fallback rules: a user who dislikes the display names the
    parameter.

  - Configurable alternatives: the full Option.name (`--point <point>`) or a
    literal anonymous placeholder (`--point <>`).

Example (defaults):

    # opt-spec
    --color <red|green|blue> : Highlight matching text

    # usage text
    [--color <c>]

    # opt-desc
    --color <c>     Highlight matching text [red|green|blue]

__DETAILS_TO_MOVE__:

  - Why not display `<>` by default? No prior art: no usage or help text in
    git, common man pages, or documented conventions uses empty placeholders.
    The choices-only form, by contrast, has precedent (argparse displays
    choices in place of a metavar).

  - Why first letter rather than the full Option.name (the argparse default)?
    `--width <width>` is redundant and verbose. The letter keeps opt-descs
    compact, and the escape hatch is ordinary.

  - Why allow `<>` at all? Supporting choices-only already requires the
    machinery for nameless parameters (Result shape, display). Forbidding the
    bare form would be a best-practice rule with no other rationale.

Follow-up notes:

  - README.md:427 and README.md:447 show `<red|green|blue>` in usage and `<>`
    in the opt-desc, with choices as `red, green, blue`; align later.

  - scenario-mockups.md S6 can reference P9 as its resolution.

## help-text: Help text

### help-text-defaults: P10: Help text defaults

- If user supplies only variants (no opt-specs), Argle will generate a
  typical listing of opt-descs. Why this is a helpful default:

  - Following git, we intend to display VarInput choices in opt-desc
    help-text, not in the opt-desc CLI-grammar (see P9).

  - If Argle did not generate opt-descs in this scenario, choices would
    remain undocumented. So the auto-generated opt-descs provide a home
    for the listing of choices.

- If the user supplies some opt-specs but not a complete list of them, the
  generated help text will follow the presentation/ordering of the
  opt-specs (and other help-text elements). Then at the end Argle will
  append an "Arguments:" section listing the opt-descs for which the user
  did not supply corresponding opt-specs.

  - Why auto-generate and append by default? Same reason as above: it will
    be the only means of displaying choices.

  - The API will allow users to request things like:
    - Do NOT auto-generate the missing opt-descs.
    - Raise if the user's opt-descs are not exhaustive (meaning: all Opts
      in the variants were matched by an opt-spec).

### help-text-slots: P11: Help-text slots (tentative)

- Some of these notes are questionable:
  - Re-assess and edit.
  - Render-once not needed: eg {opts} vs {opts_rest} and/or broad vs explicit.

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

- To support complex needs, favor a user-slot where their callable supplies
  the text or data needed to drive the slot content.

### slot-hooks: P12: Slot hooks (tentative)

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

## api: API

### api-reads: P14: API reads (tentative)

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

### query-result-repr: P18: Query-result repr (tentative)

A repr is a diagnostic, so it shows the raw Opts, each with its path (P17),
not the unified view. Eg:

    Opts([
        Positional(cmd, choices=[search], path=search.cmd),
        Positional(cmd, choices=[list], path=list.cmd),
    ])

- The unified view remains available via attribute reads (P14).

## dispatch: Dispatch

### dispatch-opt-independence: P15: Dispatch and Opt independence (tentative)

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

## opt-spec-unmatched-follow-up: Follow-up notes (P19 and P20)

- `misc/spec-syntax.md:173` and `misc/spec-syntax.md:176` need rewording to
  match. Line 176 currently reads as permitting the repeats that P19 forbids.

- P20 assumes variants and partials can be scope targets by name. The
  variant-naming form (`clone : ...`, from
  `misc/examples/argle-mock-ups/argle-repo.py:47`) is not yet in
  `misc/spec-syntax.md`.

- The raw note `opt-spec-conflicts` (below) is resolved by P19 and can be
  marked as such or removed.

## per-choice-help-edit-list: Edit list P5: per-choice help must be in sub-specs

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

## audit-notes: notes on audit

Contradictions:

  1. P8 and help grouping. P8 allows `<x> : help` across `<x=A|B>` and a bare
     `<x>` because "the duplication is visible in the help output." But under
     the help grouping we've discussed (auto-generated entries grouped by name
     and kind), those two Opts would merge into one entry, so nothing would be
     visible. One of the two needs to give.

  2. What "Opt" means. P14 says OptNode, P0 says "each Opt occurrence ... is a
     distinct Opt," and P15–P18 use "Opt" for the per-node thing. Pick one
     usage for the policies.

Obsolete or stale:

  3. P7 is superseded. In the new layout I'd move it to the details section,
     or drop it.

  4. P6's "NOTE: currently under review" may now be stale, since P6 was just
     revised for P0.

  5. P13's status lines: "Config read: maybe resolvable via P14" (P14 now
     exists), tab-completion (resolved), and help and errors still marked
     ASSESS/RESOLVE (now deferred to the mockups).

  6. P11 says the default tail is "effectively a final `{opts}`." S2b refined
     that: `{opts}` renders entries with no heading, and the tail is a heading
     plus `{opts}`. P11 wasn't updated.

Overlaps:

  7. The default tail is described in both P10 and P11. P10 should own the
     default and P11 the slot mechanics.

  8. The single-choice-literal rule appears in both the P9 note and P13's
     usage bullet.

  9. P0's "surfaces (help, errors, Result)" is the short version of P13's full
     list.

Missing or orphaned:

  10. Help grouping of auto-generated opt-descs (by name and kind, with
      choices unioned) was discussed but never recorded as a policy. It's
      needed for item 1 and for the mockups.

  12. P12's open item "default split of positionals and options" already has a
      design in notes.txt: the `opt_listing_heading` setting with
      `unified`/`by_kind`/`minimal`, where unified uses "Arguments"
      (misc/notes.txt:1052). That's worth linking.

