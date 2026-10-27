"""Range of one finger joint, checked in 2D.

Proximal link A (ears, slot) and distal link B (tongue) share a pin at the
origin. B swings toward +x (palm side) in flexion. Ears and tongue sit in
different z layers, so each layer is checked separately.

    python3 docs/calcs/joint_range.py
"""
import numpy as np

R = 7.5      # end radius, half the 15 mm depth
LB = 25.0    # pin to pin on the distal link (link 2)
SLOT = 8.0   # slot bottom behind the pin
SHOULDER = 8.0  # tongue shoulder past the pin

g = np.arange(-30, 45, 0.1)
X, Y = np.meshgrid(g, g)


def ears(stop):
    def a(x, y):
        m = ((np.abs(x) <= R) & (y <= 0)) | (x**2 + y**2 <= R**2)
        if stop is not None:  # flat stop on the back half of the ears
            m |= (x >= -R) & (x <= -2) & (y >= 0) & (y <= stop)
        return m
    return a


def b_full(x, y):  # distal link past the shoulder, full width
    body = ((np.abs(x) <= R) & (y <= LB)) | (x**2 + (y - LB)**2 <= R**2)
    return body & (y >= SHOULDER)


def slot_bottom(x, y):
    return (np.abs(x) <= R) & (y <= -SLOT)


def a_guide(x, y):  # 2 mm long, 3 mm tall, 12 mm behind the pin
    return (x >= R) & (x <= R + 3) & (y >= -13) & (y <= -11)


def b_tongue(x, y):
    return (((np.abs(x) <= R) & (y >= 0) & (y <= LB)) | (x**2 + y**2 <= R**2)
            | (x**2 + (y - LB)**2 <= R**2))


def b_guide(x, y):  # 12.5 mm past the pin
    return (x >= R) & (x <= R + 3) & (y >= 11.5) & (y <= 13.5)


def hit(deg, a, b):
    t = np.radians(deg)
    xb = X * np.cos(t) - Y * np.sin(t)
    yb = X * np.sin(t) + Y * np.cos(t)
    return bool(np.any(a(X, Y) & b(xb, yb)))


def first_contact(sign, a, b):
    for d in np.arange(0, 125, 0.5):
        if hit(sign * d, a, b):
            return d
    return None


if __name__ == "__main__":
    print("ears vs distal link, first contact in degrees")
    for stop in (None, 7.8):
        a = ears(stop)
        print(f"  stop face at y={stop}: flexion {first_contact(1, a, b_full)}, "
              f"extension {first_contact(-1, a, b_full)}")

    print("\ntongue layer, flexion / extension")
    for an, a in (("slot bottom", slot_bottom), ("link guide", a_guide)):
        for bn, b in (("tongue/body", b_tongue), ("distal guide", b_guide)):
            print(f"  {an:11s} vs {bn:12s}: {first_contact(1, a, b)} / {first_contact(-1, a, b)}")
