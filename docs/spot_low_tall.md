# Spot-arm on low and tall objects at light masses: coordination and arm use

Status (2026-11-19): code done; queued after the Spot pipeline (`slurm/submit_spot_lowtall.sh`): config check 29612192,
solo 29612193 (after the check and after the pipeline's IPPO run 29611756), shared start 29612194, MAPPO 29612195,
IPPO 29612196.

**Question.** At masses one robot can handle, which pushing behaviours does a Spot with an arm learn alone and with a
partner, when the objects make body-height pushing a poor choice? The objects are low (below the chest) or tall (tip
when pushed at the chest), and short episodes pay.

## Objects (`QUADCOOP_SHAPE_SET=spot20`, `stage2/shapes.py`)

The twelve existing shapes (indices unchanged, the beam included) plus eight. Heights are nominal; widths and lengths
are randomised 0.8-1.2x as for the others.

| object | size (m) | why |
|---|---|---|
| low_slab | 0.90 x 0.90 x 0.18 | below the chest: the body's front meets it poorly, the hand reaches it |
| low_bar | 0.24 x 1.60 x 0.16 | long and low: steering needs two contacts far apart |
| low_plus | arms 1.2, 0.24 wide, 0.18 tall | low with corners |
| low_roller | lying cylinder, r 0.12, 1.2 long | rolls, low |
| tall_box | 0.50 x 0.50 x 1.10 | borderline: tips only with dynamics |
| tall_column | 0.30 x 0.30 x 1.10 | tips when pushed at body height |
| tall_wall | 0.20 x 1.00 x 1.00 | tips when pushed broadside at body height; stable pushed end-on |
| top_heavy | 0.24 base (0.75 tall) + 0.70 x 0.70 x 0.35 top, 65% of the mass on top | very narrow footprint, high centre of mass |

**When a push tips a tall object (quasi-static).** A robot pushing at height h on an object sliding with friction mu
tips it about the leading bottom edge when mu x h > a, where a is half the base width along the push. The height of
the centre of mass does not enter until the object accelerates; then it does, because the inertial load acts there.
With mu 0.4-0.6 and a chest-height push (h about 0.45 m):
- the column (a = 0.15) tips;
- the wall pushed broadside (a = 0.10) tips;
- top_heavy (a = 0.12) tips;
- the 0.5 m box is at the edge.

So pushing *higher* (for example with the arm at the top) tips them sooner. What keeps them up is:
- pushing *lower* (the hand can reach down to about 0.1-0.3 m);
- pushing end-on (the wall);
- or a partner bracing near the top on the far side while the other pushes low: a coordination behaviour the pair
  can discover.

The low objects are where reaching with the arm matters most.

Caveats:
- tipping ends the episode (`box_tipped`), a failure;
- the top map slices at 0.12-0.75 m, so it shows the low objects (all at least 0.16 m tall) and only the base of
  top_heavy;
- the front view covers 0-1.2 m, so the 1.1 m objects fit.

## Training

Same walker (`push_ft_s3_handload`), inputs and recipe as `sp_solo_s0` / `sp_pair_*` (`docs/spot_arm_pair.md`): arm
learned with hand inputs, partner map, r7. Changes:
- **masses:** 5-25 kg at every level, identical for one robot and for pairs;
- **reward:** `--time-cost 0.5` per second (team) on top of r7, whose success bonus already shrinks with time;
- **objects:** the 20 above;
- **levels:** distance 1-1.5 / 1.5-2.5 / 2-3.5 m, same mix schedule.

Runs, each after the previous, 6000 iterations:
1. `sp20_solo_s0`: IPPO, partner parked, from scratch;
2. its actor copied to both robots;
3. `sp20_pair_mappo_s0`;
4. `sp20_pair_ippo_s0`.

## What to look at

- success and time to success by object, one robot against two (same masses);
- arm contact share and hand contact height by object (low and tall against the rest);
- tips per object;
- for pairs: both pushing at once, role splits (one pushes, one braces or steers), and whether MAPPO and IPPO differ;
- videos of the tall objects (bracing) and the low bar (two-point steering).

Not yet queued: evaluations, a spot20 task bank, videos.
