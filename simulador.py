import numpy as np
import time
from pcg import PCG

class BrownianSimulator2D:
    def __init__(self, steps, particles, grid_size, surface_radius, stick_probability, retries):
        seed = int(time.time() * 1_000)
        self.pcg = PCG(seed)
        self.retries = retries
        self.particles = particles
        self.grid_size = grid_size
        self.surface_radius = surface_radius
        self.steps = steps
        self.stick_probability = stick_probability
        self.particle_positions = self.__initialize_particle_positions()
        self.surface_grid = self.__initialize_surface_grid() 
        
    # Genera una posición aleatoria en la grilla
    def __random_position_in_grid(self):  
        return self.pcg.random() % self.grid_size, self.pcg.random() % self.grid_size
    
    # Inicializa la grilla de la superficie
    def __initialize_surface_grid(self):
        surface_grid = np.zeros((self.grid_size, self.grid_size))
        center = self.grid_size // 2
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if np.sqrt((i - center) ** 2 + (j - center) ** 2) < self.surface_radius:
                    surface_grid[i, j] = 1
        return surface_grid
    
    # Devuelve las posiciones iniciales de las partículas
    def __initialize_particle_positions(self):
        occupied_positions = set()
        surface_center = np.array([self.grid_size // 2, self.grid_size // 2])
        particles_positions = []

        while len(occupied_positions) < self.particles:
            position = self.__random_position_in_grid()
            if np.linalg.norm(np.array(position) - surface_center) > self.surface_radius:
                particles_positions.append(position)
                occupied_positions.add(position)        
        return np.array(particles_positions)
    
    # Devuelve un paso aleatorio de una partícula
    def __random_step(self):
        step_x = int(self.pcg.random_normalized() * 3) - 1 # -1, 0, 1
        step_y = int(self.pcg.random_normalized() * 3) - 1 # -1, 0, 1
        return np.array([step_x, step_y])
    
    # Actualiza las posiciones de las partículas
    def update_positions(self):
        occupied_positions = set(map(tuple, self.particle_positions))
        new_positions = []

        for i in range(len(self.particle_positions)):
            previous_position = tuple(self.particle_positions[i])
            new_position = previous_position

            for _ in range(self.retries):
                step = self.__random_step()                                     
                new_position = tuple(np.clip(self.particle_positions[i] + step, 0, self.grid_size - 1))
                if new_position not in occupied_positions:
                    break
        
            if self.__is_on_surface(new_position):
                if self.pcg.random_normalized() < self.stick_probability:
                    self.__degrade_surface(new_position)
                    continue
                else:
                    step = -step
                    new_position = tuple(np.clip(self.particle_positions[i] + step, 0, self.grid_size - 1))
            self.particle_positions[i] = np.array(new_position)
            occupied_positions.add(new_position)
            new_positions.append(new_position)
            
        self.particle_positions = np.array(new_positions)


    # Devuelve verdadero si la posición está en la superficie
    def __is_on_surface(self, position):
        x, y = position
        return self.surface_grid[x, y] == 1
    
    
    # Degrada la superficie en la posición dada
    def __degrade_surface(self, position):
        x, y = position
        self.surface_grid[x, y] = 0
        print(f"Partícula pegada en ({x},{y}), degradando la superficie y eliminando la partícula...")
        
