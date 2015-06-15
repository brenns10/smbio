smbio
=====

Stupid name, but I wanted a place to put my most reusable bioinformatics code.
My [tcga](https://github.com/brenns10/tcga) module is badly named (it really
doesn't have very much to do with The Cancer Genome Atlas).  It contains code
that I would like to use outside that one application.  So this module is my
solution.

Modules
--------

I'll keep this list updated as I add things.  I'm trying to heavily docstring
everything, so if you want details on the functions, visit their corresponding
code.

* `smbio.math.information` - Information theory functions (entropy and mutual
  information).
* `smbio.experiment` - Contains my configurable `Experiment` class, which allows
  you to execute many independent tasks in parallel without any explicit use of
  multiprocessing/threading constructs.
* `smbio.util.repl` - Contains the all-powerful `repl()` function, which pops
      open a REPL anywhere in your code (using the best REPL available).
* `smbio.util.progress` - Contains progress bar stuff:
    * Particularly, the all-powerful `progress()` function, that takes a list or
      an iterator and returns the same iterator, but while printing a progress
      bar (if your terminal is capable of a progress bar).
    * Additionally, the `@progress_bar()` annotation, which turns a generator
      into a generator with a progress bar, and inspects the arguments to figure
      out how many iterations there will be.
    * Finally, the `pzip()` function, which is a replacement for the zip
      function, and can display progress bars with accurate estimates.
* `smbio.util.menu` - Contains menu stuff:
    * The wonderful `Menu` class, which allows you to build CLI menus with
      decorators quickly and easily.
    * A nifty `repeat_input()` function that asks for input with a validation
      function (like `int()`) and continues asking until the input is valid.

Dependencies
------------

So far, the only hard dependency is on NumPy, if you're using the math
functions.

If you'd like, IPython and/or PTPython will both improve the experience of
`smbio.util.repl.repl()`, as well as provide you with better Python REPLs in
general.
