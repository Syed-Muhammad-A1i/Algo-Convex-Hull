import matplotlib.pyplot as plt
import numpy as np
import mplcursors

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # collinear
    return 1 if val > 0 else 2  # 1 for clockwise, 2 for counterclockwise

def on_hull(p, q, r):
    return orientation(p, q, r) == 2  # Check if the point is on the upper hull

def kirkpatrick_seidel(points):
    n = len(points)
    if n < 3:
        return points

    points = sorted(points, key=lambda x: x[0])

    upper_hull = [points[0], points[1]]
    lower_hull = [points[0], points[1]]

    for i in range(2, n):
        upper_hull.append(points[i])
        while len(upper_hull) > 2 and not on_hull(upper_hull[-3], upper_hull[-2], upper_hull[-1]):
            upper_hull.pop(-2)

        lower_hull.append(points[i])
        while len(lower_hull) > 2 and on_hull(lower_hull[-3], lower_hull[-2], lower_hull[-1]):
            lower_hull.pop(-2)

    convex_hull = upper_hull + lower_hull[1:-1]

    return convex_hull

def onclick(event):
    x, y = event.xdata, event.ydata
    points.append((x, y))
    ax.plot(x, y, marker='o', color='blue')
    fig.canvas.draw()

    if len(points) > 2:
        # Compute convex hull using Kirkpatrick and Seidel algorithm
        convex_hull = kirkpatrick_seidel(points)

        # Clear previous hull
        for line in hull_lines:
            line.remove()
        hull_lines.clear()

        # Plot the convex hull
        for i in range(len(convex_hull)):
            hull_lines.append(ax.plot([convex_hull[i][0], convex_hull[(i + 1) % len(convex_hull)][0]],
                                      [convex_hull[i][1], convex_hull[(i + 1) % len(convex_hull)][1]],
                                      color='red', linewidth=2, linestyle='-')[0])

        fig.canvas.draw()

# Initialize an empty list to store points
points = []

# Create a figure and axis
fig, ax = plt.subplots()
ax.set_title('Click to add points')

# Connect the click event to the onclick function
cid = fig.canvas.mpl_connect('button_press_event', onclick)

# List to store hull lines for removal
hull_lines = []

mplcursors.cursor(hover=True)
plt.show()
