import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import atan2

class Point:
    def __init__(self, x, y):
        self.x, self.y = float(x), float(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return f"({self.x}, {self.y})"


def direction(p, q, r):
    return (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)


def distance_sq(p1, p2):
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2


def find_min_y(points):
    miny = float('inf')
    mini = 0
    for i, point in enumerate(points):
        if point.y < miny:
            miny = point.y
            mini = i
        if point.y == miny:
            if point.x < points[mini].x:
                mini = i
    return points[mini], mini


def graham_scan(points):
    p0, index = find_min_y(points)
    points[0], points[index] = points[index], points[0]

    sorted_polar = sorted(points[1:], key=lambda p: (atan2(p.y - p0.y, p.x - p0.x), p))

    to_remove = []
    for i in range(len(sorted_polar) - 1):
        d = direction(sorted_polar[i], sorted_polar[i + 1], p0)
        if d == 0:
            to_remove.append(i)
    sorted_polar = [i for j, i in enumerate(sorted_polar) if j not in to_remove]

    m = len(sorted_polar)
    if m < 2:
        print('Convex hull is empty')
        return []

    stack = []
    stack.append(points[0])
    stack.append(sorted_polar[0])
    stack.append(sorted_polar[1])

    for i in range(2, m):
        while True:
            d = direction(stack[-2], stack[-1], sorted_polar[i])
            if d < 0:
                break
            else:
                stack.pop()
        stack.append(sorted_polar[i])

    return stack


class GrahamScanVisualizationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Graham's Scan Visualization")

        self.points = []

        # Canvas for drawing points
        self.canvas = tk.Canvas(self.master, width=600, height=600, bg="white")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Label for instructions
        self.label = tk.Label(self.master, text="Click on the canvas to add points.")
        self.label.pack(pady=10)

        # Button to find and plot convex hull
        self.find_hull_button = tk.Button(self.master, text="Find Convex Hull", command=self.find_and_plot_convex_hull)
        self.find_hull_button.pack(pady=10)

        # Matplotlib figure for convex hull plot
        self.fig, self.ax = plt.subplots()
        self.canvas_tkagg = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_tkagg_widget = self.canvas_tkagg.get_tk_widget()
        self.canvas_tkagg_widget.pack()

        # Bind mouse events to canvas
        self.canvas.bind("<Button-1>", self.add_point)

    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append(Point(x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue")

    def find_and_plot_convex_hull(self):
        if len(self.points) < 3:
            self.label.config(text="At least 3 points are required.")
        else:
            convex_hull = graham_scan(self.points)

            # Clear canvas before plotting
            self.canvas.delete("all")

            # Plot the original points
            for point in self.points:
                self.canvas.create_oval(point.x - 3, point.y - 3, point.x + 3, point.y + 3, fill="blue")

            # Plot the convex hull
            for i in range(len(convex_hull) - 1):
                p1, p2 = convex_hull[i], convex_hull[i + 1]
                self.canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill='red')

            # Plot convex hull using Matplotlib
            hull_x, hull_y = zip(*[(point.x, point.y) for point in convex_hull])
            self.ax.clear()
            self.ax.scatter(*zip(*[(point.x, point.y) for point in self.points]), color='blue', label='Original Points')
            self.ax.plot(hull_x + (hull_x[0],), hull_y + (hull_y[0],), color='red', label='Convex Hull')
            self.ax.legend()
            self.canvas_tkagg.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = GrahamScanVisualizationApp(root)
    root.mainloop()
