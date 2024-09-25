import numpy as np
import time
import pandas as pd
from pcg import PCG
import random

N_NUMBERS = 20
N_MOVES = 200
TIME = 1
INCREASE = 0.1
X_CENTER = 2
Y_CENTER = 2
RADIUS = 1

def generate_points_circle():
    area = np.pi * RADIUS ** 2
    seed = int(time.time() * 1_000)
    pcga = PCG(seed)
    points_x = []
    points_y = []
    for _ in range(N_NUMBERS):
        theta = pcga.random_normalized() * np.pi * 2
        rho = pcga.random_normalized() * (RADIUS)**2
        x = X_CENTER + np.sqrt(rho) * np.cos(theta)
        y = Y_CENTER + np.sqrt(rho) * np.sin(theta)
        points_x.append(x)
        points_y.append(y)
    return points_x, points_y

def next_move(i):
    list_moves = [(0, i), (0, -i), (-i, 0), (i, 0), 
                  (i,i), (i,-i), (-i,i), (-i,-i)]
    probabilities = [1/8] * 8
    move = random.choices(list_moves, probabilities)
    return move[0]

def is_point_in_circle(x, y):
    return (x - X_CENTER)**2 + (y - Y_CENTER)**2 <= RADIUS ** 2

def create_data_frame(points_x, points_y):
    frame = 0
    points = []
    for i in range(N_NUMBERS):
        points.append(i)
    data = {"x": points_x, "y": points_y, "Point": points,
            "Frame": [frame] * len(points_x), "Time[s]": [TIME * frame] * len(points_x)}
    df = pd.DataFrame(data)
    return df

def new_points(x_points, y_points):
    new_x_points = []
    new_y_points = []
    for j in range(len(x_points)):
        move = next_move(INCREASE)
        next_position_x = x_points[j] + move[0]
        next_position_y = y_points[j] + move[1]
        if not is_point_in_circle(next_position_x, next_position_y):
            new_x_points.append(x_points[j])
            new_y_points.append(y_points[j])
        else:
            new_x_points.append(next_position_x)
            new_y_points.append(next_position_y)
    return new_x_points, new_y_points

def add_frame(df, x_points, y_points, frame):
    index = len(df.index)
    for j in range(N_NUMBERS):
        df.loc[index] = [x_points[j], y_points[j], j, frame, TIME * frame]
        index += 1

def add_n_moves(df, x_points, y_points):
    frame = 1
    for _ in range(N_MOVES):
        new_x_points, new_y_points = new_points(x_points, y_points)
        add_frame(df, new_x_points, new_y_points, frame)
        x_points = new_x_points
        y_points = new_y_points
        frame += 1
    df["Frame"] = df.Frame.astype(int)
    df["Point"] = df.Point.astype(int)
