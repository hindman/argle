# Spec syntax

<!--

# Spec syntax
  ## spec
  ## usage-section
  ## section
  ## any-section-title
  ## section-title
  ## scoped-section-title
  ## section-scope
  ## query-path
  ## query-elem
  ## section-content-elem
  ## heading
  ## block-quote
  ## literal
  ## quoted-text3 and quoted-text1
  ## variant
  ## opt-spec
  ## opt-spec-def
  ## opt-spec-elem
  ## opt-spec-group
  ## python-name
  ## valid-name
  ## opt-help-text
  ## variant-def
  ## variant-elem
  ## quantifer
  ## partial-usage
  ## any-group
  ## named-group
  ## group
  ## aliases-and-option
  ## bare-option
  ## option
  ## any-parameter
  ## parameter
  ## choices
  ## choice
  ## parameter-group
  ## positional
  ## opt-mention
  ## var-input
  ## Quoting rules
  ## Whitespace rules
  ## Spec-syntax hierarchy in compact form

-->

## spec

    [usage-section]
    [section...]

## usage-section

    [variant...]
    [section-content-elem...]

- Variants come first and are parsed greedily: any line in the usage-section
  that can be read as a variant is one.

- The variants end at the first heading, block-quote, or opt-spec. After that,
  and in every later section, lines are opt-specs.

- If the first opt-spec could be mistaken for a variant, add a trailing colon
  (an empty opt-help-text) to mark it as an opt-spec.

## section

    any-section-title ::
    [section-content-elem...]

## any-section-title

    section-title | scoped-section-title

## section-title

    title-text

- Text and marker must be on one line.

## scoped-section-title

    section-scope >> section-title

- A section-scope applied to a section is a shortcut for applying the scope to
  all opt-specs within the section (details below).

## section-scope

    query-path

## query-path

    query-elem [. query-elem]...

## query-elem

    glob-char... | digit...

- Can be a name/dest glob pattern or a positive integer.
- glob-char: valid-name characters, plus wildcards (? and *).

## section-content-elem

    [heading | opt-spec | block-quote]...

## heading

    heading-text :::

- The heading-text must be on one line.
- The marker must end the line.

## block-quote

    ```  quoted-text3 ```
    ```! quoted-text3 ```             # No wrap
    ```# quoted-text3 ```             # Spec-comment

- Notes:
    - Opening quote must be first on its line.
    - Triple-quotes can sit on their own line, or not.
    - Quoted-text3 can span multiple lines.

## literal

    ` quoted-text1 `

- A literal does not support: name, dest, or quantifier.

## quoted-text3 and quoted-text1

    (literal-backslash | literal-backquote | quoted-char3)...
    (literal-backslash | literal-backquote | quoted-char1)...

- Where:

      literal-backslash | \\
      literal-backquote | \`
      quoted-char3      | Any char except backquote
      quoted-char1      | Any char except backquote, tab, newline

## variant

    [valid-name[!] :] variant-def

- Marker (!) means partial-variant.

## opt-spec

    [[opt-scope] >>] opt-spec-def [: [opt-help-text]]

- If Opts are declared in variants and later in opt-specs, the two
  configurations are merged:

  - Opt-spec configuration is connected to the relevant Opt from the
    grammar (see opt-independence for details).

  - Opt declared in the grammar can use an abbrievated form (an
    opt-mention), leaving the full configuration to the opt-spec.

- An opt-scope has the same format as a section-scope. The only difference
  is that an opt-scope can be empty (marker only).

- The opt-scope marker (>>) declares a parent-child relationship.

  - With a opt-scope:
    - Parent: Opt from variants.
    - Child: current opt-spec.
    - Declares the Opt to which the opt-spec should be connected.

  - Empty opt-scope:
    - Parent: preceding (non-scoped) opt-spec.
    - Child: current opt-spec.
    - Child configures an Parameter or Choice of the parent.

## opt-spec-def

    opt-spec-group | opt-spec-elem

## opt-spec-elem

    positional | aliases-and-option

## opt-spec-group

    (opt-spec-elem)
    [opt-spec-elem]

- The group cannot be named.
- It only function to support a quantifer.

## python-name

    first-char char...

- Where:

      first-char | letter, underscore
      char       | letter, underscore, digit

## valid-name

- Just like python-name, but char can also be a hyphen.

- Consistent with argparse, hyphen and underscore can be combined,
  adjacent, at the end. Insane but valid: --__foo-_-fubb-_

## opt-help-text

- The rest of the line, plus continuation lines.
- Colon marker without opt-help-text can be used to distinguish opt-spec
  from variant (to avoid ambiguity).

## variant-def

    variant-elem...

## variant-elem

    (
        option |
        positional |
        any-group |
        literal |
        partial-usage |
        choice-sep
    )

- All take a quantifer except:
    - choice-sep (|)
    - literal
    - partial-usage (user can wrap in a group).

- Examples with comments:

      Options:

          -f             # Short.
          --foo          # Long.
          --age <yr>     # Long with parameters (groups can be parameters too).

      Positionals:

          <bar>          # Single.
          <path>...      # With quantifier.

      Literals:

          `hello`        # Becomes a Literal, a limited form of Opt.

      Groups and alternatives:

          ()             # Group.
          []             # Group, optional.
          foo=()         # Named group.
          foo=[]         # Named group, optional.
          |              # Alternatives separator.

      Partial:

          foo!           # Insert foo partial into the variant.

      Quantifiers:

          ...            # Either 1+ or 0+ (latter if the entity is optional).
          {m-n}          # Repetition: m through n, inclusive.
          {m}            # Repetition: exactly m.
          {m+}           # Repetition: m or more.
          ?              # Non-greedy for preceding quantifier.

## quantifer

    triple-dot[?]
    quant-range[?]

- Where triple-dot:

      ...

- Where quant-range:

      {min-max}
      {min}
      {min+}

- Both are non-negative integers.

- The ? marker makes preceding quantifier non-greedy.

## partial-usage

    valid-name!

## any-group

    named-group | group

## named-group

    valid-name = group

## group

    ( variant-elem... )
    [ variant-elem... ]

## aliases-and-option

    [alias...] option

- Where alias = bare-option.

## bare-option

    - first-char
    -- valid-name

- Where first-char is a valid first character in a valid-name.

## option

    bare-option [any-parameter...]

## any-parameter

    parameter | parameter-group

## parameter

    < valid-name >
    < valid-name = choices >
    < choices >
    < >

## choices

    choice [ | choices ]

- Choices mean different things in variants and opt-specs. The syntax is
  the same either way.

- In a variant, choices make a positional or parameter a literal input:
  the end-user must supply one of the listed values, and doing so selects
  that variant (an arg-variant). One choice or several, same mechanism.

  - `<task=grep>`: matches only grep.
  - `<action=set|remove>`: matches either value (see naval-fate).

- In an opt-spec, choices configure the Opt's choices. Listing several
  declares them together; listing one per opt-spec lets each have its own help
  text, and the repeated opt-specs accumulate the full set (see blort,
  NOTE_810).

  - `[--color <red|green|blue>] : Highlight matching text`
  - `<method=first> : Blah blah`

## choice

    valid-name | literal

## parameter-group

    ( parameter... )
    [ parameter... ]

## positional

    < valid-name >
    < valid-name = choices >

## opt-mention

- A term/concept more than a parsing element.
- Consists of Opt.name, with appropriate punctuation.
- Examples:

      <foo>
      --bar
      -b

## var-input

- Variable input provided by the user.
- Primarily an internal term, not user-facing.
- Forms: positional and parameter.

## Quoting rules

If the special quoting characters are needed literally within the
quoted-text, they can be preceded by backslash, in the usual fashion.

    Quote | Situation
    ------------------------------------------
    `     | In literal
    ```   | In block-quote
    ```!  | If block-quote needs to start with !
    ```#  | If block-quote needs to start with #

    Spec              | Resulting quoted-text
    ---------------------------------------------
    `\`foo\``         | `foo`
    ```\```foo\`````` | ```foo```

That approach can be taken one final step to handle the truly edge cases like
this:

Desired quoted-text:

    \`foo\`

Spec:

    `\\`foo\\``

## Whitespace rules

- Line and indentation requirements:

  - Entities that must start on a fresh line.
    - variant
    - any-section-title (ie scoped or not)
    - section-content-elem (ie heading, block-quote, opt-spec)

  - Opt-spec and variant continuation lines must be indented more than
    the first line and be contiguous with it.

  - Section titles must entirely on one line, ending in marker.

- Line breaks not allowed:

  - NOTE: I'm not certain the current SpecParser enforces this. Maybe not
    worth caring about?

  - Within an {m-n} quantifier.

  - Between a name and equal sign.

  - Within a var-input.

- Whitespace not allowed:

  - Between option prefix and its name.

  - Between partial name and its exclamation mark.

  - Around equal sign for named groups.

  - Within a triple-dot quantifier.

- Whitespace is allowed:

  - Between an element and its quantifier (looks odd, but still valid).

## Spec-syntax hierarchy in compact form

This material condenses the material in spec-syntax into a structure that can
be used for quick-reference.

    - spec
        - usage-section
            - variant [BELOW]
            - section-content-elem [BELOW]
        - section
            - any-section-title
                - section-scope [BELOW]
                - section-title
            - section-content-elem [BELOW]

    - variant
        - valid-name
            - python-name
        - variant-def
            - variant-elem
                - option
                    - bare-option
                    - any-parameter
                        - parameter
                            - valid-name
                            - choices
                                - choice
                                    - valid-name
                                    - literal
                        - parameter-group
                            - parameter
                    - quantifier
                        - triple-dot
                        - quant-range
                        - question
                - positional
                    - valid-name
                    - choices
                    - quantifier
                - any-group => named-group | group
                    - valid-name
                    - group
                        - variant-elem
                    - quantifier
                - literal
                - partial-usage
                    - python-name
                - choice-sep

    - section-content-elem
        - heading
        - block-quote
        - opt-spec
            - opt-scope
                - query-path
                    - query-elem
            - positional [ABOVE]
            - aliases-and-option
                - bare-option
                - option [ABOVE]
            - opt-help-text
                - rest-of-line + continuation-lines

