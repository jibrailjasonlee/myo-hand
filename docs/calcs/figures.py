"""Draws the pictures in docs/figures/ from the calc scripts, so they can't drift from the maths.

    python3 docs/calcs/figures.py
"""
from math import radians, cos, sin
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb

import closing_order as co
import joint_range as jr
import tendon_path as tp

OUT = Path(__file__).resolve().parents[1] / "figures"
GREY, TEAL, RED, ORANGE, BLUE = "#b9c3cb", "#4aa8a0", "#d9480f", "#f0b429", "#1f5fbf"
PX = 0.05  # half a grid cell, mm


def render(ax, a, b, deg, xlim, ylim, highlight=None, mark_overlap=True):
    """Link A grey, link B teal, overlap red. B is rotated by deg about the pin at the origin."""
    t = radians(deg)
    xb = jr.X * cos(t) - jr.Y * sin(t)
    yb = jr.X * sin(t) + jr.Y * cos(t)
    ma, mb = a(jr.X, jr.Y), b(xb, yb)
    img = np.ones(ma.shape + (3,))
    img[ma] = to_rgb(GREY)
    if highlight is not None:
        img[highlight(jr.X, jr.Y)] = to_rgb(ORANGE)
    img[mb] = to_rgb(TEAL)
    if mark_overlap:
        img[ma & mb] = to_rgb(RED)
    ext = (jr.g[0] - PX, jr.g[-1] + PX, jr.g[0] - PX, jr.g[-1] + PX)
    ax.imshow(img, origin="lower", extent=ext, interpolation="nearest")
    ax.plot(0, 0, "k.", ms=7)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.set_xlabel("x, palm side (mm)")
    ax.set_ylabel("y, along finger (mm)")


def tendon_figure():
    r, yp, yd = 9.0, -12.0, 12.5  # the PIP guide pair
    a = lambda x, y: jr.ears(None)(x, y) | jr.a_guide(x, y)
    b = lambda x, y: jr.b_tongue(x, y) | jr.b_guide(x, y)

    fig = plt.figure(figsize=(12, 8.5), constrained_layout=True)
    gs = fig.add_gridspec(2, 3)
    for i, deg in enumerate((0, 45, 90)):
        ax = fig.add_subplot(gs[0, i])
        render(ax, a, b, deg, (-15, 40), (-28, 38), mark_overlap=False)
        t = radians(deg)
        p, q = (r, yp), (r * cos(t) + yd * sin(t), -r * sin(t) + yd * cos(t))
        ax.plot([p[0], q[0]], [p[1], q[1]], color=BLUE, lw=2.5)
        ax.plot(*p, "o", color=BLUE, ms=5)
        ax.plot(*q, "o", color=BLUE, ms=5)
        ax.set_title(f"{deg} deg: cord between guides {tp.cord_length(t, r, yp, yd):.1f} mm",
                     fontsize=10)
    axs = fig.axes
    axs[0].text(-13, -26, "grey: proximal link, teal: distal link,\nblue: cord, dot: pin",
                fontsize=8, va="bottom")

    ax = fig.add_subplot(gs[1, :2])
    deg = np.arange(0, 101, 1.0)
    pairs = (("MCP (guides at -12 and 12), to 90 deg", -12, 12, BLUE, 90),
             ("PIP (-12 and 12.5), to 100 deg", -12, 12.5, "#d98b0f", 100),
             ("DIP (-12.5 and 15), to 80 deg", -12.5, 15, "#0a7a73", 80))
    for name, yp_, yd_, c, top in pairs:
        d_ = deg[deg <= top]
        ax.plot(d_, [tp.pulled(radians(d), r, yp_, yd_) for d in d_], color=c, label=name)
    ax.plot(deg, [tp.pulled(radians(d), 5, 5.59, 8) for d in deg], color=RED, ls="--",
            label="tunnel across the slot (r=5): goes negative")
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xlabel("joint angle (deg)")
    ax.set_ylabel("cord taken up (mm)")
    ax.set_title("How much cord each joint uses up")
    ax.legend(fontsize=8)

    ax = fig.add_subplot(gs[1, 2])
    for name, yp_, yd_, c, top in pairs:
        d_ = deg[deg <= top]
        ax.plot(d_, [tp.arm(radians(d), r, yp_, yd_) for d in d_], color=c)
    ax.set_xlabel("joint angle (deg)")
    ax.set_ylabel("torque per newton of cord (mm)")
    ax.set_title("Moment arm: starts at 9, grows")
    ax.set_ylim(0, 18)
    fig.savefig(OUT / "tendon_path.png", dpi=140)
    plt.close(fig)


def range_figure():
    a_t = lambda x, y: jr.slot_bottom(x, y) | jr.a_guide(x, y)
    b_t = lambda x, y: jr.b_tongue(x, y) | jr.b_guide(x, y)
    block = lambda x, y: jr.ears(7.8)(x, y) & ~jr.ears(None)(x, y)

    fig, axs = plt.subplots(2, 2, figsize=(11, 10.5), constrained_layout=True)
    big_x, big_y = (-22, 40), (-30, 40)
    render(axs[0, 0], a_t, b_t, 0, big_x, big_y)
    axs[0, 0].set_title("Tongue layer, straight: the tongue sits in the slot", fontsize=10)
    render(axs[0, 1], a_t, b_t, 97, big_x, big_y)
    axs[0, 1].set_title("Tongue layer, flexion past 94.5 deg (shown at 97): the side of\n"
                        "the body runs into the slot-bottom corner (red)", fontsize=10)
    render(axs[1, 0], jr.ears(None), jr.b_full, -97, big_x, big_y)
    axs[1, 0].set_title("Ear layer, no stop, extension past 94 deg (shown at 97):\nthe shoulder runs into the back of the ears (red)",
                        fontsize=10)
    render(axs[1, 1], jr.ears(7.8), jr.b_full, -3, (-14, 6), (-4, 14), highlight=block)
    axs[1, 1].set_title("Ear layer with the stop (orange), zoomed, 3 deg of extension:\n"
                        "the shoulder meets the stop face (red)", fontsize=10)
    axs[1, 1].text(-13.5, -3.5, "stop face at y=7.8, shoulder at y=8: 0.2 mm of play",
                   fontsize=8, va="bottom")
    fig.savefig(OUT / "joint_range.png", dpi=140)
    plt.close(fig)


def order_figure():
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.8), constrained_layout=True)
    colors = {"MCP": BLUE, "PIP": "#d98b0f", "DIP": "#0a7a73"}
    for ax, title, f0s in ((axs[0], "Equal elastic preload (0.3 N each)", (0.3, 0.3, 0.3)),
                           (axs[1], "Graded preload (0.2 / 0.3 / 0.45 N)", (0.2, 0.3, 0.45))):
        for (name, (_, _, top)), f0 in zip(co.JOINTS.items(), f0s):
            deg = np.arange(0, top + 1, 1.0)
            ax.plot(deg, [co.tension_at(d, name, f0) for d in deg], color=colors[name], label=name)
        ax.axvline(30, color="k", lw=0.6, ls=":")
        ax.set_xlabel("joint angle (deg)")
        ax.set_ylabel("cord tension needed to hold it there (N)")
        ax.set_title(title)
        ax.set_ylim(0, 1.5)
        ax.legend()
    axs[1].text(31, 0.05, "30 deg", fontsize=8)
    fig.savefig(OUT / "closing_order.png", dpi=140)
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    tendon_figure()
    range_figure()
    order_figure()
    print("wrote", ", ".join(sorted(p.name for p in OUT.glob("*.png"))))
