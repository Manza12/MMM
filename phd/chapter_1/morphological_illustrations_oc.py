import bezier
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as m_patches
from matplotlib.legend_handler import HandlerPatch


class FilledCircleHandler(HandlerPatch):
    def create_artists(self, legend, orig_handle, x_descent, y_descent, width, height, font_size, trans):
        center = 0.5 * width - 0.5 * x_descent, 0.5 * height - 0.5 * y_descent
        height /= 1.2
        p = m_patches.Circle(xy=center, radius=min(width + x_descent, height + y_descent))
        self.update_prop(p, orig_handle, legend)
        p.set_transform(trans)
        return [p]


class FilledRectangleHandler:
    def __init__(self, color):
        self.color = color

    def legend_artist(self, legend, orig_handle, font_size, handle_box):
        unused_params = [legend, orig_handle, font_size]
        assert len(unused_params) == 3

        x0, y0 = handle_box.xdescent, handle_box.ydescent
        width, height = handle_box.width, handle_box.height
        patch_fill = m_patches.Rectangle((x0, y0), width, height, facecolor=self.color, linestyle='', alpha=0.1,
                                         transform=handle_box.get_transform())
        patch_line = m_patches.Rectangle((x0, y0), width, height, fill=False, edgecolor=self.color, linestyle='-',
                                         transform=handle_box.get_transform())
        handle_box.add_artist(patch_line)
        handle_box.add_artist(patch_fill)
        return patch_line


class DashedFilledRectangleHandler:
    def __init__(self, color):
        self.color = color

    def legend_artist(self, legend, orig_handle, font_size, handle_box):
        unused_params = [legend, orig_handle, font_size]
        assert len(unused_params) == 3

        x0, y0 = handle_box.xdescent, handle_box.ydescent
        width, height = handle_box.width, handle_box.height
        patch_fill = m_patches.Rectangle((x0, y0), width, height, facecolor=self.color, linestyle='', alpha=0.1,
                                         transform=handle_box.get_transform())
        patch_line = m_patches.Rectangle((x0, y0), width, height, fill=False, edgecolor=self.color, linestyle='--',
                                         transform=handle_box.get_transform())
        handle_box.add_artist(patch_line)
        handle_box.add_artist(patch_fill)
        return patch_line


def generate_nodes(nd_1, ctrl_1, nd_2, ctrl_2):
    return np.asfortranarray([
        [nd_1[0], nd_1[0] + ctrl_1[0], nd_2[0] + ctrl_2[0], nd_2[0]],
        [nd_1[1], nd_1[1] + ctrl_1[1], nd_2[1] + ctrl_2[1], nd_2[1]]
    ])


def get_interior_points(pts, dist):
    i_pts = np.zeros_like(pts)
    for p in range(pts.shape[1]):
        p_1 = pts[:, p - 1]
        p_2 = pts[:, p]
        p_3 = pts[:, (p + 1) % pts.shape[1]]

        v = p_3 - p_1
        v_ortho = np.array([v[1], - v[0]])
        v_norm = v_ortho / np.linalg.norm(v_ortho, 2)

        pt = p_2 + v_norm * dist
        i_pts[:, p] = pt
    return i_pts


def get_exterior_points(pts, dist):
    e_pts = np.zeros_like(pts)
    for p in range(pts.shape[1]):
        p_1 = pts[:, p - 1]
        p_2 = pts[:, p]
        p_3 = pts[:, (p + 1) % pts.shape[1]]

        v = p_3 - p_1
        v_ortho = np.array([v[1], - v[0]])
        v_norm = v_ortho / np.linalg.norm(v_ortho, 2)

        pt = p_2 - v_norm * dist
        e_pts[:, p] = pt
    return e_pts


# Parameters
n = 200
d = 0.2
alpha = 0.15
colour_dilation = 'green'

node_1 = np.array([0, 0])
node_2 = np.array([2, 1])
node_3 = np.array([4, 0])
node_4 = np.array([2, -1])

controller_1 = np.array([0, 1])
controller_2 = np.array([-0.5, 1])
controller_3 = np.array([0, 0.5])
controller_4 = np.array([0.5, -1])

nodes_1 = generate_nodes(node_1, controller_1, node_2, controller_2)
nodes_2 = generate_nodes(node_2, -controller_2, node_3, controller_3)
nodes_3 = generate_nodes(node_3, -controller_3, node_4, controller_4)
nodes_4 = generate_nodes(node_4, -controller_4, node_1, -controller_1)

curve_1 = bezier.Curve(nodes_1, degree=3)
curve_2 = bezier.Curve(nodes_2, degree=3)
curve_3 = bezier.Curve(nodes_3, degree=3)
curve_4 = bezier.Curve(nodes_4, degree=3)

s_vals = np.linspace(0.0, 1.0, n)
points_1 = curve_1.evaluate_multi(s_vals)
points_2 = curve_2.evaluate_multi(s_vals)
points_3 = curve_3.evaluate_multi(s_vals)
points_4 = curve_4.evaluate_multi(s_vals)

points = np.concatenate([points_1, points_2, points_3, points_4], axis=1)
nodes = np.stack([node_1, node_2, node_3, node_4], axis=1)

# Plot
fig_size = (4.5, 3.)
fig_1, ax_1 = plt.subplots(figsize=fig_size)
fig_2, ax_2 = plt.subplots(figsize=fig_size)
axs = [ax_1, ax_2]

# Shape
upper_points = np.concatenate([points_1, points_2], axis=1)
lower_points = np.concatenate([points_3, points_4], axis=1)

x = np.linspace(node_1[0], node_3[0], 2 * n)

r_in = d / 1.5
x_circle = np.linspace(2 - r_in, 2 + r_in, n // 2)
f_plus = np.sqrt(r_in ** 2 - (x_circle - 2) ** 2)
f_minus = -np.sqrt(r_in ** 2 - (x_circle - 2) ** 2)

y_l = np.interp(x, np.flip(lower_points[0, :]), np.flip(lower_points[1, :]))
y_u = np.interp(x, upper_points[0, :], upper_points[1, :])
#
# s_1 = x - 2 < -r_in
# s_2 = x - 2 > r_in
# s = np.logical_and(np.logical_not(s_1), np.logical_not(s_2))
fill_u = None
for i in range(2):
    line = axs[i].plot(points[0, :], points[1, :], '-')
    fill = axs[i].fill_between(x, y_l, y_u, alpha=alpha, color='tab:blue')

fill_circle = axs[0].fill_between(x_circle, f_minus, f_plus, color='white')
line_circle = axs[0].add_patch(m_patches.Circle((2, 0), r_in, fill=False, color='tab:blue', lw=1.5))

circle_center = (1, -1.2)
r_out = d / 1.5

axs[1].add_patch(m_patches.Circle(circle_center, r_out, fill=False, color='tab:blue', lw=1.5))
axs[1].add_patch(m_patches.Circle(circle_center, r_out, color='tab:blue', lw=0, alpha=alpha))

# Plot str el
str_el_center = (0, 1.7)
str_el_line = None
str_el_fill = None
origin = None
for i in range(2):
    str_el_line = axs[i].add_patch(m_patches.Circle(str_el_center, d, fill=False, color='red', lw=2))
    str_el_fill = axs[i].add_patch(m_patches.Circle(str_el_center, d, fill=True, color='red', lw=0, alpha=alpha))
    origin = axs[i].scatter(str_el_center[0], str_el_center[1], marker='x', color='r')

# Export
for i in range(2):
    axs[i].set_xticks([])
    axs[i].set_yticks([])
    axs[i].set_aspect('equal', 'box')
    axs[i].set_xlim([-0.5, 5])
    axs[i].set_ylim([-1.7, 2.5])

axs[0].legend([fill_u, (str_el_fill, str_el_line), origin],
              ['opening', 'structuring\nelement', '$0$'],
              handler_map={fill_u: FilledRectangleHandler('tab:blue'),
                           str_el_fill: FilledCircleHandler(),
                           str_el_line: FilledCircleHandler()},
              loc='upper right')
axs[1].legend([fill_u, (str_el_fill, str_el_line), origin],
              ['closing', 'structuring\nelement', '$0$'],
              handler_map={fill_u: FilledRectangleHandler('tab:blue'),
                           str_el_fill: FilledCircleHandler(),
                           str_el_line: FilledCircleHandler()},
              loc='upper right')

fig_1.tight_layout()
fig_2.tight_layout()
fig_1.savefig('opening.svg', transparent=True)
fig_2.savefig('closing.svg', transparent=True)
plt.show()
