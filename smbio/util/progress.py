"""Progress bar utilities."""

from enum import Enum
from io import StringIO
import sys


class TermType(Enum):
    """Enumeration of types of terminals."""
    TTY = 1
    IPythonTerminal = 2
    IPythonGUI = 3
    File = 4
    Unknown = 0


def _non_ipy_term_type():
    """
    The terminal type of a non-IPython terminal.

    :return: Item of type :class:`TermType`.
    """
    import sys
    if sys.stdout.isatty():
        return TermType.TTY
    else:
        return TermType.File


def get_term_type():
    """
    Identifies the type of terminal the current Python instance is running in.

    :return: Item of type :class:`TermType`.
    """
    try:
        # noinspection PyUnresolvedReferences
        import IPython
    except ImportError:
        return _non_ipy_term_type()

    import IPython.terminal.interactiveshell as intshell
    import IPython.kernel.zmq.zmqshell as zmqshell
    ipy = IPython.get_ipython()
    if ipy is None:
        return _non_ipy_term_type()
    elif isinstance(ipy, intshell.TerminalInteractiveShell):
        return TermType.IPythonTerminal
    elif isinstance(ipy, zmqshell.ZMQInteractiveShell):
        return TermType.IPythonGUI
    else:
        return TermType.Unknown


def _silent_format(string, params):
    """
    Attempt to format a string, and ignore any exceptions that occur.

    :param str string: String to format.
    :param tuple params: Formatting parameters.
    :return: The formatted string, or the string parameter on error.
    """
    try:
        return string % params
    except TypeError:  # Not all arguments converted ...
        return string


class Progress:
    """
    An iterator which draws a progress bar on stdout.
    This iterator allows a progress bar to be drawn on stdout, while still
    allowing user code to print to stdout.  Note that the current
    implementation replaces stdout with a buffer and prints the buffer every
    time next() is called on the iterator.  Therefore, a progress bar within
    a progress bar would be hopelessly pointless, as it would never display
    properly.
    """

    def __init__(self, it, width=80, niters=100):
        """
        *Constructor*

        This function can infer iterations from any object on which len() can
        be applied.  If len() cannot be applied, then niters is used to
        determine the number of iterations to base the estimate.

        :param iterable it: The iterator to wrap.
        :param int width: The console width.
        :param int niters: Estimated number of iterations.
        :return: None
        """
        self.it = iter(it)
        self.width = width
        self.iters = 0
        self.percent = 0
        self.needswrite = True
        self.finalized = False

        # Redirect stdout (mucho dangerous, I know)
        self.stdout = sys.stdout
        sys.stdout = StringIO()

        # Default formats
        self.prefix = '%3d%% ['
        self.suffix = ']'
        self.block = '#'

        # Attempt to figure out the amount of iterations:
        try:
            self.estimate = len(it)
        except TypeError:
            if niters is not None:
                self.estimate = niters
            else:
                self.estimate = 100

        self.__progress()

    def __iter__(self):
        """
        Called to create an iterator from this object.

        :return: Self.
        """
        return self

    def __flush(self):
        """
        Flush the stdout buffer, if it contains anything.

        :return: Nothing
        """
        output = sys.stdout.getvalue()
        if len(output) > 0:
            self.stdout.write('\r' + ' '*self.width + '\r')
            self.stdout.write(output)
            sys.stdout.close()
            sys.stdout = StringIO()
            self.needswrite = True

    def __progress(self):
        """
        Print the progress bar if it is necessary.

        :return: Nothing.
        """
        newpercent = int((self.iters / self.estimate) * 100)
        if newpercent > 100:
            msg = 'Unknown Progress'
            self.stdout.write('\r' + msg + ' '*(self.width-len(msg)))
        elif newpercent != self.percent or self.needswrite:
            prefix = _silent_format(self.prefix, newpercent)
            suffix = _silent_format(self.suffix, newpercent)
            navailable = self.width - len(prefix) - len(suffix)
            nblocks = int((self.iters / self.estimate) * navailable)
            self.stdout.write('\r' + prefix + self.block * nblocks + ' '*(
                navailable-nblocks) + suffix)
        self.needswrite = False

    def __next__(self):
        """
        Called on each iteration, to get a value.

        :return: The next value from self.it.
        """
        self.iters += 1
        self.__flush()
        self.__progress()
        self.percent = int((self.iters/self.estimate) * 100)
        try:
            return next(self.it)
        except StopIteration:
            if not self.finalized:
                # Write 100%
                self.iters = self.estimate
                self.needswrite = True
                self.__progress()

                # Replace stdout
                sys.stdout.close()
                sys.stdout = self.stdout
                print()

            # End the iteration
            raise StopIteration


def progress(it, *args, **kwargs):
    """
    Returns a progress bar if terminal is capable.

    See docstrings for Progress for more information on the other arguments.

    :param it: The iterator/list/range.
    :param args: Other positional arguments to pass to constructor of
                 :class:`Progress`.
    :param kwargs: Other keyword arguments for :class:`Progress`.
    :return: instance of :class:`Progress` if terminal is capable, otherwise
             returns the original iterator.
    """
    termtype = get_term_type()
    if termtype == TermType.TTY or termtype == TermType.IPythonTerminal:
        return Progress(it, *args, **kwargs)
    else:
        return it


def progress_bar(index=None, name='niters', niters=100):
    """
    Turns a generator function into an iterator that uses Progress.

    Use this function as a decorator on a generator function.  Note that to use
    this function as a decorator, you must always call the function after the @
    sign.  That is, if you don't provide size_param, use ``@progress_bar()``,
    instead of ``@progress_bar``.

    :param tuple size_param: This parameter tells the progress bar where it can
        find an estimate of the number of iterations in the parameter list of
        the call to the generator function.  The elements of the tuple are:

        - [0]: Argument index (default None)
        - [1]: Keyword argument index
        - [2]: Default (a better guess than util.Progress can provide).

        The default is to look for an niters parameter in the call to the
        wrapped generator.
    :return: Wrapped generator function.
    """
    def wrap(f):
        """
        This function is returned by the call to progress_bar.
        When a function is decorated with progress_bar(), progress_bar()
        executes on module load.  It returns this function, which is the one
        that is actually called with the function to be decorated as a
        parameter.  This function returns a wrapped version of f.

        :param f: The actual function to be decorated.
        :return: The decorated/wrapped function.
        """
        def wrapped_f(*args, **kwargs):
            if name in kwargs:
                niters = kwargs[name]
            elif index is not None and index < len(args):
                niters = args[index]
            return progress(f(*args, **kwargs), niters=niters)
        return wrapped_f
    return wrap


def pzip(*args):
    """A zip() implementation that displays a progress bar correctly."""
    if any(hasattr(x, '__len__') for x in args):
        estimate = min(len(x) for x in args if hasattr(x, '__len__'))
    else:
        estimate = 100
    return progress(zip(*args), niters=estimate)
