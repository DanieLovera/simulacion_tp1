import time
import matplotlib.pyplot as plt
from pcg import PCG

def main():
    seed = int(time.time() * 1000)
    pcga = PCG(seed)
    numbers = [int(pcga.random_normalized() * 100) for _ in range(100000)]
    
    plt.hist(numbers, bins=100, edgecolor='black')
    plt.title('Distribution of Random Numbers Generated by PCG')
    plt.xlabel('Number')
    plt.ylabel('Frequency')
    plt.savefig('random_numbers_histogram.png')

if __name__ == "__main__":
    main()