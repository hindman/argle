
<!--

# Classes and attributes
  ## Overview
  ## Parser
  ## Section
  ## Grammar
  ## Query
  ## Quantifier
  ## Variant
  ## Group
  ## Opt and children: overview
  ## Opt
  ## Positional
  ## Option
  ## Literal
  ## VarInput
  ## Parameter
  ## Choice
  ## Result
  ## SpecParser
  ## RegexLexer
  ## TokType
  ## Token
  ## ParseElem
  ## State
  ## ArgResult
  ## Target

-->

# Classes and attributes

## Overview

  - User-facing entities:

        Parser
        Section
        Grammar
        Variant
        Group
        Opt
            Positional
            Option
            Literal
        Parameter
        Choice
        Result
        Query
        Section
        Heading
        OptSpec

  - Relationships among user-facing entities:

        Parser
            sections      = List[Section]      # 1+   # Usage exists even with spec=''
            grammar       = Grammar            # 1    # Ditto.
                variants  = List[Variant]      # 0+
                    elems = List[Group or Opt] # 0+

            parse(ARGS) -> Result

        Group:
            elems = List[Group or Opt]         # 0+

        Opt:
            elems = list[Choice or Parameter]

        Parameter:
            elems = list[Choice]

  - Objects used during spec-parsing:

        SpecParser | Parses a spec, returns Grammar.
        RegexLexer | Lexer used by SpecParser.
        TokType    | Token types given to lexer.
        Token      | Emitted by lexer.
        ParseElem  | Emitted by parser functions. Later assembled into Grammar.

  - Objects used during argument parsing:

        State
        ArgResult
        Target

  - Entities used only for notation:

        PartialUsage      | Group
        Positional        | Opt
        PositionalVariant | Opt
        ParameterVariant  | Opt

## Parser

  - Class will likely have various getters or query functionality to make it
    easy to configure specific grammar elements. Users should not have to
    manually navigate the Grammar hierarchy.

  - Attributes:

        # The grammar.
        spec: str
        grammar: Grammar
        sections: list[Section]

        # Typically inferred by Argle.
        prog: str

        # Parsing mode: regular or no-config [maybe others later].
        mode: str

        # Namespace to hold help-text formatting defaults/behavior.
        # Deferred for now.
        format: HelpTextFormat

  - API:

    - Notation:

          p = Parser(SPEC)

    - Parsing:

          p.parse(args = None, mode = ...)

      - Returns a Result or raises.
      - The method can temporarily use a different mode than the Parser.mode.

    - Querying grammar elements:

          p.query(*paths, **kws) => Query

      - See grammar-querying-api

    - Configuring grammar elements:

      - See parser-config-api

    - Configuring one attribute across multiple elements:

          p.query(*paths).config_each(attr_name, **kws)

      - Convenience method to set an attribute across multiple elements.

    - Obtaining help text or text for the error from most recent parse():

          p.help_text(section...)
          p.error_text()
          p.exception()

    - Actions like printing or exiting.

          p.warn(msg)
          p.help(section...)
          p.error(msg = None, code = 1)
          p.exit(msg = None, code = 0)

## Section

  - Used to create labeled groups of Opt for help text purposes.

  - Attributes:

        # Symbolic name used in API.
        name: str

        # Section title in help text.
        title: str

        # Section content.
        # - Opts belonging to the section.
        # - Hand-crafted help text (probably needs more modelling).
        opts: list[Opt]
        text: str

## Grammar

  - Attributes:

        variants: list[Variant]

  - API:
    - See grammar-querying-api

## Query

  - Sequence object returned by Grammar.query().
  - Holds the Grammar elements satisfying the search parameters.
  - Supports bulk configuration.

  - Attributes:

        elems: list[Group or Opt or Parameter]

  - API:

    - Notation:

          p = Parser(...)
          q = p.query(...)

    - Apply configuration to grammar elements.

          q.config(...)

    - Subquery to filter down further:

          q.query(...) => Query

## Quantifier

  - Represents any valid input value for nargs or ntimes.

  - Attributes:

        m: int
        n: int
        required: bool
        greedy: bool

## Variant

  - Attributes:

        name: str .
        elems: list[Group or Opt]
        ntimes: Quantifier

## Group

  - Represents spec-syntax enclosed by brackets.
  - Primary purposes:
    - Ability to quantify groups of grammar elements.
    - Mutual exclusion for such groups.
    - Using the dest to organize nested Result data.
    - Using the name to represent groups of Opts symbolically
      in usage-text.
    - Ability to apply validation to groups of Opts.

  - Attributes:

        # Name and dest:
        # - name comes from the spec.
        # - dest defaults to name.
        # - If name is set, it is used to represent the
        #   group in usage-text.
        name: str
        dest: str

        # Quantifier and group-level validation.
        ntimes: Quantifier
        validate: callable

        # Mutual exclusion: true for groups defining alternatives.
        mutex: bool

        # Child elements.
        elems: list[Group or Opt]

## Opt and children: overview

  - Opts and their children:

        Positional > Choice
        Option > Parameter > Choice
        Literal > None

## Opt
  - Base class for Positional, Option, or Literal.
  - Some of the common attributes listed for each subclass (below) might be
    implemented at the Opt level (TBD).
  - Also see: opt-and-varinput-configuration

## Positional
  - Subclass of Opt.

  - Attributes:

        spec: str
        name: str
        dest: str
        help: str
        nargs: Quantifier
        choices: list[Choice]
        --
        hide: bool
        anchor: bool
        dispatch: list[callable]
        --
        default: object
        factory: callable
        convert: callable
        validate: callable

## Option

  - Subclass of Opt.

  - Attributes:

        spec: str
        name: str
        dest: str
        help: str
        nargs: Quantifier
        ntimes: Quantifier
        elems: list[Parameter or Group]
        --
        hide: bool
        anchor: bool
        dispatch: list[callable]
        --
        aliases: list[str]
        priority: bool                   # Flags only.
        negaters: list[Option]

## Literal

  - Subclass of Opt.

  - Attributes:

        spec: str         # The literal value (no backquotes).
        anchor: bool      # Always True.

## VarInput

  - Base class for a variable-input as a configurable unit.
  - Sub-classes: Positional or Parameter.
  - Also see: opt-and-varinput-configuration

## Parameter

  - Attributes:

        spec: str
        name: str
        dest: str
        help: str
        nargs: Quantifier
        choices: list[Choice]
        default: object
        factory: callable
        convert: callable
        validate: callable

## Choice

  - Attributes:

        spec: str      # The literal value.
        help: str

## Result

  - Data object returned to end-user by Parser.parse().

  - An iterable mapping-like object with destinations as the attributes.

  - In more complex grammers the top-level Result returned by parse() might
    contain nested Result instances (eg, a Group with a quantifier of 2+).

## SpecParser

  - Attributes:

        lexer     | Lexer.
        handlers  | Sequence of token-stream handlers.
        curr      | Managed by the mixin.
        prevpeek  | .

  - API:

        parse()
        eat()
        error()

## RegexLexer

  - General-purpose regex-based lexer.

  - Attributes:

        text      | The text to be lexed.
        toktypes  | Sequence of TokType.
        pos       | Current index of the lexer.
        mxpos     | Last index of the text.
        iseof     | Becomes True when text exhausted.

  - API:

        See old.py implementation and modifications in draft.py.

## TokType

  - Internal data object given to a lexer.

  - Attributes:

        name  | Name of token.
        regex | Regex to match the token.
        emit  | Whether to emit back to parser [default: True].

## Token

  - Simple internal data object emitted by a lexer.

  - Attributes:

        toktype | TokType of the token.
        value   | Corresponding token text.
        pos     | Position (where matched)
        line    | Line number.
        col     | Column number.

  - Kinds:

        Same as TokType.

## ParseElem

  - Simple internal data object emitted by the parsing phase of
    SpecParser.parse(). Subsequent work in that method will convert the
    ParseElem into a user-facing Grammar.

  - Attributes for each kind of ParseElem will vary.

  - Kinds:

        variant
        group
        opt
        quantifier
        choices
        parameter
        literal

## State

  - An internal data object used during argument parsing. See
    arg-parsing-algo notes.

## ArgResult

  - An internal data object used during argument parsing. See
    arg-parsing-algo notes.

## Target

  - A data object used during argument parsing to store the information
    ultimately returned as a Result to end user.

  - For the applicable parsing interpretation, a Target contains information
    about all relevant Opt/Pos and values parsed so far.

  - Attributes:

        poss | List[Pos]
        opts | Dict[Opt]
        vals | Dict[DEST -> VAL]

