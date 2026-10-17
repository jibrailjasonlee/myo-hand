# Requirements: Low-Cost Underactuated Hand (Research Prototype)

**Version:** 0.1 (Phase 0)
**Last updated:** 2026-10-17
**Status:** Draft, pending Phase 1 validation of assumptions

## 1. Problem statement

Robotic and prosthetic hands are either expensive (rigid, sensor-heavy) or cheap and unreliable. Design a hand under CAD $80 that grasps everyday objects reliably without per-object tuning, using an underactuated, tendon-driven mechanism, and verify the result with measured data.

## 2. Scope

**In scope**
- Four fingers driven by one actuator through an underactuated differential mechanism.
- Thumb with two postures (power opposition and pinch), driven by a second actuator.
- Single-channel surface EMG (forearm) for open/close, with a gesture to switch thumb posture.
- Benchtop and mock-forearm testing only.

**Out of scope**
- Individual finger control, wrist rotation, sensory feedback.
- Any use by or on a person with a limb difference.
- Picking objects flat off a table (objects are presented in a fixture or on a ledge).

## 3. Constraints

| ID | Constraint |
|----|------------|
| C1 | Research prototype, not a medical device. No clinical claims. |
| C2 | Battery-powered only. No mains connection to any part touching the body. |
| C3 | Every printed part fits within the Bambu A1 Mini bed (180 x 180 x 180 mm). |
| C4 | Total cost at most $80 CAD, including shipping to Toronto. |
| C5 | Finger proportions scaled to a human index finger (see section 5). |

## 4. Requirements

Priority: **Must** = defines project success. **Should** = expected, can be descoped with justification. **Could** = nice to have. **Stretch** = gated by a go/no-go decision.

| ID | Requirement | Basis | Priority | Verification | Status |
|----|-------------|-------|----------|--------------|--------|
| R1 | Hold the MoYu WeiLong V10 cube (65 g) and an Xbox controller with 2 AA batteries (295 g) for 30 s without slip | Friction model (section 6) | Must | Hold test, repeated trials, record pass/fail | Open |
| R2 | At least 1.5 N fingertip force per finger, all four fingers | Controller hold, SF 2, mu 0.5 | Must | Press fingertip on a scale, record force | Open |
| R3 | Open aperture at least 100 mm | Object sizes (cube body diagonal about 95 mm, controller wider) | Must | Caliper measurement | Open |
| R4 | Minimum controllable grip force at most 0.2 N, with resolution at most 0.05 N | Potato chip | Stretch | Force vs. position test on single-finger rig | Open |
| R5 | Hold a potato chip with at most 10% breakage over 30 trials | Potato chip | Stretch (gated, see section 7) | 30-trial test, report confidence interval | Open |
| R6 | Full close time at most 1.5 s | Usability | Should | Video or stopwatch | Open |
| R7 | Hand mass at most 500 g | Wearability (target to be checked against prosthetics literature) | Should | Kitchen scale | Open |
| R8 | Hold a grip with zero actuator power | Battery life | Could | Power-off hold test | Open |
| R9 | Total cost at most $80 CAD | Project constraint C4 | Must | Bill of materials total | Open |

## 5. Measured inputs

| Item | Value | Source |
|------|-------|--------|
| Rubik's cube (MoYu WeiLong V10) mass | about 65 g | Measured by author |
| Xbox controller with 2 AA batteries | 295 g | Measured by author |
| Index finger segment lengths (proximal, middle, distal) | 45, 25, 23 mm | Measured by author |
| Palm width across knuckles | 74 mm | Measured by author |
| Finger width per digit | 17 mm (74 mm / 4, minus gap) | Derived |
| Chip | No-name chip, No Frills | Breakage force not yet measured |

## 6. Derived values and calculations

Holding condition for a two-sided grasp: `N >= SF * W / (2 * mu)`.

| Object | Weight W | Required normal force |
|--------|----------|----------------------|
| Cube | 0.64 N | about 1.3 N total |
| Controller | 2.9 N | about 5.8 N per side, about 1.45 N per finger over four fingers |
| Chip | about 0.02 N (estimated) | about 0.04 N |

Required force range from chip to controller is roughly 50:1.

Tendon tension estimate: `T = F * L / r`, with F = 1.5 N, L = 93 mm (fingertip-only contact), r = proximal pulley radius.

| Pulley radius | Tension per finger | Spool rotation (6 mm spool, about 30 mm stroke) |
|---------------|--------------------|-------------------------------------------------|
| 5 mm | about 28 N | about 290 degrees |
| 4 mm | about 34.9 N | about 233 degrees |

Estimated actuator torque: roughly 0.7 N.m (wrap grasp) to 1.3 N.m (fingertip-only pinch) at the motor output, assuming 50% transmission efficiency. Order of magnitude only.

Calculation scripts should be placed in `docs/calcs/` and referenced here.

## 7. Stretch gate (R4, R5)

After the Phase 1 single-finger rig is built, measure force vs. position on a TPU pad.
- **Go:** the curve is smooth and repeatable enough to reach about 0.05 N resolution. Keep R4 and R5.
- **No-go:** friction and hysteresis make it erratic. Drop R4 and R5, document the reason in `decisions.md`, and record the measured data.

## 8. Assumptions to validate

| ID | Assumption | Value | Status | How to validate |
|----|------------|-------|--------|-----------------|
| A1 | Friction coefficient, TPU pad on object | 0.5 (conservative) | Unverified | Tilt test with printed TPU swatch |
| A2 | Safety factor | 2 | Unverified | Review after Phase 1 data |
| A3 | Transmission efficiency (tendon plus gearing) | 50% | Unverified | Measure tension in vs. fingertip force out |
| A4 | Joint flexion ranges (MCP, PIP, DIP) | 90, 100, 80 degrees | Unverified | Check against measurements and literature |
| A5 | Chip fracture force | Unknown | Not measured | Coin-loading test or Phase 1 rig |
| A6 | Tendon stroke allowance for differential | +30% | Unverified | Check in CAD and on the rig |
| A7 | Hand mass target | 500 g | Unverified | Compare to prosthetics literature |

## 9. Change log

| Date | Change |
|------|--------|
| 2026-10-17 | v0.1 created from Phase 0 discussion. Torque estimate revised from about 0.7 N.m to 0.7 to 1.3 N.m after using measured finger length (93 mm). Chip requirements moved to Stretch with Phase 1 gate. |
