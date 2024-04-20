from collections.abc import Iterable

import sys
from time import time


class Memoize:
    """
    Simple cookiecutter memoization decorator.\\
    FOR FUNCTIONS WITH `np.ndarray` PARAMETERS
    """

    def __init__(self, f):
        self.f = f
        self.cache = {}

    def _hashlist(self, x):
        if (len(x) > 0) and isinstance(x[0], Iterable):
            return "#".join(map(self._hashlist, x))
        return ''.join(map(str, x))

    def __call__(self, *args):
        values = tuple([self._hashlist(arg.tolist()) if isinstance(arg, Iterable) else arg for arg in args])
        if not values in self.cache:
            self.cache[values] = self.f(*args)
        return self.cache[values]
    

class ProgressBar:
    """
    Simple progress bar based on:\\
    https://gist.github.com/sibosutd/c1d9ef01d38630750a1d1fe05c367eb8
    """

    def __init__(self, total: int, length: int):
        self.i = 0
        self.total = total
        self.length = length
        self._display()

    def _display(self):
        percent = 100.0*self.i/self.total
        sys.stdout.write('\r')
        sys.stdout.write("[{:{}}] {:>3}%"
                        .format('#'*int(percent/(100.0/self.length)),
                                self.length, int(percent)))
        sys.stdout.flush()

    def step(self):
        """
        Move progress bar
        """

        self.i += 1
        self._display()
        if self.i == self.total:
            print()


def print_table(table):
    """
    Simple table print
    """

    col_width = [max(len(str(x)) for x in col) for col in zip(*table)]
    for i, line in enumerate(table):
        print("| " + " | ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line)) + " |")
        if i == 0:
            print('-'*(sum(col_width)+4*len(col_width)))


def time_call(f, *args):
    """
    Wrapper to output runtime of function
    """

    s = time()
    r = f(*args)
    e = time()
    print("Time: {:.1f}s".format(round(e-s, 1)))
    return r