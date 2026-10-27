"""Which joint closes first, for a given elastic return spring on the back.

Each joint balances cord torque against the elastic:
    T * arm(theta) = tau0 + k * theta
tau0 and k come from an elastic of stiffness ke held a distance rd behind the
pin with preload f0. Cord tension T is the same at every joint here, which
ignores friction in the guides. Elastic numbers are guesses until the cord
test measures them.

    python3 docs/calcs/closing_order.py
"""
from math import radians
import numpy as np
from tendon_path import arm

R = 9.0                  # cord arm in a straight finger, mm
RD = 6.0                 # elastic distance behind the pin, mm
KE = 0.3                 # elastic stiffness, N/mm (guess)
JOINTS = {               # y_prox, y_dist of the guides, max flexion in deg
    "MCP": (-12.0, 12.0, 90),
    "PIP": (-12.0, 12.5, 100),
    "DIP": (-12.5, 15.0, 80),
}


def tension(theta, joint, f0):
    y_prox, y_dist, _ = JOINTS[joint]
    return (RD * f0 + KE * RD**2 * theta) / arm(theta, R, y_prox, y_dist)


def tension_at(deg, joint, f0):
    return tension(radians(deg), joint, f0)


if __name__ == "__main__":
    for label, f0s in (("equal preload 0.3 N", (0.3, 0.3, 0.3)),
                       ("graded preload 0.2 / 0.3 / 0.45 N", (0.2, 0.3, 0.45))):
        print(f"\n{label}: cord tension in N to reach each angle")
        print("  joint   30 deg   60 deg   max")
        for (name, (_, _, top)), f0 in zip(JOINTS.items(), f0s):
            print(f"  {name}   {tension_at(30, name, f0):6.2f}   "
                  f"{tension_at(60, name, f0):6.2f}   {tension_at(top, name, f0):6.2f}  ({top} deg)")
