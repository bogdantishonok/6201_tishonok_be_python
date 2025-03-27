import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import time

def read_config(config):
    with open(config, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            xmin = float(row['xmin'])
            step = float(row['step'])
            xmax = float(row['xmax'])
            a = float(row['a'])
            b = float(row['b'])
            c = float(row['c'])
    return xmin, step, xmax, a, b, c

def calculate_y(x, a, b, c):
    return a * math.sin(x) + b * math.cos(x) + abs(a * math.sin(x) - b * math.cos(x)) + c

xmin, step, xmax, a, b, c = read_config('config.csv')

x_values = []
current_x = xmin
while current_x <= xmax:
    x_values.append(current_x)
    current_x += step

start_time = time.time()
y_values = [calculate_y(x, a, b, c) for x in x_values]
math_time_1 = time.time()
math_time = math_time_1 - start_time
print(y_values)

x_np = np.arange(2, 12, 0.001)
start_time_np = time.time()
y_np = a * np.sin(x_np) + b * np.cos(x_np) + np.abs(a * np.sin(x_np) - b * np.cos(x_np)) + c
numpy_time = time.time() - start_time_np

with open('results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['x', 'y (numpy)'])
    for x, y in zip(x_np, y_np):
        writer.writerow([x, y])

print(f"Затрачено времени math: {math_time} сек")
print(f"Затрачено времени numpy: {numpy_time} сек")

plt.plot(x_values, y_values, marker = "o")
plt.title('График функции y(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.grid()
plt.show()