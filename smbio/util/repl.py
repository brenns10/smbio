"""Utility functions and classes!"""

_embed_banner = '\n* BREAKPOINT: {filename}:{line}\n* Ctrl+D to continue...'


def _embed_ptipython():
    """
    Embed a ptpython prompt using IPython.

    PTPython has an IPython module supporting the exact same embedding API as
    IPython.  This code is the same as the IPython code, except for which
    module the InteractiveShellEmbed class comes from.  I kept the functions
    separate so that the order can still be customized in the backend list.
    """
    try:
        from ptpython.ipython import InteractiveShellEmbed
    except ImportError:
        return False
    from inspect import currentframe
    caller = currentframe().f_back.f_back
    shell = InteractiveShellEmbed.instance(display_banner=False)
    print(_embed_banner.format(filename=caller.f_code.co_filename,
                               line=caller.f_lineno))
    shell(stack_depth=3)
    return True


def _embed_ptpython():
    """Embed a ptpython vanilla prompt."""
    try:
        from ptpython.repl import embed
    except ImportError:
        return False

    from inspect import currentframe
    caller = currentframe().f_back.f_back
    print(_embed_banner.format(filename=caller.f_code.co_filename,
                               line=caller.f_lineno))
    embed(caller.f_globals, caller.f_locals)
    return True


def _embed_ipython():
    """Embed an IPython prompt."""
    try:
        from IPython.terminal.embed import InteractiveShellEmbed
    except ImportError:
        return False
    from inspect import currentframe
    caller = currentframe().f_back.f_back
    shell = InteractiveShellEmbed.instance(display_banner=False)
    print(_embed_banner.format(filename=caller.f_code.co_filename,
                               line=caller.f_lineno))
    shell(stack_depth=3)
    return True


def _embed_vanilla():
    """
    Embed vanilla python interpreter (two frames back).

    This function is adapted from a StackOverflow answer by user "Havok", which
    you can find here: <http://stackoverflow.com/a/28423594>.
    """
    from code import InteractiveConsole
    from inspect import currentframe

    caller = currentframe().f_back.f_back

    env = {}
    env.update(caller.f_globals)
    env.update(caller.f_locals)

    try:
        import readline
        import rlcompleter
        readline.set_completer(rlcompleter.Completer(env).complete)
        readline.parse_and_bind("tab: complete")
    except ImportError:
        pass

    shell = InteractiveConsole(env)
    shell.interact(
        _embed_banner.format(
            filename=caller.f_code.co_filename, line=caller.f_lineno
        )
    )

    return True


# Backends are tried in this order.  The first one to successfully import its
# requirements will run and return True.
_embed_backends = [
    _embed_ptipython,
    _embed_ptpython,
    _embed_ipython,
    _embed_vanilla,
]


def repl():
    """
    Open up a terminal to inspect variables and do basic debugging tasks.

    Insert a call to this function anywhere in your code, and it will pop open
    a REPL.  You can access everything in scope at that particular point.  You
    will be able to modify objects, but you will not be able to reassign
    variables!  So, you could append to a list, but not assign an integer to a
    new value.

    This function will load the most capable possible REPL interface possible.
    If you have ptpython installed, that will be used, so you will benefit from
    completion support, etc.  Furthermore, if you have IPython, that will also
    be used.  With a bare Python installation, the basic Python interpreter
    will be used (along with readline if your platform supports it).
    """
    for backend in _embed_backends:
        if backend():
            return
