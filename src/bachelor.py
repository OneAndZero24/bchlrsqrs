from typing import List

import numpy as np

from src.basics import disjoint, subsets
from src.transversals import transversals


def is_bachelor(LS: np.ndarray) -> bool:
    """
    Checks for bachelor square by checking if it has less than n disjoint transversals.\\
    """

    n = LS.shape[0]

    if n < 2:
        return True

    Ts = transversals(LS)
    t = len(Ts)
    if t < n:
        return True

    D = np.zeros((t, t))    # For each pair of transversals 1 - disjoint, 0 - else
    for i, a in enumerate(Ts):
        for j in range(i, t):
            b = Ts[j]
            D[i, j] = D[j, i] = disjoint(a, b)

    # Filter until left with group of transversals where each is disjoint with at least n-1 others
    dropped = 1                 # Number of dropped transversals if 0 stop
    T_idxs = list(range(t))     # Indicies of transversals disjoint with at least n-1 others
    while len(T_idxs) > 0 and dropped:
        dropped = 0     # reset
        for i in T_idxs:
            if np.count_nonzero(D[i, :]) < n-1:
                D[:, i] = np.zeros(t)
                T_idxs.remove(i)
                dropped += 1

    t = len(T_idxs)
    if t < n:
        return True
    
    groups = subsets(np.array(T_idxs), n)  # Possible disjoint transversals groups
    for group in groups:
        flag = True         # Is this group n disjoint?
        for i in group:     # Each has to be disjoint with all others
            rest = group.difference(set([i]))
            for j in rest:
                if D[i, j] == 0:
                    flag = False
                    break 
            group = rest
        if flag:
            return False

    return True