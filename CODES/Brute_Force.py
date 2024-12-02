import tkinter as tk
from itertools import combinations

class ConvexHullApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Convex Hull Finder")

        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="white")
        self.canvas.pack()

        self.points = []

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.find_hull_button = tk.Button(self.master, text="Find Convex Hull", command=self.find_convex_hull)
        self.find_hull_button.pack()

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")
        self.points.append((x, y))

    def find_convex_hull(self):
        convex_hull = self.brute_force_convex_hull(self.points)

        # Clear previous hull if any
        self.canvas.delete("hull")

        # Draw convex hull
        for i in range(len(convex_hull)):
            p1 = convex_hull[i]
            p2 = convex_hull[(i + 1) % len(convex_hull)]
            self.canvas.create_line(p1, p2, fill="red", width=2, tags="hull")

    def orientation(self, p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        return 1 if val > 0 else -1

    def is_inside(self, points, p):
        n = len(points)
        if n < 3:
            return False

        for i in range(n):
            if self.orientation(points[i], points[(i + 1) % n], p) != -1:
                return False

        return True

    def brute_force_convex_hull(self, points):
        n = len(points)
        convex_hull = []

        for subset in combinations(points, 3):
            subset = list(subset)
            p1, p2, p3 = subset
            if self.orientation(p1, p2, p3) != 0:
                if self.is_inside(convex_hull, p1):
                    convex_hull.remove(p1)
                convex_hull.append(p1)
                if self.is_inside(convex_hull, p2):
                    convex_hull.remove(p2)
                convex_hull.append(p2)
                if self.is_inside(convex_hull, p3):
                    convex_hull.remove(p3)
                convex_hull.append(p3)

        return convex_hull


def main():
    root = tk.Tk()
    app = ConvexHullApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
