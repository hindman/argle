# spec-syntax: Spec syntax

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
  ## alternative
  ## variant-elem
  ## quantifier
  ## partial-usage
  ## choice-sep
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
  ## parameter-group-def
  ## positional
  ## opt-mention
  ## var-input
  ## Quoting rules
  ## Line types
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

- title-text: any text on one line. Surrounding whitespace is stripped
  for the purpose of generating end-user-facing help text.

- See Line types.

## scoped-section-title

    section-scope >> section-title

- A section-scope applied to a section is a shortcut for applying the scope
  prefix to all regular opt-specs within the section (see opt-spec-scopes).

## section-scope

    query-path

## query-path

    query-elem [. query-elem]...

## query-elem

    glob-char... | digit...

- Can be a name/dest glob pattern or a non-negative integer.
- A glob-char includes valid-name characters, plus wildcards (? and *).
- An all-digit query-elem is an integer, not a glob pattern. It is a
  0-based index into the elements matched by the path so far (x.2: the
  third element matching x). See grammar-querying-api.

## section-content-elem

    heading | opt-spec | block-quote

## heading

    title-text :::

- See section-title and Line types.

## block-quote

    ```  quoted-text3 ```
    ```! quoted-text3 ```             # No wrap
    ```# quoted-text3 ```             # Spec-comment

- Notes:
    - Opening quote must be first on its line.
    - Triple-quotes can sit on their own line, or not.
    - Quoted-text3 can span multiple lines.
    - A marker (! or #) must immediately follow the opening quote.
    - To start the text with a literal ! or #, escape it: ```\!foo```
      is a wrapped block-quote whose text is !foo. See Quoting rules.

## literal

    ` quoted-text1 `

- A literal does not support: name, dest, or quantifier.

## quoted-text: quoted-text3 and quoted-text1

    quoted-text3:  (escape | quoted-char3)...
    quoted-text1:  (escape | quoted-char1)...

- Where:

      escape       | Backslash escapes; see Quoting rules
      quoted-char3 | Any char; but three backquotes in a row end the text
      quoted-char1 | Any char except backquote, newline

- A block-quote ends at the first three unescaped backquotes. One or two
  backquotes in a row are ordinary text.

## variant

    [valid-name[!] :] variant-def

- Marker (!) means partial-variant.

## opt-spec

    [[opt-scope] >>] opt-spec-def [: [opt-help-text]]

- An opt-spec can:
  - Declare and configure a new Opt.
  - Add configuration to Opt(s) that were declared above:
    - Either in the variants.
    - Or in a preceding regular opt-spec (see below).

    - How matching works: see opt-independence.

- Two flavors:
  - Regular opt-spec.
  - Sub-spec: an opt-spec with empty scope (just the `>>` marker).

- Opt-scope:

  - Format: same as a section-scope (or empty in a sub-spec).

  - The scope declares a parent-child relationship:
    - Child: current opt-spec.
    - Parent: Opt(s) defined in variants; or in preceding opt-spec.

  - Determining the parent(s):

    - Child is regular opt-spec:
      - Parent(s) are the matching Opts from the variants.

    - Child is a sub-spec:
      - Parent: the immediately preceding regular opt-spec.
      - No intervening material is allowed between the child sub-spec and its
        parent opt-spec (other than sibling sub-specs).
      - The child must match a sub-component within the parent Opt (see
        opt-spec-scopes).

## opt-spec-def

    opt-spec-group | opt-spec-elem

## opt-spec-elem

    positional | aliases-and-option

## opt-spec-group

    (opt-spec-elem) [quantifier]
    [opt-spec-elem] [quantifier]

- The group cannot be named.
- A () group is useful only with a quantifier.
- A [] group makes its contents optional.

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

- The first line's last word cannot be :: or ::: (see Line types). To get
  such text, put it on a continuation line. The first line can be empty.

## variant-def

    alternative [choice-sep alternative]...

## alternative

    variant-elem...

## variant-elem

    (option | positional | any-group) [quantifier]
    literal
    partial-usage

- To quantify a partial-usage, wrap it in a group.

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

## quantifier

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

- A [] group adds 0 to the allowed quantities. For example, [x]{3-4}
  allows 0, 3, or 4.

- An element takes only one quantifier (no stacking). For more complex
  quantification, nest groups:

      (<x>{2}){1-3}

- A quantifier binds to the element just before it. After a parameter, it
  sets the parameter's nargs. To repeat the option, wrap it in a group:

      --foo <x>...             # One option, 1+ values (nargs).
      (--foo <x>)...           # Option repeated 1+ times (ntimes).

## partial-usage

    valid-name!

## choice-sep

    |

- Separates the alternatives of a variant or group, so it binds most
  loosely: a b | c d means (a b) | (c d). Use a group to narrow it:
  a (b | c) d.

- Because every alternative has at least one variant-elem, a leading,
  trailing, or doubled | is an error.

## any-group

    named-group | group

## named-group

    valid-name = group

## group

    ( variant-def )
    [ variant-def ]

## aliases-and-option

    [alias...] option

- Where alias = bare-option.

## bare-option

    - first-char
    -- valid-name

- Where first-char is a valid first character in a valid-name.

## option

    bare-option [any-parameter...]

- Options attach to any-parameter greedily. That is consistent with Argle
  policy in various areas. Reorder the spec or add groups where needed. Some
  examples:

      --point <x> <y>          # Option with 2 parameters.
      (--point) <x> <y>        # Flag and 2 positionals.
      <x> <y> --point          # Same.
      [--point <x> <y>] <z>    # Option with 2 parameters, then a positional.
      --help [<topic>]         # Option with an optional parameter.

## any-parameter

    (parameter | parameter-group) [quantifier]

## parameter

    < valid-name >
    < valid-name = choices >
    < choices >
    < >

- A bare < valid-name > is always a name. The choices-only form needs
  two or more choices, or a literal: <red|green>, <`red`>. For a single
  choice, use the named form: <color=red>.

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

    [valid-name =] ( parameter-group-def )
    [valid-name =] [ parameter-group-def ]

## parameter-group-def

    any-parameter... [choice-sep any-parameter...]...

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

## quoting-rules: Quoting rules

Most text needs no escaping. Backslashes are ordinary text, and so are
one or two backquotes in a block-quote.

Escaping is needed only where a character would otherwise be read as
syntax. These are the special characters:

    Char          | Where                          | Otherwise read as
    --------------------------------------------------------------------
    `             | In a literal                   | Closing quote
    ` (1st of 3)  | In a block-quote               | Closing quote
    ! or #        | Right after the opening quote  | Marker

To make a special character ordinary, put a backslash before it.

Edge case: to put a literal backslash right before a special character,
double it. In a run of backslashes before a special character, each \\
yields \, and a leftover single \ escapes the character.

Examples:

    Spec              | Result      | Note
    ------------------------------------------------------------------
    `\`foo\``         | `foo`       | .
    ```\```foo\`````` | ```foo```   | .
    ```see `foo\````  | see `foo`   | .
    ```\!foo```       | !foo        | Wrapped
    ```!#foo```       | #foo        | No-wrap; # after marker is text
    ```C:\temp```     | C:\temp     | Backslash is ordinary
    ```\\server```    | \\server    | No special char follows
    ```foo\\```       | foo\        | .
    ```\\!foo```      | \!foo       | .
    `\\\`foo\\\``     | \`foo\`     | .

## line-types: Line types

Each line is classified by the first rule that applies:

- Inside a block-quote: quoted text.

- Contiguous with an opt-spec or variant, and indented more than its first
  line: a continuation line.

- Last word is ::: (heading) or :: (section-title). The marker must be its
  own word, so the text can end in anything.

- Otherwise: variant or opt-spec.

## whitespace-rules: Whitespace rules

- Line and indentation requirements:

  - Entities that must start on a fresh line.
    - variant
    - any-section-title (ie scoped or not)
    - section-content-elem (ie heading, block-quote, opt-spec)

  - Opt-spec and variant continuation lines must be indented more than
    the first line and be contiguous with it.

  - Section titles and headings: see Line types.

- Line breaks not allowed:

  - Within an {m-n} quantifier.

  - Within a var-input.

- Whitespace not allowed:

  - Between option prefix and its name.

  - Between partial name and its exclamation mark.

  - Within a triple-dot quantifier.

- Whitespace is allowed:

  - Between an element and its quantifier.

  - Between a quantifier and its non-greedy `?` marker.

  - Around the equal sign of a named group or parameter-group, including
    line breaks.

  - Within a var-input, around its = and | separators (but see the
    line-break rule above).

## spec-syntax-hierarchy: Spec-syntax hierarchy in compact form

This material condenses the material in spec-syntax into a hierarchy
displaying the relationships among the elements.

Start with the components of a variant:

    - variant
        - valid-name [!]
        - variant-def
            - alternative
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
                                - valid-name
                                - parameter-group-def
                                    - any-parameter
                                    - choice-sep
                            - quantifier
                        - quantifier
                            - triple-dot
                            - quant-range
                            - ? (non-greedy)
                    - positional
                        - valid-name
                        - choices
                        - quantifier
                    - any-group => named-group | group
                        - valid-name
                        - group
                            - variant-def
                        - quantifier
                    - literal
                    - partial-usage
                        - valid-name
            - choice-sep

Then the components that can reside in a section:

    - section-content-elem
        - heading
        - block-quote
        - opt-spec
            - opt-scope
                - query-path
                    - query-elem
            - opt-spec-def => opt-spec-group | opt-spec-elem
                - opt-spec-group
                    - opt-spec-elem
                    - quantifier
                - opt-spec-elem => positional | aliases-and-option
                    - positional
                    - aliases-and-option
                        - bare-option
                        - option
            - opt-help-text
                - rest-of-line + continuation-lines

And the components of the full spec:

    - spec
        - usage-section
            - variant
            - section-content-elem
        - section
            - any-section-title
                - section-scope
                - section-title
            - section-content-elem

