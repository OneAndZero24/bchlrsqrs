from argparse import ArgumentParser

from src.utils import ProgressBar, time_call, print_table
from src.rls_gen import rls_gen
from src.bachelor import is_bachelor
from src.isotopy import n_iso


def _step(f, i):
    RLSs = time_call(rls_gen, i)
    n = len(RLSs)
    print(f"Number of RLS {i}x{i}: {n}")
    if not f is None:
        f.write("RLSs:\n")
        f.write(str(RLSs))
        f.write('\n')

    Bs = []
    def bchlr():
        B = 0
        pb = ProgressBar(n, 100)
        for RLS in RLSs:
            r = is_bachelor(RLS)
            B += r
            if r:
                Bs.append(RLS)
            pb.step()
        return B
    
    B = time_call(bchlr)
    print(f"Number of bachelor RLS {i}x{i}: {B}")
    if not f is None:
        f.write("BACHELORS:\n")
        f.write(str(Bs))
        f.write('\n')

    n_iso_Bs = time_call(n_iso, Bs)
    print(f"Number of non-isotopic bachelor RLS {i}x{i}: {n_iso_Bs}")
    print()

    return n, B, n_iso_Bs

parser = ArgumentParser()
parser.add_argument("-n", type=int, default=6)
parser.add_argument("--debug", action="store_true")

args = parser.parse_args()

f = None
if args.debug:
    f = open("debug.log", "a")

summary = [["N", "Number of RLS", "Number of bachelor RLS", "Number of non-isotopic bachelor RLS"]]
for i in range(1, args.n+1):
    n, B, n_iso_B = _step(f, i)
    summary.append([i, n, B, n_iso_B])
print_table(summary)
if args.debug:
    f.close()