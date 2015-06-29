smbio
=====

This is a poorly named library containing generally useful code for
bioinformatics.  Anything that's not too specific to the problem at hand can
usually be placed into this library.  It contains implementations of math
functions that aren't present in NumPy (like entropy and mutual information), as
well as some time-saving utilities.  The full list of modules is below.

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

* I only use Python 3.  I have tested none of this code on Python 2.  Your
  mileage may vary.
* So far, the only hard dependency is on NumPy, if you're using the math
  functions.
* If you'd like, IPython and/or PTPython will both improve the experience of
  `smbio.util.repl.repl()`, as well as provide you with better Python REPLs in
  general.

Installation
------------

So far, I haven't felt the need to package this into a "true" Python library
that you can install with Pip.  So, installation really just consists of cloning
the code and adding the package to your Python path.

For instance:

```bash
cd ~/repos
git clone repository-url-here
export PYTHONPATH=$PYTHONPATH:$HOME/repos/smbio/smbio
```

This would only add the library to your path for the duration of that shell
session.  To make this permanent, you'll want to place a line in your
`~.profile` folder like this:

```
export PYTHONPATH=$PYTHONPATH:/full/path/to/smbio
```

Contribution
------------

If this package proves useful to you, and you have any more code you think
belongs here, please feel free to fork and create a pull request.  Hopefully
this can be a package that's useful to a lot of people who use Python for
bioinformatics, especially in my research group.

License
-------

This code is under the MIT License.  You can find more information in
`LICENSE.txt`.
