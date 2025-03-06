import csv
import math
import matplotlib.pyplot as plt
import numpy as np

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

if __name__ == "__main__":
    xmin, step, xmax, a, b, c = read_config('config.csv')

    x_values = []
    current_x = xmin
    while current_x <= xmax:
        x_values.append(current_x)
        current_x += step

    y_values = [calculate_y(x, a, b, c) for x in x_values]

    with open('results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x', 'y'])
        for x, y in zip(x_values, y_values):
            writer.writerow([x, y])

    x = np.arange(2, 12, 0.2)
    print("y = ", a * np.sin(x) + b * np.cos(x) + abs(a * np.sin(x) - b * np.cos(x)) + c)

    plt.plot(x_values, y_values, marker = "o")
    plt.title('График функции y(x)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.show()