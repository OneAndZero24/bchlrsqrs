from typing import List, Set
from collections.abc import Iterable

import numpy as np

from src.utils import Memoize


@Memoize
def permutations(A: np.ndarray) -> List[np.ndarray]:
    """  
    Generates all possible permutations of given array using Heap's algorithm.\\
    COMPLEXITY:
    - time O(n!)
    - space O(n!)  
    """

    perms = []

    def _gen(k: int, A: np.ndarray):
        if k == 1:
            perms.append(A.copy())
        else:
            _gen(k-1, A)        # Permutations with A[k-1] unaltered
            for i in range(k-1):  # Which element to fix
                if k%2 == 0:
                    A[i], A[k-1] = A[k-1], A[i]
                else:
                    A[0], A[k-1] = A[k-1], A[0]
                _gen(k-1, A)

    _gen(A.size, A)
    return perms


def disjoint(A: np.ndarray, B: np.ndarray) -> bool:
    """
    Checks if two sequences are disjoint.\\
    COMPLEXITY:
    - time O(n)
    - space O(1)
    """ 

    for a, b in zip(A, B):
        if (a == b).all():
            return False
    return True


@Memoize
def derange_check(A: np.ndarray) -> bool:
    """
    Simple check to see if given sequence is a derangement.\\
    COMPLEXITY:
    - time O(n)
    - space O(1)
    """

    for i, A_i in enumerate(A):
        if i+1 == A_i:
            return False
    return True


@Memoize
def subsets(A: np.ndarray, n: int) -> List[List]:
    """
    Generates all subsets of `A` with size `n`.\\
    COMPLEXITY:
    - time O(A.shape[0] choose n)
    - space O(1)
    """

    if n == 0:
        return [ set() ]
    if A.size < n:
        return []
    
    return subsets(A[1:], n)+[ S.union(set([A[0]])) for S in subsets(A[1:], n-1) ]


def reduce(LS: np.ndarray) -> np.ndarray:
    """
    Transforms latin square into rduced form.\\
    COMPLEXITY:
    - time O(n^3)
    - space O(1)
    """

    n = LS.shape[0]

    def _order(LS):     # Orders rows
        for i in range(n-1):
            if LS[i, 0] != i+1:     # Have to move this row
                for j in range(i+1, n):
                    if LS[j, 0] == i+1:     # Correct place
                        LS[[i, j]] = LS[[j, i]]
                        break
        return LS

    RLS = LS.copy()
    RLS = _order(RLS.T)       # Order columns
    RLS = _order(RLS.T)     # Order rows
    return RLS