"""Contains the Experiment class."""

import itertools as it
import multiprocessing as mp
import traceback
from abc import ABCMeta, abstractmethod
from collections import OrderedDict


class Experiment(object):
    """
    Abstract Base Class for experiment execution.

    This ABC encapsulates an 'experiment', which can be any task that generates
    data.  An experiment has "parameters", which are inputs to the experiment.
    Each parameter has a range of values it can take.  The experiment "task" is
    repeated for every combination of parameter values (which I call a
    "configuration" in the code).

    With this class, you can execute tasks in serial on one process,
    or in parallel across many processes (simply use the ``mp`` argument to
    :func:`run()`, which defaults to True).  If you're using lots of data in
    parallel, you should know that all class data will get copied to the new
    processes when they're forked.  You need to be a bit clever with your
    storage of large datasets if that's going to be an issue.

    In order to use this class, you must override the `task()` method and the
    :func:`result()` method.  You will also need to provide a constructor
    (which calls the base class constructor first).  Then, all you need to do
    is call :func:`run()`.  Set ``mp=False`` if you want the experiment done
    in serial (although I'm not sure why you would).
    """
    __metaclass__ = ABCMeta

    def __init__(self, silent=False):
        """
        Constructor for Experiment ABC.  You'll need to override this.

        Your first call in your overridden constructor should be
        ``super().__init__(...)``.  Then, you'll want to set the parameters of
        your experiment.  To do this, add their names as keys in self._params,
        and an iterable of possible values as the dictionary value.  EG:

            self._params['Trial'] = range(100)  # Do 100 trials

        In your task() function, you will get a list of parameter values,
        ordered by when they were added to the dictionary.

        :param silent: Set this to True if you don't want a line of output for
        every completed task.
        :type silent: bool
        :return: None
        """
        self._silent = silent
        self._params = OrderedDict()
        self.__completed = 0
        self.__num_configs = 0

    @abstractmethod
    def task(self, configuration):
        """
        The task that is run for every configuration.

        This function MUST be overridden.  It is the actual "point" of the
        experiment -- the task that must be repeated a bunch of times.  It
        should return any results that need to be saved.  These will be
        passed on to the :func:`result` function.

        When the experiment is run multiprocessing, it is run in a separate
        process!

        :param configuration: A list of parameter values.  The order is the
        order they were added to the
        :type configuration: tuple
        :return: Any results which need to be saved.
        """
        pass

    @abstractmethod
    def result(self, retval):
        """
        Saves results from the task.

        This function MUST be overridden.  It will be called with the return
        value of :func:`task`.  It should save this data in a structure (like
        a DataFrame) that was initialized in :func:`__init__`.  Unlike
        :func:`task`, this function is always run in the parent/master
        process, so you can be sure that you will not have any issues
        updating a single data structure.

        :param retval: The value returned by run_task().
        :return: None
        """
        pass

    def configs(self):
        """Return an iterable of all configurations for the experiment."""
        return it.product(*self._params.values())

    @staticmethod
    def _err(exception):
        """
        Error callback for multiprocessing.

        This function 'handles' exceptions from Processes by displaying them.
        The :func:`_wrapper` function puts tracebacks into the exceptions,
        so that printing them here is actually meaningful.

        :param exception: The exception thrown by :func:`task`.
        :type exception: Exception
        """
        print(exception)

    def _cb(self, retval):
        """
        Receives callbacks from multiprocessing.

        This function is called by the multiprocessing module when a task is
        completed.  It does a little bit of bookkeeping, and then calls the
        user-defined callback.

        :param retval: Value returned by :func:`task`.
        :return: None
        """
        self.__completed += 1
        if not self._silent:
            print('Completed %d/%d.' % (self.__completed, self.__num_configs))
        self.result(retval)

    def _wrapper(self, configuration):
        """
        Wraps the :func:`task` function with a catch-all handler.

        Since the multiprocessing module doesn't really allow you to get
        things like stack traces from exceptions, this function wraps the
        :func:`task` function, and catches all exceptions.  It then re-raises
        them with a stack trace, so that the error-callback (:func:`_err`)
        can display a stack trace.

        :param configuration: Passed to :func:`task`.
        :return: Return value from :func:`task`.
        """
        try:
            return self.task(configuration)
        except Exception:
            raise Exception("".join(traceback.format_exc()))

    def __run_mp(self, processes=None):
        """
        Runs the experiment using the multiprocessing module.

        A process worker pool is created, and tasks are delegated to each
        worker.  Since there is some process spawning overhead, as well as
        IPC overhead, this isn't perfect.  Tasks should be slow enough that
        the speed gains of parallelizing outweigh the overhead of spawning
        and IPC.

        :param processes: Number of processes to use in the pool.  Default is
        None. If None is given, the number from multiprocessing.cpu_count()
        is used.
        :return: Blocks until all tasks are complete.  Returns nothing.
        """
        # Setup the class variables used during the experiment.
        self.__completed = 0

        # Create a multiprocessing pool and add each configuration task.
        result_objects = []
        with mp.Pool(processes=processes) as pool:
            for configuration in self.configs():
                result_objects.append(
                    pool.apply_async(self._wrapper, (configuration,),
                                     callback=self._cb,
                                     error_callback=self._err))
                self.__num_configs += 1
            if not self._silent:
                print('Experiment: queued %d tasks.' % self.__num_configs)
            for result in result_objects:
                result.wait()
            if not self._silent:
                print('Experiment: completed all tasks.')

    def __run_serial(self):
        """
        Runs the experiment in serial.

        Runs each task one after another (in serial).  For big, long running
        tasks this is much slower than in parallel.  But, if you have a few
        smaller ones, serial might be more efficient.  I guess.
        """
        self.__completed = 0
        for config in self.configs():
            try:
                self.result(self.task(config))
                self.__completed += 1
            except:
                print("".join(traceback.format_exc()))
            if not self._silent:
                print('Experiment: completed %d tasks.' % self.__completed)
        if not self._silent:
            print('Experiment: completed all tasks.')

    def run(self, mp=True, nproc=None):
        """
        Run the experiment.

        :param mp: Whether or not to use multiprocessing.
        :type mp: bool
        :param nproc: Number of processes to use (ignored unless ``mp==True``).
        :type nproc: int
        :return: None
        """
        if mp:
            self.__run_mp(processes=nproc)
        else:
            self.__run_serial()
