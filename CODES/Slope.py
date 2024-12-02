import tkinter as tk

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def slope(p1, p2):
    if p1.x == p2.x:
        return float('inf')  # Vertical line
    return (p2.y - p1.y) / (p2.x - p1.x)

def on_segment(p, q, r):
    return (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and
            q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y))

def do_intersect(p1, q1, p2, q2):
    slope1 = slope(p1, q1)
    slope2 = slope(p2, q2)

    if slope1 == slope2:  # Parallel lines
        return False

    intercept1 = p1.y - slope1 * p1.x
    intercept2 = p2.y - slope2 * p2.x

    intersection_x = (intercept2 - intercept1) / (slope1 - slope2)
    intersection_y = slope1 * intersection_x + intercept1

    intersection_point = Point(intersection_x, intersection_y)

    return on_segment(p1, intersection_point, q1) and on_segment(p2, intersection_point, q2)

class LineIntersectionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Line Intersection Checker")

        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="white")
        self.canvas.pack()

        self.points = []
        self.lines = []

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.check_intersection_button = tk.Button(self.master, text="Check Intersection", command=self.check_and_visualize_intersection)
        self.check_intersection_button.pack()

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")
        new_point = Point(x, y)
        self.points.append(new_point)

        if len(self.points) == 2:
            self.lines.append(self.canvas.create_line(self.points[0].x, self.points[0].y, self.points[1].x, self.points[1].y))

            # Reset points for the next line segment
            self.points = []

    def check_and_visualize_intersection(self):
        if len(self.lines) == 2:
            line1_coords = self.canvas.coords(self.lines[0])
            line2_coords = self.canvas.coords(self.lines[1])

            p1 = Point(line1_coords[0], line1_coords[1])
            q1 = Point(line1_coords[2], line1_coords[3])
            p2 = Point(line2_coords[0], line2_coords[1])
            q2 = Point(line2_coords[2], line2_coords[3])

            if do_intersect(p1, q1, p2, q2):
                print("The line segments intersect.")
            else:
                print("The line segments do not intersect.")

def main():
    root = tk.Tk()
    app = LineIntersectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
