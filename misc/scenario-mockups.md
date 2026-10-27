
<!--

# sc-scenario-mockups: Scenario mockups
  ## sc-background: Background and problem-solving strategy
  ## sc-criteria: Relevant criteria
  ## sc-scenarios: Scenarios
    ### scenarios-template: Scenarios template
    ### sc-positional-choices: S1: positional with choices; variants-only
    ### sc-partial-opt-spec: S2a: S1 plus a partial opt-spec and an epilogue; no slot
    ### sc-other: OTHER
# argparse-messages: Reference: argparse messages
  ## sc-argparse-msg-format: Message format
  ## sc-argparse-common-msgs: Common messages
  ## sc-argparse-msg-examples: Message examples

-->

# sc-scenario-mockups: Scenario mockups

## sc-background: Background and problem-solving strategy

These scenarios started as a way to address some policy gaps/problems related
to Opt independence-vs-unification, based on Opt.name. The idea was to focus
on concrete mockups for various scenarios and see if coherent policy would
emerge from the mockups.

Each mockup would document inputs and outputs:
  - spec
  - API calls if needed
  - usage text
  - help text
  - error reporting for arg parsing
  - maybe other output surfaces: API querying, etc.

## sc-criteria: Relevant criteria

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

## sc-scenarios: Scenarios

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
    - Add during a dedicated later pass, after usage and help text are mocked
      up across the scenarios.
    - For each scenario, consider common and weird error cases.
    - Most will be obvious once a general approach exists; add error examples
      only where they are interesting.

  - API calls:
    - Add to "Notes" sub-section only if noteworthy.

  - Result() mockup and matching end-user input:
    - Add to "Notes" sub-section only if noteworthy.

### scenarios-template: Scenarios template

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

### sc-positional-choices: S1: positional with choices; variants-only

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

### sc-partial-opt-spec: S2a: S1 plus a partial opt-spec and an epilogue; no slot

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

### sc-opts-slot: S2b: S2a plus an `{opts}` slot

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

### sc-other: OTHER

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


# argparse-messages: Reference: argparse messages

## sc-argparse-msg-format: Message format

    usage: USAGE_TEXT
    PROG: error: MSG

## sc-argparse-common-msgs: Common messages

    Missing required args | the following arguments are required: x, n, --user
    Invalid conversion    | argument n: invalid int value: 'abc'
    Invalid choice        | argument z: invalid choice: 'D' (choose from 'A', 'B', 'C')
    Excess positional     | unrecognized arguments: extra
    Unknown option        | unrecognized arguments: --blort
    Missing parameters    | argument --color: expected one argument
    Mutually exclusive    | argument --yaml: not allowed with argument --json
    Ambiguous abbrev      | ambiguous option: --ver could match --verbose, --verify
    Invalid subcommand    | argument cmd: invalid choice: 'fubb' (choose from 'add', 'rm')

## sc-argparse-msg-examples: Message examples

Source:

    misc/scripts/argparse-workshop

Examples:

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

