# Requirements

What the hand has to do, how I'll check each requirement, and the numbers behind them. Most numbers are estimates until the single-finger rig exists. The assumptions table at the bottom says which.

## The problem

Hands are either rigid and expensive or cheap and flaky. I want one under $80 CAD that picks up everyday objects without per-object tuning. It's tendon-driven and underactuated: one motor pulls all four fingers through a differential, so they wrap around whatever they touch.

## Scope

In: four fingers on one motor. A thumb with two postures (power and pinch) on a second motor. One forearm EMG channel for open/close, with a gesture to switch thumb posture. Testing on the bench and on a mock forearm.

Out: individual finger control, wrist rotation, force feedback, anyone with a limb difference actually using it, and picking things flat off a table (objects get presented on a ledge or in a fixture).

## Constraints

- Research prototype. No clinical claims.
- Battery power only. Nothing that touches the body ever connects to mains.
- Every printed part fits in the A1 Mini's 180 x 180 x 180 mm bed.
- $80 CAD all-in, shipping to Toronto included.
- Finger proportions come from my own index finger.

## Requirements

Must means the project fails without it. Should can be dropped with a reason. Could is nice to have. Stretch gets decided after the single-finger test (see below).

| ID | Requirement | Where it comes from | Priority | How I'll check |
|----|-------------|---------------------|----------|----------------|
| R1 | Hold the cube (65 g) and the Xbox controller (295 g, with 2 AA) for 30 s without slipping | Friction math below | Must | Hold test, repeated trials, pass/fail |
| R2 | At least 1.5 N fingertip force per finger, all four | Controller hold, SF 2, mu 0.5 | Must | Press a fingertip on a scale |
| R3 | Open aperture of at least 100 mm | Cube body diagonal is about 95 mm, controller is wider | Must | Calipers |
| R4 | Controllable grip force down to 0.2 N, with 0.05 N resolution | Potato chip | Stretch | Force vs. position on the single-finger rig |
| R5 | Hold a chip with at most 10% breakage over 30 trials | Potato chip | Stretch | 30 trials, report the confidence interval |
| R6 | Close in 1.5 s or less | Usability | Should | Video or stopwatch |
| R7 | Hand mass of 500 g or less | Wearability, still to check against prosthetics literature | Should | Kitchen scale |
| R8 | Hold a grip with zero motor power | Battery life | Could | Cut power, see if it holds |
| R9 | Total cost of $80 CAD or less | Project constraint | Must | Bill of materials |

## The numbers

Measured: cube about 65 g, controller with batteries 295 g, index finger segments 45, 25 and 23 mm, palm width 74 mm. That gives 17 mm per finger (74 / 4, minus a gap). I haven't measured the chip's breaking force yet. The chips are the no-name ones from No Frills.

Grip math. For a two-sided pinch you need N >= SF * W / (2 * mu). With SF = 2 and mu = 0.5:

- Cube (0.64 N): about 1.3 N total.
- Controller (2.9 N): about 5.8 N per side, so roughly 1.45 N per finger across four fingers.
- Chip (about 0.02 N, a guess): about 0.04 N.

Chip to controller is about 50:1 in force. That spread is the hard part of this project, more than raw strength.

Cord path. The cord runs along the palm face through small guides either side of each joint, 9 mm off the axis (see D-012 and docs/calcs/tendon_path.py). The arm is 9 mm in a straight finger and grows to about 15 mm as it closes.

- Cord to take up with all three joints closed (90 / 100 / 80 deg): about 61 mm per finger.
- Tension for 1.5 N at the tip with the finger straight: T = F * L / r = 1.5 * 93 / 9, about 15.5 N. It drops once the finger curls.
- Four fingers on a 6 mm spool: about 583 deg of rotation, and roughly 0.5 Nm (wrap grasp) to 0.75 Nm (tip pinch) at the motor, assuming 50% efficiency. A 10 mm spool cuts the rotation to 350 deg and raises the torque by two thirds.

Order of magnitude only. Guide friction will push the real efficiency below 50%.

## Chip gate

Once the single-finger rig exists, I'll measure force vs. position on a TPU pad. If the curve is smooth and repeatable enough for about 0.05 N resolution, R4 and R5 stay. If friction and hysteresis make it erratic, both get dropped, the reason goes in decisions.md, and the data stays in the repo.

## Assumptions

None of these are verified yet.

| ID | Assumption | How I'll check |
|----|------------|----------------|
| A1 | Friction coefficient of 0.5 for a TPU pad on the objects | Tilt test with a printed TPU swatch |
| A2 | Safety factor of 2 | Revisit after rig data |
| A3 | 50% efficiency through guides, cord and gearing | Tension in vs. fingertip force out |
| A4 | Joint ranges of 90 / 100 / 80 deg (MCP / PIP / DIP) | Compare against literature |
| A5 | Chip fracture force (unknown) | Coin loading, or the rig |
| A6 | 30% extra tendon stroke for the differential | Check in CAD and on the rig |
| A7 | 500 g is a sensible hand mass target | Compare against prosthetics literature |
