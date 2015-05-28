"""Contains information-theory related functions."""

import numpy as np


def entropy(l):
    """
    Return the entropy of any discrete vector.

    Shannon Entropy is a measure of the "information content" of a random
    variable.  The more widely dispersed the possible values of the RV, the
    higher its entropy.  Entropy is measured in bits (as in, the theoretical
    minimum amount of bits it take to represent the RV).  A RV which was 1 with
    probability 1 would have entropy of 0.  A RV which took on two values with
    equal probability would have entropy of 1 bit, etc.  The entropy function
    is denoted by H(X), and the definition is as follows:

        :math:`H(X) = - \sum_{x\inX} p(X=x) \log_2(p(X=x))`

    :param l: Array (compatible with NumPy array) of integers/bools.
    :returns: The entropy of the array.
    """

    probabilities = np.bincount(l) / len(l)
    with np.errstate(divide='ignore'):  # ignore log(0) errors, we'll handle
        log_probabilities = np.nan_to_num(np.log2(probabilities))
    return -np.sum(probabilities * log_probabilities)
