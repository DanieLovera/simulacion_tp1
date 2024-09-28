import matplotlib.pyplot as plt
from decimal import Decimal

# Constantes
S = 0x9f32e1cbc5e1374b  # Constante Weyl (p.7 del paper)
TWO32 = 4294967296.0  # Para convertir en flotante de precisión 32 bits
TWO32_MINUS_1 = TWO32 - 1.0  # Ajuste para obtener números en [0, 1]
TWO64 = 18446744073709551616  # 2^64 for modulo 64-bit arithmetic

class MSWS:
    def __init__(self, seed_x, seed_w):
        self.x = seed_x % TWO64
        self.w = seed_w % TWO64
        self.s = S % TWO64

    def msws32(self):
        # Update Weyl sequence
        self.w = (self.w + self.s) % TWO64

        # Square x and keep only the lower 64 bits
        self.x = (self.x * self.x) % TWO64

        # Add the Weyl sequence to x and keep it within 64 bits
        self.x = (self.x + self.w) % TWO64

        # Print the current x for inspection
        # print("x after squaring and adding Weyl: %.2E" % Decimal(self.x))

        # Rotate bits: take the upper 32 bits after shifting
        self.x = ((self.x >> 32) | (self.x << 32)) % TWO64

        # Return the lower 32 bits of the final value
        return self.x & 0xFFFFFFFF

    def random(self):
        # Generar número pseudoaleatorio entre 0 y 1
        return self.msws32() / TWO32_MINUS_1


# Inicializar el RNG con semillas aleatorias
rng = MSWS(seed_x=0x9f32e1cbc5e1374b, seed_w=0x9f32e1cbc5e1374b)

# Generate 10,000 random numbers
raw_numbers = [rng.msws32() for _ in range(10000)]
random_numbers = [rng.random() for _ in range(10000)]

# Gráfico de histograma de los números generados (Case 1: Raw 32-bit numbers)
plt.hist(raw_numbers, bins=50, color='green', alpha=0.7)
plt.title("Distribución de números pseudoaleatorios (32-bit Raw Output)")
plt.xlabel("Valor")
plt.ylabel("Frecuencia")
plt.show()

print(random_numbers)

# Gráfico de histograma de los números generados (Case 2: Numbers between 0 and 1)
plt.hist(random_numbers, bins=50, color='blue', alpha=0.7)
plt.title("Distribución de números pseudoaleatorios (Normalized 0-1 Output)")
plt.xlabel("Valor")
plt.ylabel("Frecuencia")
plt.show()
