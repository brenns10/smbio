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


def joint_dataset(l1, l2):
    """
    Create a joint dataset for two non-negative integer (boolean) arrays.

    Works best for integer arrays with values [0,N) and [0,M) respectively.
    This function will create an array with values [0,N*M), each value
    representing a possible combination of values from l1 and l2.  Essentially,
    this is equivalent to zipping l1 and l2, but much faster by using the NumPy
    native implementations of elementwise addition and multiplication.
    """
    N = np.max(l1) + 1
    return l2 * N + l1


def mutual_info(l1, l2):
    """
    Return the mutual information of non-negative integer arrays.

    Again, will work best for arrays with values [0,N), where N is rather
    small.  This will compute the mutual information (a measure of "shared
    entropy") between two arrays.  The mutual information between two arrays is
    maximized when one is completely dependant on the other, and minimized if
    and only if they are independent.  (Note that this really applies to random
    variables.  Measurements of random variables obviously won't always
    evaluate to completely independent probabilities, and so they won't always
    have exactly 0 mutual information).
    """
    return entropy(l1) + entropy(l2) - entropy(joint_dataset(l1, l2))


def mutual_info_fast(l1, l2, l1_entropy, l2_entropy):
    """
    Compute mutual info without recomputing the entropy of l1 and l2.

    This function is useful when you are going to be computing many mutual
    information values.  Instead of blindly recomputing the entropy of each
    vector again and again, you may do it once and supply it to this function
    in order to save on that computation.
    """
    return l1_entropy + l2_entropy - entropy(joint_dataset(l1, l2))
