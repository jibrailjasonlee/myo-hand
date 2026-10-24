# myo-hand

A cheap tendon-driven hand with a prosthetic-style EMG interface. One motor closes all four fingers through an underactuated differential, a second motor flips the thumb between power and pinch, and a single forearm EMG channel handles open/close. The target is under $80 CAD, and every printed part fits on a Bambu A1 Mini.

It's a research prototype, not a medical device, and nobody is going to wear it.

Grasp targets: a MoYu WeiLong V10 cube, an Xbox controller, and (stretch) a potato chip that doesn't snap.

## Status

Early. The finger skeleton and the first link body (60 x 15 x 17 mm) are modelled. Joint details and the tendon channel are next. Nothing is printed, wired or programmed yet.

## What's here

    cad/                    SolidWorks parts, with a STEP export next to them where I've made one
    docs/requirements.md    what it has to do, the numbers behind that, how each requirement gets checked
    docs/decisions.md       design decisions, newest at the bottom

You need SolidWorks for the .SLDPRT files. The STEP files open in anything.

There's nothing to build or run yet. Firmware will get its own folder, and build steps will go here when it does.

## Known problems

The force and torque numbers are hand estimates. The friction coefficient (0.5), the 50% tendon efficiency and the joint ranges are all guesses until I build a single-finger test rig.

By my rough math the motor needs 0.7 to 1.3 Nm at its output. That's well past a typical N20 gearmotor and close to the limit of a metal-gear hobby servo, so the transmission may change.

The potato chip may get dropped. If friction in the tendon makes low-force control too erratic, it's out and the data says why.
