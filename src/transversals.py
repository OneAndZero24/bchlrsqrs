from typing import List

import numpy as np


def transversals(LS: np.ndarray) -> List[np.ndarray]:
    """
    Generates a list of transversals of given latin square.
    """

    n = LS.shape[0]
    Ts = []

    def _ext(T: List):  # extends transversal by one
        m = len(T)
        if m == n:
            Ts.append(np.array(T))
        else:
            # Values already present in transversal, row is fixed
            columns = []
            values = []
            if m > 0:
                _, columns, values = list(zip(*T))

            # Possible columns of next entries in transversal
            pos_columns = set(list(range(n))).difference(set(columns))
            for y in pos_columns:
                v = LS[m, y]
                if not (v in set(values)):
                    _ext(T+[[m, y, v]])

    _ext([])
    return Ts