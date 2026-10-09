# Spec examples

<!--

  ## pgrep: README example-1: EX_README_1
  ## pgrep: README example-2: EX_README_2
  ## pgrep: README example-3: EX_README_3
  ## pgrep: README example-4: EX_README_4
  ## Parser configuration: spec-vs-API: EX_JOB_CLIENT
  ## blort: EX_BLORT
  ## neck-diagram: EX_NECK_DIAG
  ## nab: EX_NAB
  ## repo
  ## naval-fate
  ## API-driven configuration vs text-driven configuration

-->

## pgrep: README example-1: EX_README_1

See argparse-vs-argle/pgrep-1-bare-bones

## pgrep: README example-2: EX_README_2

See argparse-vs-argle/pgrep-2-basic

## pgrep: README example-3: EX_README_3

See argparse-vs-argle/pgrep-3-enhanced

## pgrep: README example-4: EX_README_4

See argparse-vs-argle/wrangle

## Parser configuration: spec-vs-API: EX_JOB_CLIENT

See misc/examples/spec-vs-api/job-client-*

## blort: EX_BLORT

See misc/examples/argle-mock-ups/blort.py

- A subcommand-style script.
- Includes a full spec and the resulting usage-text.
- Plus bells and whistles to exercise most of the spec-syntax.
- Includes Opts with same-name and different-config.
- Several notes to document the spec syntax and behaviors.

## neck-diagram: EX_NECK_DIAG

This is a non-standard command line program: its grammar consists of one or
more subcommands with a literal separator between them.

    cmd! :  command=(
                <cmd=snum>   <snum>             |
                <cmd=fnum>   <fnum>             |
                <cmd=number> <numbering=on|off> |
                <cmd=tuning> <notes>...         |
                <cmd=fret>   <syms>...          |
                <cmd=invert> <syms>...
            )

    main : cmd! [ `/` cmd! ]...

## nab: EX_NAB

Another separator-based grammar.

    chomp!   : `/` <cmd=chomp>
    findall! : `/` <cmd=findall> <rgx> [-a]
    grep!    : `/` <cmd=grep> <rgx> [-i] [-v] [-s]
    range!   : `/` <cmd=range> <start> <stop> [<step>] [-g]
    run!     : `/` <cmd=run> <code> [-g <>] [-a] [-v] [-i]

    main : [--trace] commands=(chomp! | findall! | grep! | range! | run!)...
    help : --help

## repo

A comparison of Click and Argle for a subcommand program. Illustrates several
API details.

- click-repo.py
- argle-repo.py

## naval-fate

A comparison of Docopt, Click and Argle.

- click-naval-fate.py
- argle-naval-fate.py
- docopt-naval-fate

## API-driven configuration vs text-driven configuration

See misc/examples/spec-vs-api/

Simple programs.
    - get-pocket-items
    - daily-reading

More complex examples.
    - job-client-*

