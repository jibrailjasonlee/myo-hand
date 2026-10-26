# Bill of materials

Prices are my estimates in CAD, shipping not included, and probably off by 30% either way. The only prices I checked against a source: MyoWare 2.0 is US$44.95 on Adafruit (listing says no longer stocked). Check Creatron, RobotShop, Canada Robotix, Amazon.ca before buying anything. Cap is $200 all-in (D-014).

## Stage 1: three-link finger, buy now

| Item | Qty | Use | Est. |
|---|---|---|---|
| Braided PE fishing line, 0.25 to 0.3 mm | 1 spool | cord | $10 |
| Beading elastic, about 0.7 mm | 1 | return spring | $4 |
| 1.75 mm filament offcuts | 3 per finger | pins | $0 |

Stage total: about $15.

## Stage 2: actuation and control, after the cord test

| Item | Use | Est. |
|---|---|---|
| 12 V 37 mm gearmotor with encoder | finger motor | $20 to 35 |
| Motor driver (TB6612FNG or DRV8871) | drives it | $5 to 10 |
| ESP32 dev board | controller | $10 to 15 |
| INA219 current sensor (optional) | grip detection | $4 to 8 |
| M3 screws, nuts, heat-set inserts | assembly | $15 to 20 |
| Breadboard, wire, connectors | wiring | $10 to 15 |
| Micro servo | thumb posture, later | $5 to 8 |

Stage total: about $70 to 110.

Don't pick the motor yet. The JGB37-520 110 rpm is rated 3.9 kg·cm with a 2.4 A stall at 12 V, which is under the 0.5 to 0.75 Nm estimate for a 6 mm spool. A smaller spool lowers the torque needed. The cord test gives the real tension.

## Stage 3: EMG, power, extras

| Item | Est. |
|---|---|
| EMG front end built from an instrumentation amp and op-amps, plus electrodes | $25 to 35 |
| 3S LiPo and charger (bench supply until then, kept away from the EMG) | $30 to 45 |
| TPU spool for chip pads | $15 to 25 |

Stage total: about $70 to 105.

## Against the cap

Low end of all three stages is about $155, high end about $230. $200 works if the EMG front end is built, not bought (MyoWare plus electrodes is $70 or more by itself), there's no custom PCB, and parts come from the robotics association's stock where possible.
