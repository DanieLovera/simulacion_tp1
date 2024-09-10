class PCG:
    __64BIT_MASK = 0xFFFFFFFFFFFFFFFF
    __32BIT_MASK = 0xFFFFFFFF
    __5BIT_MASK = 0x1F
    __MULTIPLIER = 6364136223846793005
    __INCREMENT = 1442695040888963407

    def __init__(self, seed):
        self.state = seed + PCG.__INCREMENT
        self.random()

    def random(self):
        state = self.state
        # LCG
        self.state = (state * PCG.__MULTIPLIER + PCG.__INCREMENT) & PCG.__64BIT_MASK
        # Apply xorshift
        xorshifted = (state ^ (state >> 18)) >> 27
        # Rotate right (RR)
        rot = state >> 59
        result = PCG.__rotateright32(xorshifted & PCG.__32BIT_MASK, rot & PCG.__32BIT_MASK)
        return result

    def random_normalized(self):
        return PCG.__normalize(self.random())

    @staticmethod
    def __rotateright32(v, r):
        return (v >> r | v << (-r & PCG.__5BIT_MASK)) & PCG.__32BIT_MASK

    @staticmethod
    def __normalize(result):
        return result / PCG.__32BIT_MASK
