
<!-- 

  # road-map: Road map
  # temp: Temp work area

-->

# road-map: Road map

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

# temp: Temp work area

...

