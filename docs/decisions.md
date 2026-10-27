# Decisions

Running log, newest at the bottom. If I change my mind I add a new entry instead of rewriting the old one. "Untested" means it's a bet I still have to check.

## D-001: Underactuated hand for assistive use (2026-10-17)

I wanted a personal project with a real problem behind it, not tied to either rover team. A reaction-wheel pendulum read as a controls exercise more than robotics, and rover state estimation was tied to a team. A low-cost tendon-driven hand aimed at assistive use fits better. It leans on mechanism design, force control, EMG processing and embedded code. It stays a research prototype. If the $80 cap or the timeline falls apart, this gets revisited.

## D-002: Two motors, one EMG channel (2026-10-17)

One motor closes all four fingers through an underactuated differential. A second motor switches the thumb between power and pinch. Control comes from one EMG channel. Individual fingers, wrist rotation and feedback are real research topics but too much for one term. A second EMG channel would allow pattern recognition for grip selection, which is a possible extension later.

## D-003: The chip is a stretch goal (2026-10-17)

The chip needs about 0.04 N to hold and the controller needs about 5.8 N per side. That 50:1 spread is the hardest thing in the project. Motor current is probably useless as a force estimate at the low end, since friction is about the same size as a 0.1 N fingertip force. Soft, low-stiffness pads might give usable force from position alone (F = k * dx), with no sensor.

So the cube, controller, aperture and cost stay as must-haves, and the chip requirements (R4, R5) are stretch. The thumb pinch posture and soft pads get designed in from the start because they're cheap to include. Go or no-go comes after the single-finger rig measures force vs. position on a TPU pad.

## D-004: Baseline finger is pins, tendon, elastic (2026-10-17)

Three pin joints per finger (2 mm steel pin, or an M2 screw with a nylock nut). A tendon on the palm side closes the finger and an elastic cord on the back opens it. Links are 45, 25 and 23 mm and 17 mm wide, taken from my own finger and palm.

The closing order is set by k/r at each joint, meaning return spring stiffness over pulley radius. That's what to sweep in a script before building anything. A flexure (TPU) finger is the obvious alternative, and I'll compare against it once the rig exists.

## D-005: Close proximal joint first (untested)

Proximal, then middle, then distal, which is the usual wrap. The worry is that a proximal-first finger can shove a light object like the cube away before the tip gets there. I'll sweep k/r in Python before building.

## D-006: Big pulleys, rest of the ratio in the motor (untested)

Pulley radius is just a gear ratio. A smaller radius means less tendon travel and more tension: 5 mm gives about 28 N and about 290 deg of spool rotation, 4 mm gives about 34.9 N and about 233 deg. Tension times travel stays constant.

Big pulleys add no parts and no backlash, and they cut tendon friction, so I'm going as large as the finger allows (my guess is 5 to 6 mm) and putting the rest of the ratio in the motor gearing. Spool rotation of 230 to 290 deg rules out a standard 180 deg hobby servo. It needs a continuous-rotation servo or a geared DC motor with an encoder. I'll test two pulley sizes on the rig.

Update 2026-10-24: there are no pulleys after all, see D-012. Cord travel is now about 61 mm, so the 180 deg servo is still out.

## D-007: Torque is a range, not a number (2026-10-17)

The first estimate was about 0.7 Nm at the motor, using a 60 mm lever arm. With my real 93 mm finger and a fingertip-only contact it comes out near 1.3 Nm. Wrap grasps like the controller sit near the low end and a tip pinch sits near the high end. The 50% efficiency figure is a guess. I'm planning around 0.7 to 1.3 Nm and picking the actuator in Phase 2, after I've measured real efficiency. If that's too much: drop the safety factor, let the palm and thumb carry part of the load, or use a smaller spool with a higher gear ratio.

Update 2026-10-24: with the guide layout in D-012 the range drops to about 0.5 to 0.75 Nm at a 6 mm spool.

## D-008: Requirements and decisions live in git from the start (2026-10-17)

Both docs sit in docs/. Calc scripts will go in docs/calcs/ once there are some. Milestones get tagged, phase tasks go in GitHub issues, and folders only get added when a phase needs them.

## D-009: Finger sketch conventions (2026-10-18)

The master sketch is on the Front Plane. Origin is the center of the base joint, the finger runs along +Y, the pin axis is Z, and +X is the palm (tendon) side. Joints sit at y = 0, 45 and 70 mm, with the tip at 93 mm. I first drew it on the Top Plane, which would have put the pin axis on Y, so I moved it.

There's a 10 mm diameter construction circle at each joint, and it does two jobs: it's the rounded knuckle end of the link around the pin, and it's the tendon moment arm (5 mm radius, so torque = T * 5 mm). That fixes the baseline pulley radius at 5 mm, in line with D-006. Later links start as copies of this skeleton file.

Update 2026-10-24: the circles are a layout reference only. They aren't a pulley, see D-012.

## D-010: Link 1 body (2026-10-18)

A stadium profile with 7.5 mm end radii centered on the joints (15 mm deep in X), extruded 17 mm in Z about the mid plane. It comes out 60 x 15 x 17 mm. Round ends concentric with the pins let neighbouring links rotate without hitting each other, which matters because the links are short next to a 15 mm depth. Each link is its own file, made with Save As copy from the skeleton.

Not decided yet: clevis, tongue, clearances and the tendon channel. Watch the wall between the pulley surface (5 mm radius) and the palm face (7.5 mm). That's only 2.5 mm before the channel is cut.

Untested: printing it flat with the pin axis vertical, so tendon load acts in the layer plane and the pin holes come out round.

Update 2026-10-25: that orientation stops working once the slot is cut. With the pin axis vertical the slot becomes a horizontal gap and the top ear hangs over it, so it needs supports, and the slot width would depend on support quality instead of XY accuracy. Print it on its flat back face (x = -7.5) with the guide blocks pointing up. Slot and tongue widths then come from XY accuracy, no supports are needed, and the pin holes lie on their side, so expect them to print a bit small and oval. The lower quarter of each rounded end will come out rough.

## D-011: Link 1 tongue, slot and pin holes (2026-10-24)

Tongue on the proximal end: 7.0 mm wide, shoulder 8 mm past the pin. Slot on the distal end: 7.6 mm wide, bottom 8 mm behind the pin, open at the end. That leaves 4.7 mm ears (4.7 + 7.6 + 4.7 = 17). The next link's 7.0 mm tongue sits in the slot with 0.3 mm per side, and the 8 mm slot depth and shoulder offset both clear the 7.5 mm rounded end by 0.5 mm.

Pin holes: 2.2 mm through the tongue so it spins freely, 2.0 mm through the ears so the pin stays put. A 2 mm dowel about 16 mm long fits the 17 mm width. Printed holes tend to come out small, so none of these clearances are trusted until a test print.

Built and measured in Link1_Proximal: 7.0, 7.6, 4.7 and 8 mm all match.

Rev A printed in PLA, back face down (2026-10-25). Ruler measurements match the CAD, though a ruler can't confirm the 0.3 mm clearance. Both pin holes printed small. A wooden toothpick (about 2 mm, not a precise gauge) is a firm fit in the tongue hole and won't go through the ear holes easily. Flexion stops a little past 90 deg, with the shoulders and the guide blocks touching at about the same angle. Extension goes about 90 deg past straight before the back of the tongue stops it, so the finger needs a hard stop at straight. The cord test is skipped for now (no thread at home). Rev B will probably open the tongue hole to about 2.4 mm and the ear holes to about 2.1 to 2.2 mm, once the sanded-pin fit is known.

## D-012: Cord rides on the palm face, in guides (2026-10-24)

The 10 mm circles aren't a pulley, and the first two fixes I tried on paper don't work.

A tunnel 5 mm off the axis can't cross the slot: both mouths end up past the pin, so bending the joint lengthens the cord instead of shortening it. docs/calcs/tendon_path.py shows it. The cord taken up goes negative past 15 deg (minus 8.6 mm at 90 deg) and the arm flips sign, so the cord would fight the bend.

A groove concentric with the joint (my first fix) fails for a different reason. When the finger curls toward the palm, the palm-side cord is on the inside of the bend. It can't wrap a pin-centred surface there, it takes a straight shortcut between guides. That one is reasoning only, it isn't in the script.

What works is a straight cord between small guides on the palm face, one either side of each joint, like a bowstring across the inside of the bend. The guide holes sit 9 mm off the axis (1.2 mm hole in a 3 mm block on the 7.5 mm palm face). Guides at y = 12 and y = 33 on link 1, y = 57.5 on link 2, and the cord anchored near the tip at y = 89. The arm is 9 mm in a straight finger and grows to about 15 mm by 90 deg of bend.

From the script: about 61 mm of cord to take up with all three joints closed (90 / 100 / 80 deg), and 15.5 N per finger for 1.5 N at the tip with the finger straight, which is worse than real use. Spacing the guides 12 mm either side keeps the arm positive past 100 deg. Closer guides would cut the range.

Untested: friction through the guides, whether the cord pinches between the links at full bend, and whether the small blocks print cleanly. The single-finger rig will measure the real arm. Collisions between the link ends at full bend get checked in CAD with a motion study.

## D-013: Link 2 (2026-10-26)

Link 1 with the pins 25 mm apart: 40 mm long, same 15 x 17 section. Tongue and slot are the same as link 1, with the slot bottom at y = 17. One guide block at y = 11.5 to 13.5 sits 12.5 mm from each pin, so it serves the PIP and the DIP joint both. Hole sizes are the same as rev A (2.2 tongue, 2.0 ears, 1.2 guide) so they can all change together once the real pin is chosen.

Checked in the STEP file: extents, tongue, slot, shoulder, block and hole positions and sizes all match. Not printed yet.

## D-014: Cost cap raised to $200 CAD (2026-10-26)

The $80 cap didn't survive a real parts list. The finger, motor, driver, ESP32 and fasteners alone come to roughly $85 to $125, and EMG plus a battery add another $85 to $150 on top. Estimates are in docs/bom.md, with only the MyoWare price and one gearmotor's specs checked against a source.

New cap is $200 CAD all-in with shipping. That's tight, not comfortable. It holds if the EMG front end is built from an instrumentation amp instead of bought as a MyoWare, a bench supply covers power until late, and there's no custom PCB. If receipts pass $200 I'll log it here instead of quietly moving the number again.

## D-015: Link 3 (2026-10-26)

The fingertip. Same tongue as links 1 and 2, no slot. Stadium with its centers 15.5 mm apart, so the tip is 23 mm past the pin and the whole part is 30.5 mm long. One cord anchor block at y = 14 to 16 with a 1.2 mm hole at x = 9, same height off the axis as the guides.

Checked in the STEP file: extents, tongue, shoulder, anchor block and hole positions all match. Not printed yet.

The anchor is 15 mm past the DIP pin, where tendon_path.py had it at 19. Total cord to take up goes from 61 mm to 60 mm, which doesn't matter yet. The script is updated to match.

## D-016: Extension stop on the ears (2026-10-26)

Rev A joints bend about 94 deg both ways. Flexion is fine, but extension has to stop at straight: the elastic on the back pulls the finger open, and with nothing in the way it would keep going backwards.

docs/calcs/joint_range.py models one joint in 2D from the link dimensions. It gives 94.5 deg of flexion and 94 deg of extension, which matches the hand test (a little past 90 flexion, about 90 extension). The slot bottom is what stops both: the limit works out to 2 * atan(slot depth / 7.5), so 93.6 deg for an 8 mm slot.

Fix: a block on the back half of each pair of ears, x = -7.5 to -2, running from the pin to 7.8 mm past it. The next link's shoulder sits 8 mm past the pin, so it hits the block after 2.5 deg of extension, and the 0.2 mm gap is the play. In the model flexion doesn't change. The block has to go in before the slot cut in the feature tree so the cut trims it and the slot stays clear for the tongue. It goes on the distal ears of links 1 and 2 (rev B), and in the palm clevis later. Back-face-down printing is unchanged, since the block's back face is the same plane as the link's.

PIP wanted 100 deg and this doesn't get there. The slot corner limits at 94.5 and the guide blocks touch at 96. Reaching 100 or more would take a 10 mm slot, a 10 mm shoulder and shorter guides, for a few degrees. Not doing that. If the cord test says the middle joint needs more, I'll revisit.

Untested: it's a 2D model, and the printed stop hasn't been tried.

## D-017: Closing order comes from elastic preload (2026-10-27)

docs/calcs/closing_order.py balances cord torque against the back elastic at each joint. With the same elastic on all three joints, they start closing at nearly the same cord tension (0.61 to 0.63 N to reach 30 deg), so the order is undefined and guide friction would decide it. With the preload graded 0.2 / 0.3 / 0.45 N the knuckle goes first, but only by 0.05 to 0.1 N. A preload of 0.1 / 0.3 / 0.8 N widens that. The cord geometry barely helps, since the guides give nearly the same arm at every joint.

So D-005 (proximal first) gets set with the elastic, not the guides: the knuckle gets the lightest elastic and the tip the heaviest. The model has no friction and the stiffness (0.3 N/mm) is a guess. The cord test should measure the elastic's real stiffness and preload. Free-air order only matters for pushing the cube away. Once the finger touches something, contact forces decide the rest.
