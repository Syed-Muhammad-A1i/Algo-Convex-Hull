import tkinter as tk
from shapely.geometry import LineString

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SweepLineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sweep Line Intersection Detection")

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        self.lines = []
        self.current_line = []

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        tk.Button(root, text="Run Sweep Line", command=self.run_sweep_line).pack()

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        point = Point(x, y)
        self.current_line.append(point)

        if len(self.current_line) == 2:
            self.lines.append(list(self.current_line))
            self.canvas.create_line(self.current_line[0].x, self.current_line[0].y,
                                    self.current_line[1].x, self.current_line[1].y, fill="black")
            self.current_line = []

    def run_sweep_line(self):
        intersections = self.sweep_line_intersection()

        for intersection in intersections:
            self.canvas.create_oval(intersection.x - 3, intersection.y - 3, intersection.x + 3, intersection.y + 3, fill="red")

    def sweep_line_intersection(self):
        intersections = []

        for i in range(len(self.lines)):
            for j in range(i + 1, len(self.lines)):
                line1 = LineString([(self.lines[i][0].x, self.lines[i][0].y),
                                    (self.lines[i][1].x, self.lines[i][1].y)])
                line2 = LineString([(self.lines[j][0].x, self.lines[j][0].y),
                                    (self.lines[j][1].x, self.lines[j][1].y)])

                if line1.intersects(line2):
                    intersection = line1.intersection(line2)
                    if intersection.is_empty or intersection.geom_type == 'Point':
                        intersections.append(Point(*list(intersection.coords)[0]))

        return intersections

if __name__ == "__main__":
    root = tk.Tk()
    app = SweepLineApp(root)
    root.mainloop()
