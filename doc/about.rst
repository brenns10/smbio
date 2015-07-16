About
=====

Introduction
------------

After working on a few Bioinformatics related projects, I've rediscovered how
nice it is to reuse code.  For instance, I really should only need to create one
good implementation for information-theory math functions like entropy, mutual
information, and synergy.  Instead, have ended up doing it a few times, with
varying levels of quality.  I selected my best implementations of my frequently
used code, and put them into this library.

My hope is that this will grow as time goes by, providing me with a large
library of general purpose, research oriented, and bioinformatics specific
Python code that will improve my development and prototyping speed.


What Is In Here?
----------------

I'm willing to include most code that doesn't directly relate to a specific
problem.  This means that implementations of general mathematical or computer
science concepts (that aren't already readily implemented in widely used
libraries) are fair game.  I've already done a few, like entropy, mutual
information, and synergy.

Beyond the general theoretical implementations, I also include tons of practical
tools for making my life easier.  For instance, I frequently ask myself, "how do
I append a row in a pandas DataFrame?".  Well, I've written code to do that many
times, and so I've saved it and can use it whenever I'd like (see
:func:`smbio.util.pandas.dataframe_append()`.  Plus, if I find a new, faster way
to do it, I can reimplement that one function and benefit all my code.

So, theoretical as well as practical code are all eligible to be in this
library, so long as I can see myself using them outside of the particular
problem I'm working on.


Installation
------------

Right now, the only installation method is to clone the repository (hosted
privately at `our research server
<https://singularity.case.edu/sbrennan/smbio>`_ and publicly mirrored on `GitHub
<https://github.com/brenns10/smbio>`_), and add it to your Python Path.
However, if anybody actually ends up caring about this library, I will add a
``setup.py`` and the ability to install it using ``pip``.


Examples
--------

Some example code can be found in the ``examples`` directory.
