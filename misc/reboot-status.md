
<!--

# reboot-status : Status of project reboot
# Most active files
# TODOs
# Temp work area
# reboot-status : Status of project reboot
# TODOs
# spec-syntax-remaining-issues
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

- Create a `argle-3.14.8` virtualenv (the old `argle-3.9.4` is out of date).
  Then verify with `pytest tests` and `misc/scripts/spec-check
  tests/data/specs/blort.txt -t`. Open questions: whether to include
  `mhutils`; whether to add `pyperclip` (used by `misc/scripts/`) to the `dev`
  extras in `setup.py`.

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

Remaining issues from latest spec-syntax review:

13. Asymmetry: parameters have a `< choices >` form, but positionals don't.
    This is presumably on purpose, since a positional needs a name for its
    dest, but one line saying so would help.

Yes, positionals require a name, as discussed in notes.txt. If the formal
definitions in spec-syntax.md require a name for positionals (and they do),
are further notes needed? I'm inclined to say no.

14a. The whitespace rule for `=` covers named groups but not `<name=choices>`.

The restriction for named groups had a compelling reason, if my hazy memory is
correct. Maybe the rule makes recognizing that "this is a group" during spec
parsing more straightforward? Or maybe the free-floating group name could be
confused for another grammatical element? Or maybe it just looks confusing to
a reader of a spec? Do notes.txt speak on this topic? In any case, within a
`<...>` structure, I don't see similar practical parsing or readability
concerns. What does the current spec parsing code allow or do? My inclination
is to leave policy as-is.

14b. Whether whitespace is allowed before the non-greedy `?` isn't stated.

What does the spec parsing code do today? My inclination is to NOT allow
whitespace beween the quantifier and the non-greedy `?`.

15. Opt-spec vs variant quantity conflict. If a variant declares an Opt as
    required and an opt-spec declares it optional (or vice versa), does the
    opt-spec's quantity win, or is a mismatch an error? Can an opt-spec set
    quantity at all for an Opt already declared in the variants?

This issue is clear: configuration in an opt-spec must be additive, not
conflicting. I think our current docs state that even more clearly now
after our recent editing efforts. Any more need to be done?

14c. `-1` style short options are excluded by `first-char`, without comment.

We need to fix this in the spec-syntax. An Option does require a valid
name/dest, but as long as the Option has that (via its long option form), 
a short form like `-1` should be allowed.

# Temp work area

Claude's replies to spec-syntax-remaining-issues:

13. Agreed: no note needed. The positional rule requires valid-name, and the
    parameter section already says when choices-only is allowed. Done.

14a. Code: the lexer makes `name=(` and `name=[` single tokens
(`paren_open_named`, `brack_open_named` in tokens.py), so no whitespace is
possible there. Inside `<...>`, `valid_name`, `assign`, and choices are
separate tokens and whitespace tokens are discarded, so
`< color = red | green >` parses today.

notes.txt: I found no stated rationale for the named-group restriction. My
guess at the real reason: as one token, `foo=(` is unambiguous at lex time,
and a spaced-out `foo = (` reads like three unrelated things on a usage line.
Inside `<...>` the brackets already bind everything, so neither concern
applies.

Recommendation: leave policy as-is, but add one line to Whitespace rules
("Whitespace is allowed") saying whitespace inside `<...>` is free. That
documents current behavior rather than leaving it implied.

14b. Code: `question` is its own token and whitespace is discarded, so
`<x>... ?` and `{2} ?` are accepted today (spec_parser.py, `quantifier()`).

I agree with disallowing it. The `?` is part of the quantifier, like the
dots in `...`. The fix is small: fold `\??` into the `triple_dot` and
`quant_range` regexes and drop the standalone `question` token. Add "Between
a quantifier and its ?" to the "Whitespace not allowed" list.

Related, found while looking: the lexer accepts `{m-}` for m-or-more, but
spec-syntax says `{m+}`. One of them needs to change. Also, `quant_range`
allows whitespace inside the braces (`{ 2 - 3 }`). The doc says only that
line breaks are not allowed there, which is consistent but unstated.

15. Partial pushback. The rule is clear in notes.txt (opt-independence:
"must be additive... cannot replace or contradict"), but spec-syntax only
says an opt-spec can "add configuration" and points to opt-independence,
which is still in notes.txt. Two loose ends:

- spec-syntax should state the rule directly: opt-spec configuration must be
  additive; a contradiction is an error. One or two lines in the opt-spec
  section.

- What does an unbracketed opt-spec mean? notes.txt treats `-i --ignore-case
  : ...` as saying nothing about quantity when `[-i]` is in the variant. But
  for an Opt declared only in an opt-spec, no brackets presumably means
  required. So brackets in an opt-spec mean "optional," while their absence
  means "required" for a new Opt but "unspecified" for a matched one. That
  asymmetry should be written down. If we don't, someone will read `<path> :
  File path` as a conflict with `[<path>]`.

Also, the opt-independence example itself seems to break the rule. The variant
has `[--bar <b1> <b2>]`, while the Blorting opt-spec has `[--bar <b1>
[<b2>]]`, which makes `<b2>` optional. That's a contradiction, not an
addition. Either the example is wrong, or "additive" allows refining a
parameter's grammar. That needs resolving before opt-independence gets
extracted.

14c. Code: `short_option` is `-` followed by `\w`, so the lexer already
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
