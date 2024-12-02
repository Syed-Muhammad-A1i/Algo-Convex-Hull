import tkinter as tk

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0  # collinear
    return 1 if val > 0 else 2  # 1 for clockwise, 2 for counterclockwise

def on_segment(p, q, r):
    return (
        (q.x <= max(p.x, r.x))
        and (q.x >= min(p.x, r.x))
        and (q.y <= max(p.y, r.y))
        and (q.y >= min(p.y, r.y))
    )

def do_intersect(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if (o1 != o2) and (o3 != o4):
        return True

    if (o1 == 0) and on_segment(p1, p2, q1):
        return True

    if (o2 == 0) and on_segment(p1, q2, q1):
        return True

    if (o3 == 0) and on_segment(p2, p1, q2):
        return True

    if (o4 == 0) and on_segment(p2, q1, q2):
        return True

    return False

class LineIntersectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Line Intersection Checker")

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        self.points = []
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        tk.Button(root, text="Check Intersection", command=self.check_intersection).pack()
        self.result_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.result_label.pack()

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        self.points.append(Point(x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")

        if len(self.points) == 4:
            self.canvas.create_line(self.points[0].x, self.points[0].y, self.points[1].x, self.points[1].y, fill="black")
            self.canvas.create_line(self.points[2].x, self.points[2].y, self.points[3].x, self.points[3].y, fill="black")

    def check_intersection(self):
        if len(self.points) == 4:
            intersect = do_intersect(self.points[0], self.points[1], self.points[2], self.points[3])

            if intersect:
                self.result_label.config(text="Lines intersect!")
            else:
                self.result_label.config(text="Lines do not intersect")

        self.points = []  # Reset points for the next round

if __name__ == "__main__":
    root = tk.Tk()
    app = LineIntersectionApp(root)
    root.mainloop()
