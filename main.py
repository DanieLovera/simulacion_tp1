import time
from pcg import PCG


def main():
    seed = int(time.time() * 1000)
    pcga = PCG(seed)
    for i in range(100):
        print(pcga.random_normalized())


main()
