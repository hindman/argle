
# Road map

Spec-parsing [see grammar.py for todo list].

Argument parsing.
  - Read arg-parsing-algo

Generate basic usage and help text.

Docs: proper README [see readme-next-version].

Upgrade classifers to beta.

setup.py:
  - Drop.
  - Move metadata to pyproject.toml
  - See: https://chatgpt.com/c/681fb756-3b08-8003-b89c-c4e070fe87bc

tasks.py:
  - task to create and push a tag

Slogan ideas:
  - Some candidates, none very good: https://chatgpt.com/c/681f862c-f714-8003-a9ed-33242056c155

Release.
  - Maybe drop tox.
  - Set up Github Actions.
  - Decide which Python versions to support.
  - Support nothing older than 3.7

        3.6 : f-strings added
        3.7 : dicts ordered

  - Current status:

        3.7: end of life
        3.8: end of life
        3.9: nearly there

Plan future releases:
  - The ordering of the remaining items (below) seems questionable.
  - Reassess as the project moves forward.

Opt and Parameter configuration:

  - Convert.

  - Validate.

  - Choices.

  _ Factory.

  - Utility types: Path, File, etc.

Parsing enhancements:

  - No-args behaviors, such as show-help or default-args.

  - Data flattening/non-flattening in Result.

Help text: enhancements:

  - Help text: show defaults and choices.

  - Help text: sections.

Alternative inputs: basics:

  - Aliases.

  - Tight binding of option and parameter: --opt=<param>

  - Short-flag bundling.

  - Option-prefix customization.

  - Quoting customization.

  - Non-option args having option prefix: negative numbers.

  - Non-option args having option prefix: configurable escape prefix.

  - Negaters.

Project health:

  - Add validation to user-facing callables.

  - Documentation.

  - Docstrings.

  - Github Actions for CI.

Alternative/fuzzy inputs: handy:

  - Abbrevations for long-options.

  - Abbrevations for choices.

  - Case-insensitivity for options and choices.

Dispatching:

  - General dispatch.

  - Help dispatch.

  - Different dispatch for --help vs -h.

Grammar enhancements:

  - Priority options.

  - Anchored Opts.

Parser enhancements:

  - Parser.query() and bulk configuration.

  - Parser utilities: warn(), help(), error(), exit().

  - Parser configuration to add single-letter option aliases automatically.

  - Group validation.

Alternative inputs: other:

  - @FILE (command line arguments from a file). See argparse fromfile_prefix_chars.

  - Case-insensitive options.

  - Support prompting for inputs (eg password).

Text customization:

  - Help text: short options in separate section.

  - Help text: usage: symbolically named groupings.

  - Help text: customizations via config and/or hooks.

  - Help text: supplied via alternative devices (text file or blob, with
  - f-string support).

  - Error text: customizations via config and/or hooks.

  - Man-page-style help text.

Development aids:

  - Hidden options: either totally or in specific types of help text.

  - Automatic --version.

  - Ability to emit Parser configuration as data (and re-create from data).

  - Bash completion.

  - Integration with configuration data (user prefs) and environment variables.

Other possibilities:

  - Enhanced quantifiers: range-step and disjoint values.

--------------------------

The hierarchy and the grammar now agree, apart from the `opt-spec-group`
quantifier I flagged last time. The real problems are in the grammar itself:
some places can be parsed more than one way, and two parts contradict each
other. Here they are, most serious first.

## Ambiguities: the same text, two parses

1. `<foo>` as a parameter. A parameter can be `< valid-name >` or `< choices
   >`, and a single `choice` can be a `valid-name`. So `--color <red>` could
   mean a parameter named `red` or a parameter whose only choice is `red`. You
   need a rule. For example, the bare form is always a name, and the
   choices-only form needs a `|` or a literal.

2. What follows an option. `option = bare-option [any-parameter...]` takes as
   much as it can, and `<x>` is valid as both a parameter and a positional. So
   in `--foo <x> <y>`, both are parameters, and you can only get a positional
   after an option by reordering or grouping. The same applies to `--foo (<a>
   <b>)`, which could be a parameter-group or a separate group of positionals.
   Both readings are probably intended, but the grammar should state the rule
   (parameters attach to the option before them; a group whose contents are
   all parameters is a parameter-group).

4. Where `|` binds. `choice-sep` is now defined, but its binding strength
   isn't. Does `a b | c d` mean `(a b) | (c d)` or `a (b | c) d`? The docopt
   convention is lowest binding strength within the enclosing group or
   variant. Also unstated: whether a leading, trailing, or doubled `|` is an
   error.

5. How line types are told apart. `title-text` is never defined, and there's
   no order of checks across line types. A line like `--foo : see below::` can
   be read as an opt-spec or as a section title. You need a rule such as "a
   line ending in `::` (or `:::`) is a title/heading, and is checked first."
   With that rule, opt-help-text can't end in those markers unless something
   escapes them.

## Contradictions

6. The edge-case quoting example is wrong under the grammar. `` `\\`foo\\`` ``
   reads as an opening backquote, then `\\` (a literal backslash), then a
   backquote that closes the literal. It doesn't produce `` \`foo\` ``. The
   correct spec would be `` `\\\`foo\\\`` ``.

7. The grammar and the quoting table disagree about what gets escaped. In the
   grammar, `quoted-char3` excludes every backquote, so a single backquote
   inside a block-quote must be escaped, one backquote at a time. The table
   and the ```` ```\```foo\`````` ```` example treat a run of three backquotes
   as the thing being escaped. Pick one model. The per-character model is
   simpler and matches the grammar. If you keep it, the example becomes ````
   ```\`\`\`foo\`\`\```` ````.

8. An empty opt-scope inside a scoped section. A section-scope means "apply
   the scope to all opt-specs in the section." An empty `>>` takes as its
   parent the preceding non-scoped opt-spec. In a scoped section, every
   opt-spec is scoped, so that preceding opt-spec doesn't exist. Either the
   empty scope ignores section scoping, or it's an error. Say which.

## Gaps and loose ends

11. `query-elem`: the note says "positive integer," but `digit...` allows 0.
    What an integer query-elem means (an index?) is never explained.

12. Dangling references:
    - "details below" (line 92) points to nothing.
    - "opt-independence" (line 163) isn't in this doc.
    - The `` ```! `` table row ("if block-quote needs to start with !")
      doesn't say what to write.

13. Asymmetry: parameters have a `< choices >` form, but positionals don't.
    This is presumably on purpose, since a positional needs a name for its
    dest, but one line saying so would help.

14. Small things:
    - The whitespace rule for `=` covers named groups but not
      `<name=choices>`.
    - Whether whitespace is allowed before the non-greedy `?` isn't stated.
    - `-1` style short options are excluded by `first-char`, without comment.

## Overall

The basic design holds up. Distinguishing variants by a leading name and
colon, the colon rule for opt-specs, and the separate markers (`:`/`::`/`:::`,
`>>`, `!`) mostly keep line types distinct. Problems 1, 2, 4, and 5 are the
ones a parser author would get stuck on. Each needs one sentence to resolve,
not a new construct. Problems 6–9 are plain errors or contradictions. I'd
fix those first, since they're cheap.

Do you want me to draft any of these fixes, or would you rather decide 1–5
first? Those are design decisions, not wording.

