import pytest
from six.moves import zip_longest
from textwrap import dedent

from argle._old import (
    OptType,
    SimpleSpecParser,
    ExitCode,
    jdump,
    FormatterConfig,
    Opt,
    ArgleError,
    Parser,
    Section,
    SectionName,
)

def test_parser_using_wildcards():
    args = [
        'tigers',
        'Bees',
        '--spy',
        '--end_run',
        '12.34',
        '--fbi-and-cia',
        'x99',
    ]
    exp = {
        'spy': True,
        'end_run': True,
        'fbi_and_cia': True,
        'positionals': ['tigers', 'Bees', '12.34', 'x99'],
    }
    # Parse.
    p = Parser()
    popts = p.parse(args, should_exit = False)
    # The dict of the ParsedOptions is correct.
    got = dict(popts)
    assert got == exp
    # And we can also access options directly as attributes on the ParsedOptions.
    for k, v in exp.items():
        got = getattr(popts, k)
        assert (k, got) == (k, v)

def test_simple_spec_parser():

    # Valid.
    spec = '-n NAME --foo --bar B1 B2 <x> <y>'
    p = Parser(simple_spec = spec)
    args = [
        '-n', 'Spock',
        '--foo',
        '--bar', '12', '13',
        'phasers',
        'beam',
    ]
    exp = dict(
        n = 'Spock',
        foo = True,
        bar = ['12', '13'],
        x = 'phasers',
        y = 'beam',
    )
    popts = p.parse(args, should_exit = False)
    got = dict(popts)
    assert got == exp

    # Valid.
    spec = '<x> -a A <y>'
    p = Parser(simple_spec = spec)
    args = [
        'phasers',
        'beam',
        '-a', 'hi bye',
    ]
    exp = dict(
        x = 'phasers',
        y = 'beam',
        a = 'hi bye',
    )
    popts = p.parse(args, should_exit = False)
    got = dict(popts)
    assert got == exp

    # Invalid.
    spec = '<x> -a A <y>'
    p = Parser(simple_spec = spec)
    args = [
        'phasers',
        'beam',
        'foo',
        '-a', 'hi bye',
    ]
    with pytest.raises(ArgleError) as einfo:
        popts = p.parse(args, should_exit = False)
    msg = str(einfo.value)
    assert 'unexpected positional' in msg
    assert 'foo' in msg
    popts = p.parsed_options
    d = p.parsed_options._dump()
    assert popts.args == args
    assert popts.args_index == 2
    assert popts.x == 'phasers'
    assert popts.y == 'beam'
    assert popts.a is None

    # Invalid.
    spec = '-n NAME --foo --bar B1 B2 <x> <y>'
    p = Parser(simple_spec = spec)
    args = [
        '-n',
        '--foo',
        '--bar', '12', '13',
        'phasers',
        'beam',
    ]
    with pytest.raises(ArgleError) as einfo:
        popts = p.parse(args, should_exit = False)
    assert 'expected option-argument' in str(einfo.value)

    # Invalid.
    spec = '-n NAME --foo --bar B1 B2 <x> <y>'
    p = Parser(simple_spec = spec)
    args = [
        '-n', 'Spock',
        '--foo',
        '--bar', '12', '13',
        'phasers',
        'beam',
        '--fuzz',
    ]
    with pytest.raises(ArgleError) as einfo:
        popts = p.parse(args, should_exit = False)
    assert 'unexpected option' in str(einfo.value)

def test_basic_api_usage():

    # Scenarios exercised:
    # - Can pass nargs as keyword arg.
    # - Can also pass nargs implicitly via the option_spec.
    # - Can pass an Opt directly or via a dict.
    p = Parser(
        Opt('-n', nargs = 1),
        Opt('--foo'),
        dict(option_spec = '--bar B1 B2 B3 B4 B5'),
        Opt('<x>'),
        Opt('<y>'),
    )

    # Valid.
    args = [
        '-n', 'Spock',
        '--foo',
        '--bar', '11', '12', '13', '14', '15',
        'phasers',
        'beam',
    ]
    exp = dict(
        n = 'Spock',
        foo = True,
        bar = ['11', '12', '13', '14', '15'],
        x = 'phasers',
        y = 'beam',
    )
    popts = p.parse(args, should_exit = False)
    got = dict(popts)
    assert got == exp

    # Invalid.
    args = [
        'phasers',
        'beam',
        '-n', 'Spock',
        '--foo',
        '--bar', '11', '12',
    ]
    with pytest.raises(ArgleError) as einfo:
        popts = p.parse(args, should_exit = False)
    msg = str(einfo.value)
    assert 'expected N of arguments' in msg
    assert '--bar' in msg

    # Invalid.
    args = [
        'phasers',
        '-n', 'Spock',
        '--foo',
        '--bar', '11', '12', '13', '14', '15',
    ]
    with pytest.raises(ArgleError) as einfo:
        popts = p.parse(args, should_exit = False)
    msg = str(einfo.value)
    assert 'Did not get expected N of occurrences' in msg
    assert '<y>' in msg

    # Invalid.
    args = [
        'phasers',
        'beam',
        '--foo',
        '--bar', '11', '12', '13', '14', '15',
        '-n',
    ]
    with pytest.raises(ArgleError) as einfo:
        popts = p.parse(args, should_exit = False)
    msg = str(einfo.value)
    assert 'expected N of arguments' in msg
    assert '-n' in msg

    # Invalid.
    args = [
        'phasers',
        'beam',
        '--foo',
        '--foo',
        '--bar', '11', '12', '13', '14', '15',
        '-n',
    ]
    with pytest.raises(ArgleError) as einfo:
        popts = p.parse(args, should_exit = False)
    msg = str(einfo.value)
    assert 'Found repeated option' in msg
    assert '--foo' in msg

    # Invalid.
    p = Parser(
        Opt('-n', nargs = 1),
        Opt('--foo', required = True),
        dict(option_spec = '--bar B1 B2 B3 B4 B5'),
        Opt('<x>'),
        Opt('<y>'),
    )
    args = [
        'phasers',
        '--bar', '11', '12', '13', '14', '15',
    ]
    with pytest.raises(ArgleError) as einfo:
        popts = p.parse(args, should_exit = False)
    msg = str(einfo.value)
    assert 'Did not get expected N of occurrences' in msg
    assert '--foo, <y>' in msg

    # Invalid.
    p = Parser(
        Opt('-n', nargs = 1),
        Opt('--foo', required = True),
        dict(option_spec = '--bar B1 B2 B3 B4 B5'),
        Opt('<x>'),
        Opt('<y>'),
    )
    args = [
        'X',
        'Y',
        '-n', 'N1',
        '--foo',
        '--bar', '11',
    ]
    with pytest.raises(ArgleError) as einfo:
        popts = p.parse(args, should_exit = False)
    msg = str(einfo.value)
    assert 'Did not get expected N of arguments' in msg
    assert '--bar' in msg

    # Invalid.
    p = Parser(
        Opt('-n', nargs = (0,1), required = True),
        Opt('--foo', required = True),
        Opt('<x>'),
    )
    args = [
        'X',
        '--foo',
    ]
    with pytest.raises(ArgleError) as einfo:
        popts = p.parse(args, should_exit = False)
    msg = str(einfo.value)
    assert 'Did not get expected N of occurrences' in msg
    assert '-n' in msg

    # Valid.
    p = Parser(
        Opt('-n', nargs = (0,1), required = True),
        Opt('--foo', required = True),
        Opt('<x>'),
    )
    args = [
        'X',
        '--foo',
        '-n', '1',
    ]
    exp = dict(
        n = ['1'],
        foo = True,
        x = 'X',
    )
    popts = p.parse(args, should_exit = False)
    got = dict(popts)
    assert got == exp

    # Valid.
    p = Parser(
        Opt('-n', nargs = (0,1), required = True),
        Opt('--foo', required = True),
        Opt('<x>'),
    )
    args = [
        'X',
        '--foo',
        '-n',
    ]
    exp = dict(
        n = [],
        foo = True,
        x = 'X',
    )
    popts = p.parse(args, should_exit = False)
    got = dict(popts)
    assert got == exp

def test_basic_help_text1():

    long_help = 'The N of times to do the operation that needs to be done, either now or in the future'

    p = Parser(
        Opt('-n', nargs = 1, sections = ['foo', 'bar', 'blort'], text = long_help),
        Opt('--foo', sections = ['foo'], text = 'Some Foo behavior'),
        Opt('--xy X Y', sections = ['foo'], text = 'Some xy behavior'),
        dict(option_spec = '--bar', nargs = 5),
        Opt('--some_long_opt1'),
        Opt('--some_crazy_insane_long_opt2', text = long_help),
        Opt('--some_long_opt3'),
        Opt('--some_long_opt4'),
        Opt('--some_long_opt5'),
        Opt('--some_long_opt6'),
        Opt('--some_long_opt7'),
        Opt('<x>', text = 'The X file'),
        Opt('<y>', text = 'The Y file'),
        formatter_config = FormatterConfig(
            Section('foo', 'Foo options'),
            Section(SectionName.POS),
            Section('bar', 'Bar options'),
            Section(SectionName.OPT, 'Some Options'),
            Section(SectionName.USAGE, 'Usage'),
        ),
    )

    exp = dedent('''
        Foo options:
          -n                   The N of times to do the operation that needs to be done,
                               either now or in the future
          --foo                Some Foo behavior
          --xy X Y             Some xy behavior

        Positional arguments:
          <x>                  The X file
          <y>                  The Y file

        Bar options:
          -n                   The N of times to do the operation that needs to be done,
                               either now or in the future

        Some Options:
          --bar
          --some_long_opt1
          --some_crazy_insane_long_opt2
                               The N of times to do the operation that needs to be done,
                               either now or in the future
          --some_long_opt3
          --some_long_opt4
          --some_long_opt5
          --some_long_opt6
          --some_long_opt7

        Usage:
          cli -n --foo [--xy X Y] --bar --some_long_opt1 --some_crazy_insane_long_opt2
              --some_long_opt3 --some_long_opt4 --some_long_opt5 --some_long_opt6
              --some_long_opt7 <x> <y>

        Blort options:
          -n                   The N of times to do the operation that needs to be done,
                               either now or in the future
    ''')

    got = p.help_text()
    assert exp == got

    exp = dedent('''
        Foo options:
          -n                   The N of times to do the operation that needs to be done,
                               either now or in the future
          --foo                Some Foo behavior
          --xy X Y             Some xy behavior

        Bar options:
          -n                   The N of times to do the operation that needs to be done,
                               either now or in the future
    ''')
    got = p.help_text('foo', 'bar')
    assert exp == got

def test_basic_help_text2():

    p = Parser(
        Opt('-n', nargs = 1, sections = ['foo', 'bar', 'blort'], text = 'N of times to do it'),
        Opt('-f -x --foo', sections = ['foo'], text = 'Some Foo behavior'),
        dict(option_spec = '--bar', nargs = 5),
        Opt('<x>', text = 'The X file'),
        Opt('<y>', text = 'The Y file'),
        program = 'frob',
    )

    exp = dedent('''
        Usage:
          frob -n --foo --bar <x> <y>

        Foo options:
          -n                   N of times to do it
          --foo                Some Foo behavior

        Bar options:
          -n                   N of times to do it

        Blort options:
          -n                   N of times to do it

        Positional arguments:
          <x>                  The X file
          <y>                  The Y file

        Options:
          --bar

        Aliases:
          --foo -f -x
    ''')
    got = p.help_text()
    assert exp == got

def test_formatter_config():
    fc = FormatterConfig()
    s = Section('fubbs', 'Fubb options')

def test_simple_spec_parsing():
    text = ' --foo FF GG  -x --blort -z Z1 Z2 <qq> <rr>  --debug  '
    ssp = SimpleSpecParser(text)
    otoks = list(ssp.parse())
    got = [(o.opt_type, o.option_spec, o.nargs) for o in otoks]
    exp = [
        (OptType.LONG,  '--foo FF GG', (2, 2)),
        (OptType.SHORT, '-x',          (0, 0)),
        (OptType.LONG,  '--blort',     (0, 0)),
        (OptType.SHORT, '-z Z1 Z2',    (2, 2)),
        (OptType.POS,   '<qq>',        (1, 1)),
        (OptType.POS,   '<rr>',        (1, 1)),
        (OptType.LONG,  '--debug',     (0, 0)),
    ]
    for g, e in zip_longest(got, exp):
        assert g == e

def test_parser_validations():
    with pytest.raises(ArgleError) as einfo:
        p = Parser(Opt('-n'), Opt('--bar'), Opt('-n'))
    assert 'duplicate Opt' in str(einfo.value)

def test_opt_validations():
    with pytest.raises(ArgleError) as einfo:
        Opt('--foo=X'),
    assert 'invalid option_spec' in str(einfo.value)

def test_parse_exit(std_streams):
    # Create Parser and pass it invalid args to parse.
    # We should get a SystemExit.
    p = Parser(Opt('--foo'))
    args = ['--blort']
    with pytest.raises(SystemExit) as einfo:
        popts = p.parse(args)
    assert str(einfo.value) == str(ExitCode.PARSE_FAIL.code)
    # And stdout should contain expected content.
    output = std_streams.stdout
    assert 'Errors:' in output
    assert 'Found unexpected option: --blort' in output

def test_aliases():

    # Aliases passed as params.
    p = Parser(
        Opt('-n N'),
        Opt('--foo', aliases = ['-f', '-x']),
    )
    exp = dict(
        n = 'Spock',
        foo = True,
    )
    for val in ('--foo', '-f', '-x'):
        args = ['-n', 'Spock'] + [val]
        popts = p.parse(args, should_exit = False)
        got = dict(popts)
        assert got == exp

    # Aliases passed as part of the option_spec.
    p = Parser(
        Opt('-n --number N'),
        Opt('-f -x --foo'),
    )
    exp = dict(
        number = 'Spock',
        foo = True,
    )
    for val in ('--foo', '-f', '-x'):
        # Using -n.
        args = ['-n', 'Spock'] + [val]
        popts = p.parse(args, should_exit = False)
        got = dict(popts)
        assert got == exp
        # Using --number.
        args = ['--number', 'Spock'] + [val]
        popts = p.parse(args, should_exit = False)
        got = dict(popts)
        assert got == exp

def test_add_help(std_streams):

    p = Parser(
        Opt('-n N'),
        Opt('--zoo Z1 Z2', required = True),
        Opt('--foo'),
        add_help = True,
    )

    exp = dedent('''
        Usage:
          cli [-n N] (--zoo Z1 Z2) --foo --help

        Options:
          -n N
          --zoo Z1 Z2
          --foo
          --help               Print help and exit.

        Aliases:
          --help -h
    ''')

    tests = [
        ['--help'],
        ['-h'],
        ['--foo', '--help', '-n', '99']
    ]
    for args in tests:
        with pytest.raises(SystemExit) as einfo:
            popts = p.parse(args)
        assert str(einfo.value) == str(ExitCode.PARSE_HELP.code)
        output = std_streams.stdout
        assert output == exp
        std_streams.reset()

def test_new_parsing_strategy():

    p = Parser(
        Opt('-n', nargs = 1),
        Opt('--trek', nargs = (2, 4)),
        Opt('--bones', nargs = (3, 5)),
        Opt('<x>'),
        Opt('<y>'),
    )

    args = [
        '-n', 'Spock',
        '--trek', 't1', 't2',
        '--bones', 'b11', 'b12', 'b13', 'b14', 'b15',
        'phasers',
        'beam',
    ]
    exp = dict(
        n = 'Spock',
        trek = ['t1', 't2'],
        bones = ['b11', 'b12', 'b13', 'b14', 'b15'],
        x = 'phasers',
        y = 'beam',
    )
    popts = p.parse(args, should_exit = False, alt = True)
    got = dict(popts)
    assert got == exp

    o = Opt('--bones', nargs = (3, 5))
    o._concrete_opts()

