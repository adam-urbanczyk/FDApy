#!/usr/bin/python3.7
# -*-coding:utf8 -*

import itertools
import numpy as np 


#############################################################################
# Checkers used by the UnivariateFunctionalData class.

def _check_argvals(argvals):
    """Check the user provided `argvals`.
    
    Parameters
    ---------
    argvals : list of tuples
        A list of numeric vectors (tuples) or a single numeric vector (tuple) giving the sampling points in the domains. 

    Return
    ------
    argvals : list of tuples
    """
    if type(argvals) not in (tuple, list):
        raise ValueError('argvals has to be a list of tuples or a tuple.')

    if isinstance(argvals, list) and \
            not all([isinstance(i, tuple) for i in argvals]):
        raise ValueError('argvals has to be a list of tuples or a tuple.')

    if isinstance(argvals, tuple):
        print('argvals is convert into one dimensional list.')
        argvals = [argvals]

    # Check if all entries of `argvals` are numeric. 
    argvals_ = list(itertools.chain.from_iterable(argvals))
    if not all([type(i) in (int, float) for i in argvals_]):
        raise ValueError('All argvals elements must be numeric!')

    return argvals

def _check_values(X):
    """Check the user provided `values` (`X`).
    
    Parameters
    ----------
    X : numpy.array
        A numpy array containing values.

    Return
    ------
    X : numpy array
    """

    # TODO: Modify the function to deal with other types of data.
    if not isinstance(X, np.ndarray):
        raise ValueError('X has to be a numpy array.')

    return X

#############################################################################
# Class Univariate FunctionalData 
class UnivariateFunctionalData(object):
    """An object for defining Univariate Functional Data.

    Parameters
    ----------
    argvals : list of tuples
        A list of numeric vectors (tuples) or a single numeric vector (tuple) giving the sampling points in the domains.

    X : array-like
        An array, giving the observed values for N observations. Missing values should be included via `None` (or `np.nan`). The shape depends on `argvals`::

            (N, M) if `argvals` is a single numeric vector,
            (N, M_1, ..., M_d) if `argvals` is a list of numeric vectors.

    Attributes
    ----------

    Notes
    -----

    References
    ----------

    """
    def __init__(self, argvals, X):

        argvals = _check_argvals(argvals)
        X = _check_values(X)

        if len(argvals) != len(X.shape[1:]):
            raise ValueError('argvals and X elements have different support dimensions!')
        if tuple(len(i) for i in argvals) != X.shape[1:]:
            raise ValueError('argvals and X have different number of sampling points!')

        self.argvals = argvals
        self.X = X

    @property
    def argvals(self):
        return self._argvals
    
    @argvals.setter
    def argvals(self, new_argvals):
        new_argvals = _check_argvals(new_argvals)
        self._argvals = new_argvals

    @property
    def X(self):
        return self._X
    
    @X.setter
    def X(self, new_X):
        new_X = _check_values(new_X)
        self._X = new_X