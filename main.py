import time
from pcg import PCG

def main():
    print("Usage example of PCG random number generator\n")
    seed = int(time.time() * 1000)
    print("Seed:", seed)
    pcga = PCG(seed)
    numbers = [pcga.random() for _ in range(100000)]
    print(numbers[:10])

if __name__ == "__main__":
    main()