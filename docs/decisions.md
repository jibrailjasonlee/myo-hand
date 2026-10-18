# Decision Log

Each entry records a choice, why it was made, and what would make us revisit it. Newest entries go at the bottom. Never delete an old entry: if a decision changes, add a new entry that supersedes it.

**Status values:** Accepted, Hypothesis (to be tested), Superseded.

---

## D-001: Project direction, assistive/prosthetic underactuated hand
- **Date:** 2026-10-17
- **Status:** Accepted
- **Context:** The goal is a personal, low-cost project that solves a real engineering problem, builds skills used in robotics roles, and is independent of any team project. A fixed-pivot reaction-wheel pendulum and a rover state-estimation project were considered and set aside (the first as not impactful enough, the second as tied to a team).
- **Decision:** Build a low-cost underactuated tendon-driven hand, targeting the assistive/prosthetic use case, as a research prototype.
- **Consequences:** Heavy on mechanism design, force control, EMG signal processing, and embedded software. Not a medical device (constraint C1).
- **Revisit if:** Cost cap or timeline proves unachievable.

## D-002: Scope limited to two actuators and one EMG channel
- **Date:** 2026-10-17
- **Status:** Accepted
- **Context:** Individual finger control, wrist rotation, and sensory feedback are real research directions but would exceed a one-term timeline.
- **Decision:** One actuator closes four fingers through an underactuated differential. One actuator switches the thumb between power and pinch postures. Control uses one EMG channel.
- **Consequences:** Pattern-recognition grip selection needs a second EMG channel and is a stretch extension.

## D-003: Potato chip is a stretch goal with a Phase 1 gate
- **Date:** 2026-10-17
- **Status:** Accepted
- **Context:** The chip needs about 0.04 N holding force but must not exceed its breaking force, while the controller needs about 5.8 N per side. This is a roughly 50:1 force range and is the hardest requirement. Motor current is likely a poor force estimate at the low end because friction is comparable to a 0.1 N fingertip force. Soft, low-stiffness pads may give usable force from position alone (F = k * dx).
- **Decision:** Keep the cube, controller, aperture, and cost requirements (R1, R2, R3, R9) as the Must items. Move R4 and R5 to Stretch, and design in the thumb pinch posture and soft pads from the start. Decide go/no-go after the Phase 1 single-finger rig measures force vs. position on a TPU pad.
- **Consequences:** Project success does not depend on the chip. If no-go, the measured data is documented as the result.
- **Revisit:** After Phase 1 rig data.

## D-004: Baseline finger uses pin joints, palm-side tendon, and elastic return
- **Date:** 2026-10-17
- **Status:** Accepted (baseline), alternatives to be compared later
- **Context:** The simplest mechanism that works lets us build a first rig quickly. Flexure (TPU) fingers are a known alternative but add print-tuning risk and unknown fatigue life.
- **Decision:** Use pin joints (2 mm steel pin or M2 screw with nylock nut) at three joints per finger, a tendon on the palm side to close, and an elastic cord on the back to open. Finger link lengths are 45, 25, and 23 mm, and finger width is 17 mm.
- **Consequences:** Closing order of the joints is set by the ratio of return-spring stiffness to pulley radius (k_i / r_i). This ratio becomes a design parameter to sweep in simulation.
- **Revisit:** After the Phase 1 rig, compare against a flexure finger.

## D-005: Closing order target is proximal joint first (hypothesis)
- **Date:** 2026-10-17
- **Status:** Hypothesis
- **Context:** A proximal-first sequence gives the usual enveloping wrap, but a proximal-first finger may push light objects such as the cube away before the fingertip arrives.
- **Decision:** Start with proximal, then middle, then distal. Test other orders in a Python sweep over k_i / r_i before building.
- **Revisit:** If simulation or the rig shows objects being pushed away.

## D-006: Pulleys as large as the finger envelope allows, remaining ratio in the motor gearing (hypothesis)
- **Date:** 2026-10-17
- **Status:** Hypothesis
- **Context:** Pulley radius acts as a gear ratio. A smaller radius means less tendon travel but more tendon force (5 mm radius: about 28 N and about 290 degrees of spool rotation; 4 mm radius: about 34.9 N and about 233 degrees). Larger pulleys add no parts or backlash and lower tendon friction losses, but are limited by finger thickness.
- **Decision:** Use the largest pulley radius the envelope allows (practical maximum expected around 5 to 6 mm) and put the rest of the ratio in the motor and gearing.
- **Consequences:** Spool rotation of roughly 230 to 290 degrees rules out standard 180-degree hobby servos. A continuous-rotation servo or a geared DC motor with an encoder is needed.
- **Revisit:** Test two pulley sizes on the Phase 1 rig and measure tension vs. fingertip force.

## D-007: Actuator torque requirement is a range, not a single value
- **Date:** 2026-10-17
- **Status:** Accepted
- **Context:** The initial estimate used a 60 mm lever arm and gave about 0.7 N.m at the motor. Using the measured 93 mm finger length for a fingertip-only contact gives about 1.3 N.m. A wrap grasp (controller) sits near the lower end and a tip pinch near the upper end. The 50% efficiency figure is a guess until measured.
- **Decision:** Treat 0.7 to 1.3 N.m as the planning range and resolve the actuator choice in Phase 2 using measured efficiency.
- **Options if too demanding:** lower the safety factor, let the palm and thumb carry part of the load, or use a smaller spool with a higher gear ratio.

## D-008: Requirements-first workflow in a Git repo
- **Date:** 2026-10-17
- **Status:** Accepted
- **Context:** Requirements, calculations, and decisions are the most valuable artifacts and are easy to lose if kept only in chat.
- **Decision:** Keep `docs/requirements.md` and `docs/decisions.md` in the repo from the start, with calculation scripts in `docs/calcs/`. Tag milestones, track Phase tasks as GitHub Issues, and add folders only when each phase needs them.
- **Consequences:** Every requirement carries a verification method, and every assumption is tracked until validated.

## D-009: Finger master sketch conventions
- **Date:** 2026-10-18
- **Status:** Accepted
- **Context:** All links, the palm, and the thumb must share one coordinate convention so that mates and joint-angle math stay consistent. The first sketch was drawn on the Top Plane, where the pin axis would have been Y.
- **Decision:** The finger master sketch (`Finger_Skeleton`) lives on the **Front Plane**. The origin is the center of the base (MCP) joint, the finger extends along +Y, the pin axis is Z, and +X is the palm side (tendon side). Joint centers are at y = 0, 45, and 70 mm, with the fingertip at 93 mm. A fully defined construction circle of diameter 10 mm sits at each joint.
- **Consequences:** Each circle serves two purposes: it is the rounded knuckle end of the link around the pin, and it is the tendon moment arm (radius 5 mm, so tau = T * 5 mm). This fixes the baseline pulley radius at 5 mm, consistent with the hypothesis in D-006. Later links start from a copy of this skeleton file.
- **Revisit if:** The rig data in Phase 1 shows a different pulley radius is needed.

## D-010: Link 1 body envelope (stadium, 15 x 17 mm section)
- **Date:** 2026-10-18
- **Status:** Accepted (envelope), print orientation is a hypothesis
- **Context:** Link lengths (45, 25, 23 mm) are short compared with a 15 mm body depth, so every joint end needs to rotate without hitting its neighbour. Semicircular ends concentric with each pin avoid that interference. Body depth also has to leave wall material around the tendon channel at r = 5 mm.
- **Decision:** Link 1 is a stadium profile on the Front Plane with end radius 7.5 mm centered on the joint centers (15 mm depth in X), extruded 17 mm in Z about the mid plane. Measured result: 60 x 15 x 17 mm. Each link is its own part file, created with Save As copy from the skeleton. Joint details (clevis ears, tongue, clearances, tendon channel) are added in the next step and are not decided here.
- **Consequences:** The wall between the pulley surface (r = 5 mm) and the palm face (7.5 mm) is only 2.5 mm before the tendon channel is cut, so the channel wall thickness must be checked in the next step. The link fits easily within the 180 mm print bed.
- **Hypothesis:** Print the link flat with the pin axis vertical, so tendon loads act in the plane of the layers and the pin holes print as round vertical bores. Confirm with a test print.
