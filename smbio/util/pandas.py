"""Utility functions for pandas."""


def dataframe_append(dataframe, rowdict):
    """
    Shortcut method for appending a row to a DataFrame.
    :param dataframe: The DataFrame to append to.
    :param rowdict: A dictionary containing each column's value.
    """
    newrow = len(dataframe)
    dataframe.loc[newrow] = 0  # init with 0's
    for k, v in rowdict.items():
        dataframe.loc[newrow, k] = v
