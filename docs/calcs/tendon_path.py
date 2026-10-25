"""Cord length across one finger joint.

The cord runs straight between a guide on the proximal link and a guide on
the distal link. Pin at the origin, finger along +y, palm side is +x.
Flexion swings the distal link toward +x.

    python3 docs/calcs/tendon_path.py
"""
from math import cos, sin, hypot, radians


def cord_length(theta, r, y_prox, y_dist):
    # only the distal guide moves; the proximal one is fixed to the proximal link
    qx = r * cos(theta) + y_dist * sin(theta)
    qy = -r * sin(theta) + y_dist * cos(theta)
    return hypot(qx - r, qy - y_prox)


def pulled(theta, r, y_prox, y_dist):
    # cord you have to take up at the actuator to reach this angle
    return cord_length(0, r, y_prox, y_dist) - cord_length(theta, r, y_prox, y_dist)


def arm(theta, r, y_prox, y_dist, h=1e-4):
    # torque per newton of tension = d(pulled)/d(theta)
    return (pulled(theta + h, r, y_prox, y_dist)
            - pulled(theta - h, r, y_prox, y_dist)) / (2 * h)


def show(name, r, y_prox, y_dist, top_deg):
    print(f"\n{name}  (r={r}, proximal guide y={y_prox}, distal guide y={y_dist})")
    print("  deg   pulled mm   arm mm")
    for d in list(range(0, top_deg, 15)) + [top_deg]:
        t = radians(d)
        print(f"  {d:3d}   {pulled(t, r, y_prox, y_dist):8.1f}   {arm(t, r, y_prox, y_dist):6.1f}")
    t = radians(top_deg)
    return pulled(t, r, y_prox, y_dist)


if __name__ == "__main__":
    # what D-012 first assumed: a tunnel at 5 mm that stops at the ear ends and
    # the next link's shoulder, so both mouths are past the pin
    show("tunnel across the slot", 5, 5.59, 8, 90)

    # guides on the palm face, 9 mm off the axis, either side of each joint
    r = 9
    mcp = show("MCP: palm guide to link 1 guide at y=12", r, -12, 12, 90)
    pip = show("PIP: link 1 guide at y=33 to link 2 guide at y=57.5", r, -12, 12.5, 100)
    dip = show("DIP: link 2 guide at y=57.5 to tip anchor at y=89", r, -12.5, 19, 80)
    print(f"\ntotal cord to take up, all three joints fully closed: {mcp + pip + dip:.0f} mm")

    # fingertip-only push, straight finger (arm is smallest here, so worst case)
    f_tip, finger_len = 1.5, 93
    print(f"tension for {f_tip} N at the tip, straight finger: {f_tip * finger_len / r:.1f} N")
