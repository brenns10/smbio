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
* `smbio.util.repl` - Contains utilities to make life easier:
    * `repl` - Call this to pop open a REPL anywhere in your code (uses the best
      REPL available).

Dependencies
------------

So far, the only hard dependency is on NumPy, if you're using the math
functions.

If you'd like, IPython and/or PTPython will both improve the experience of
`smbio.util.repl.repl()`, as well as provide you with better Python REPLs in
general.
