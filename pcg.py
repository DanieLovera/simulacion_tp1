class PCG:
    def __init__(self, seed):
        self.state = seed
        self.multiplier = 6364136223846793005
        self.increment = 1442695040888963407

    def random(self):
        # LCG
        self.state = (self.state * self.multiplier + self.increment) & ((1 << 64) - 1)
        # Apply xorshift
        xorshifted = (self.state ^ (self.state >> 18)) >> 27
        # Rotate right (RR)
        rot = self.state >> 59
        result = PCG.rotate32(xorshifted, rot)
        return result

    def random_normalized(self):
        return PCG.normalize(self.random())

    def rotate32(v, r):
        return (v >> r) | (v << ((-r) & 31)) & 0xFFFFFFFF

    def normalize(result):
        return result / 0xFFFFFFFF
