from typing import List

import numpy as np

from src.basics import permutations, reduce


def _n_sub_ls2x2(LS: np.ndarray) -> int:
    """
    Calculates the number of 2x2 latin subsquares.\\
    COMPLEXITY:
    - time O(n^4)
    - space O(1)
    """

    n = LS.shape[0]
    R = 0
    #(x1, y1) ...
    # ...    (x2, y2)
    for x1 in range(n-1):
        for y1 in range(n-1):
            for x2 in range(x1+1, n):
                for y2 in range(y1+1, n):
                    if (LS[x1, y1] == LS[x2, y2]) and (LS[x1, y2] == LS[x2, y1]):
                        R += 1
    return R


def n_iso(Bs: List[np.ndarray]) -> int:
    """
    Divides bachelors squares into isotopic groups. Returns list of representants.\\
    """

    R = 0
    if len(Bs) > 0:
        n = Bs[0].shape[0]

        # Groups by amount of 2x2 latin subsquares
        tmp = sorted(zip(list(map(_n_sub_ls2x2, Bs)), Bs), key=lambda x: x[0])
        groups = []
        cgroup_n = -1   # Number in current group 
        for i in tmp:
            cn, cBLS = i
            if cn != cgroup_n:
                cgroup_n = cn
                groups.append([])
            groups[-1].append(cBLS)

        perms = permutations(np.array(list(range(1, n+1))))    # LS values permutations

        # Filter isotopic in each group by definition
        for group in groups:
            while len(group) > 0:
                cBLS = group.pop()

                for perm in perms:      # "Renaming" values - each possibility
                    pcBLS = np.array(list(map(lambda x: perm[x-1], cBLS.copy())))
                    for i in range(n):  # Swap row for first
                        spcBLS = pcBLS.copy()
                        spcBLS[[0, i]] = spcBLS[[i, 0]]
                        spcBLS = reduce(np.array(spcBLS))    # To reduced form
                        
                        if (spcBLS != cBLS).any():
                            newgroup = []
                            for c in group:
                                if (spcBLS != c).any():
                                    newgroup.append(c)    # Remove from group
                            group = newgroup
                R += 1  # All isotopic have been removed
    return R