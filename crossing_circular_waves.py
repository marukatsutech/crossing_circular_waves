# Crossing circular waves with crossing points
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import matplotlib.patches as patches


def set_axis():
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_title('Crossing circular waves')
    ax.set_xlabel('x * pi')
    ax.set_ylabel('y * pi')
    ax.grid()
    ax.set_aspect("equal")


def circumscribed_point(p0, r0, p1, r1):
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    ratio = r0 / (r0 + r1)
    return (
        (p0[0] + dx * ratio), (p0[1] + dy * ratio)
    )


def inscribed_point(p0, r0, p1, r1):
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    ratio = - r0 / (r1 - r0)
    return (
        (p0[0] + dx * ratio), (p0[1] + dy * ratio)
    )


def circles_cross_points(p0, r0, p1, r1, d):
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    ratio = r0 / d
    v = (dx * ratio, dy * ratio)    # Vector from p0 to p1 as same length as r0
    cos_alpha = (r0**2 + d**2 - r1**2) / (2 * r0 * d)   # Cosine formula
    sin_alpha = np.sqrt(1 - cos_alpha**2)
    rot_plus = np.array([[cos_alpha, - sin_alpha], [sin_alpha, cos_alpha]])  # Matrix of rotation
    rot_minus = np.array([[cos_alpha, sin_alpha], [- sin_alpha, cos_alpha]])  # Matrix of reverse rotation
    v_plus = np.dot(rot_plus, v)    # rotate
    v_minus = np.dot(rot_minus, v)
    return (
        (p0[0] + v_plus[0], p0[1] + v_plus[1]),
        (p0[0] + v_minus[0], p0[1] + v_minus[1])
    )


def get_cross_status(d, r0, r1):
    if abs(r0 - r1) <= tolerance and d <= tolerance:    # r0 == r1 and d = 0
        return 1  # Match
    else:
        if abs(d - (r0 + r1)) <= tolerance:  # d == r0 + r1
            return 2  # Circumscribed circles
        elif abs(abs(r0 - r1) - d) <= tolerance:  # abs(r0 - r1) == d
            return 3  # Inscribed circles
        else:
            if d > (r0 + r1):  # d > r0 + r1
                return 4  # Not cross
            elif abs(r0 - r1) > d:  # abs(r0 - r1) > d
                return 5  # Not cross (Included circles)
            elif abs(r0 - r1) < d < abs(r0 + r1):   # abs(r0 - r1) < d < r0 + r1
                return 6  # Cross
            else:
                return 0    # Error


def draw_crossing_points(cross_status, p0, r0, p1, r1, d):
    if cross_status == 2:
        cp = circumscribed_point(p0, r0, p1, r1)
        circle_cp = patches.Circle(xy=cp, radius=cp_r, color="red")
        ax.add_patch(circle_cp)
    elif cross_status == 3:
        cp = inscribed_point(p0, r0, p1, r1)
        circle_cp = patches.Circle(xy=cp, radius=cp_r, color="red")
        ax.add_patch(circle_cp)
    elif cross_status == 6:
        cp0, cp1 = circles_cross_points(p0, r0, p1, r1, d)
        circle_cp0 = patches.Circle(xy=cp0, radius=cp_r, color="red")
        circle_cp1 = patches.Circle(xy=cp1, radius=cp_r, color="red")
        ax.add_patch(circle_cp0)
        ax.add_patch(circle_cp1)
    else:
        pass


def draw_crossing_points_of_circles(c1, c2):
    for i in c1:
        x1 = i[0]
        y1 = i[1]
        r1 = i[2]
        for j in c2:
            x2 = j[0]
            y2 = j[1]
            r2 = j[2]
            point1 = np.array([x1, y1])
            point2 = np.array([x2, y2])
            pv = point2 - point1  # Vector from p1 to p1
            d = np.linalg.norm(pv, 2)  # Norm of vector pv
            cross_status = get_cross_status(d, r1, r2)
            draw_crossing_points(cross_status, point1, r1, point2, r2, d)


def draw_circles(c, col, lst):
    for i in c:
        x = i[0]
        y = i[1]
        r = i[2]
        c = patches.Circle(xy=(x, y), radius=r, fill=False, ec=col, ls=lst)
        ax.add_patch(c)


def draw_graph():
    ax.cla()
    set_axis()
    global circles_crest_right, circles_crest_left, circles_trough_right, circles_crest_left
    # Draw circles
    circles_crest_right.clear()
    circles_crest_left.clear()
    circles_trough_right.clear()
    circles_trough_left.clear()
    for i in range(num_circles):
        wave_len = 2. / k
        r_crest = i * wave_len + wave_len / 4.
        circles_crest_right.append((x_right_circles, y_right_circles, r_crest))
        circles_crest_left.append((x_left_circles, y_left_circles, r_crest))
        r_trough = i * wave_len + wave_len * 3 / 4.
        circles_trough_right.append((x_right_circles, y_right_circles, r_trough))
        circles_trough_left.append((x_left_circles, y_left_circles, r_trough))
    draw_circles(circles_trough_right, 'blue', '--')
    draw_circles(circles_trough_left, 'blue', '--')
    draw_circles(circles_crest_right, 'red', '-')
    draw_circles(circles_crest_left, 'red', '-')
    draw_crossing_points_of_circles(circles_crest_right, circles_crest_left)
    canvas.draw()
    ax.grid()


def change_distance(value):
    global x_right_circles, x_left_circles
    x_right_circles = float(value) / 2.
    x_left_circles = - float(value) / 2.
    draw_graph()


def change_k(value):
    global k
    k = float(value)
    draw_graph()


def change_radius_crossing_points(value):
    global cp_r
    s = float(value)
    cp_r = min([x_max - x_min, y_max - y_min]) * s
    draw_graph()


def change_num_circles(value):
    global num_circles
    num_circles = value
    draw_graph()


# Global variables
x_min = -5.
x_max = 5.
y_min = -5.
y_max = 5.
k = 1.
num_circles = 3

x_right_circles = 0.
y_right_circles = 0.
x_left_circles = 0.
y_left_circles = 0.
distance = abs(x_right_circles - x_left_circles)
circles_crest_right = []
circles_crest_left = []
circles_trough_right = []
circles_trough_left = []

tolerance = 1 / 1000000
size_cpr = 0.01        # Radius of crossing points
cp_r = min([x_max - x_min, y_max - y_min]) * size_cpr   # Radius of crossing points

# Generate tkinter
root = tkinter.Tk()
root.title("Crossing circular waves")

# Generate figure and axes
fig = Figure(figsize=(8, 6))
ax = fig.add_subplot(1, 1, 1)

# Embed Figure in canvas
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack()

# Draw circles as initial
draw_graph()

# Add toolbar
toolbar = NavigationToolbar2Tk(canvas, root)

# Label and spinbox to change parameters
# Distance between 2 points of right and left circles
label_distance = tkinter.Label(root, text="Distance")
label_distance.pack(side='left')
var_d = tkinter.StringVar(root)  # variable for spinbox-value
var_d.set(distance)  # Initial value
s_d = tkinter.Spinbox(
    root, textvariable=var_d, format="%.1f", from_=0., to=10., increment=0.5,
    command=lambda: change_distance(var_d.get()), width=5
    )
s_d.pack(side='left')
# k
label_k = tkinter.Label(root, text=" ,k(Wave number)")
label_k.pack(side='left')
var_k = tkinter.StringVar(root)  # variable for spinbox-value
var_k.set(distance)  # Initial value
s_k = tkinter.Spinbox(
    root, textvariable=var_k, format="%.1f", from_=1., to=10., increment=1.,
    command=lambda: change_k(var_k.get()), width=5
    )
s_k.pack(side='left')
# Radius of crossing point dots
label_cpr = tkinter.Label(root, text=" ,Radius of crossing points")
label_cpr.pack(side='left')
var_cpr = tkinter.StringVar(root)  # variable for spinbox-value
var_cpr.set(size_cpr)  # Initial value
s_cpr = tkinter.Spinbox(
    root, textvariable=var_cpr, format="%.3f", from_=0.001, to=0.01, increment=0.001,
    command=lambda: change_radius_crossing_points(var_cpr.get()), width=5
    )
s_cpr.pack(side='left')
# Number of circles
label_num = tkinter.Label(root, text="Number of circles")
label_num.pack(side='left')
var_num = tkinter.IntVar(root)  # variable for spinbox-value
var_num.set(num_circles)  # Initial value
s_num = tkinter.Spinbox(
    root, textvariable=var_num, from_=1, to=50, increment=1,
    command=lambda: change_num_circles(var_num.get()), width=4
    )
s_num.pack(side='left')

# main loop
set_axis()
root.mainloop()
