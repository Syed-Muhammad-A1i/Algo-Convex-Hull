import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


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


def jarvis_march(points):
    a = min(points, key=lambda point: point.x)
    index = points.index(a)

    l = index
    result = [a]

    while True:
        q = (l + 1) % len(points)
        for i in range(len(points)):
            if i == l:
                continue
            d = direction(points[l], points[i], points[q])
            if d > 0 or (d == 0 and distance_sq(points[i], points[l]) > distance_sq(points[q], points[l])):
                q = i
        l = q
        if l == index:
            break
        result.append(points[q])

    return result


class JarvisMarchVisualizationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Jarvis March Visualization")

        self.points = []

        # Canvas for drawing points and convex hull
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
            hull_points = jarvis_march(self.points)
            hull_points.append(hull_points[0])  # Closing the loop

            # Clear canvas before plotting
            self.canvas.delete("all")

            # Plot the original points
            for point in self.points:
                self.canvas.create_oval(point.x - 3, point.y - 3, point.x + 3, point.y + 3, fill="blue")

            # Plot the convex hull
            self.canvas.create_line(*[(point.x, point.y) for point in hull_points], fill='red')

            # Plot convex hull using Matplotlib
            self.ax.clear()
            self.ax.scatter(*zip(*[(point.x, point.y) for point in self.points]), color='blue', label='Original Points')
            self.ax.plot(*zip(*[(point.x, point.y) for point in hull_points]), color='red', label='Convex Hull')
            self.ax.legend()
            self.canvas_tkagg.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisMarchVisualizationApp(root)
    root.mainloop()
