from typing import List

import numpy as np

from src.basics import *



def rls_gen(n: int) -> List[np.ndarray]:
    """
    Generates a list of reduced latin squares size nxn.\\
    """

    LSs = []

    def _gen(k: int, LS: np.ndarray):   # Starts to fill LS from row k (indexed from 1)
        # Form of current row
        crow = np.arange(1, n+1)
        crow[k-1] = crow[0]
        crow[0] = k

        # Consider each potential row
        pot_rows = list(filter(lambda P: derange_check(P), [ np.concatenate(([k], P)) for P in permutations(crow[1:]) ]))
        for r, row in enumerate(pot_rows):
            LS[k-1, :] = row

            # Check LS property given previous rows
            for i in range(k-1):
                if not disjoint(LS[i, 1:], LS[k-1, 1:]):     # LS properties violated
                    if r < len(pot_rows)-1:
                        break
                    return  # Last row didnt match
            else:   # ROW FOUND
                if k < n:
                    _gen(k+1, LS.copy())
                else:
                    LSs.append(LS.copy())   # LS FOUND

    if n > 1:
        template = np.zeros((n, n), dtype=int)
        template[0, :] = np.arange(1, n+1)
        _gen(2, template)
    elif n == 1:
        LSs = [np.array([[1]])]

    return LSs