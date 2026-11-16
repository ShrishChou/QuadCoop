# Presentation videos

A curated set of evaluation clips, copied from `logs/evals/` and `evals/spot_arm/`. Those folders are git-ignored and hold
about 1,700 clips (6.4 GB). Each file name is `<system>__<original clip name>`; the original name ends in the
episode's outcome (`success`, `horizon` = time ran out, `fell_<robot>`). Captions are burned into the videos.

Results quoted below come from the evaluation summaries listed under each folder.

## 00_wiring
- `spotarm_pair__arms.mp4`: the two Spot-arm robots on RAI's walker; the arm wiring check.

## 01_armless_anymal_pair: ANYmal + ANYmal on the 480-task benchmark (presentation set)
Tasks: object at the origin, both robots behind it. `A_straight` = goal 3 m ahead; `D_far_turn` = 5 m ahead, turned 90°.
Mass in the name. Horizon 80 s; success = within 10 cm and 6° for 1 s.

| system prefix | what it is | benchmark success (480 tasks) | source |
|---|---|---|---|
| `anymal_alone` | one ANYmal, the partner parked far away | 52.4% | `logs/evals/pres-solo-anymal` |
| `frozen_pair` | two single-robot policies run side by side, untrained together | 46.2% | `logs/evals/pres-frozen-pair` |
| `ippo_trained` | trained together, IPPO | 65.6% (ten-object checkpoint) | `logs/evals/pres-ippo-it4000` |
| `mappo_trained` | trained together, MAPPO | 64.6% (ten-object checkpoint) | `logs/evals/pres-mappo-B-it5000` |
| `contact_planner` | contact planner + executor | – | `logs/evals/pres-planner-expert` |
| `spot_alone` | one Spot (older evaluation, 60 kg) | 40.7% | `logs/evals/solo-spot` |

The success column gives the ten-object benchmark numbers (`evals/team-*`, `evals/ten-*`). The clips come from the
presentation-set evaluations named in the last column; their checkpoints may differ slightly from those benchmark
checkpoints. Best comparison: `long_80kg_A_straight` (the frozen pair and the solo ANYmal time out; trained MAPPO
succeeds) and `long_40kg_D_far_turn`.

## 02_spot_arm_transport_60deg: two Spots with arms, 1 m transport, 20 kg long object, goal heading 0 / ±60°
Clip name: `<turn>_<mode>`. Modes:
- `both`: as trained;
- `none`: both arms locked stowed;
- `solo_1` / `solo_2`: only robot 1 / 2 acts, the other is parked 40 m away;
- `stowed`: a policy trained with the arms stowed.

| system prefix | as trained | both arms locked | robot 1 alone | robot 2 alone | source |
|---|---|---|---|---|---|
| `mappo_jointarms` (MAPPO, arms on joint targets) | 99.2% | 99.2% | 0% | 0% | `evals/sa-team-sa_mappo_learned60_s0/summary.md` |
| `mappo_stowed` (MAPPO, arms stowed) | 81.7% | – | 0% | 0% | `evals/sa-team-sa_mappo_stowed60_s0/summary.md` |

120 tasks per mode. The arms touch the object under 1% of the time. Transport needs both robots, but not the arms.

## 02b_spot_arm_transport_30deg: the same task at ±30°, IPPO
| system prefix | as trained | both arms locked | either robot alone | source |
|---|---|---|---|---|
| `ippo_jointarms` | 100% | 98.3% | 0% | `evals/sa-team30-sa_ippo_learned_s0/summary.md` |
| `ippo_stowed` | 90.0% | – | 0% | `evals/sa-team30-sa_ippo_stowed_s0/summary.md` |

## 03_hand_reach_preflight: the hand-position interface works
Each Spot alone, partner parked. It reaches its hand left, right or keeps it stowed, then walks into the object at 0.5 m/s.
- Reaching left turns the object clockwise (−15.5° / −25.9°), reaching right counter-clockwise (+34.6° / +31.0°).
- With the arm stowed it turns only +4.5° / +7.1°.

Source: `evals/spot_arm/hand_reach_vx0.5/`.

## 04_turn_in_place: 20 kg long object, centre held at the goal, turn clockwise (`cw`) or counter-clockwise (`ccw`)
One robot behind the object and one in front; they push opposite ends, which turns it about its centre.

| system prefix | what it is | success |
|---|---|---|
| `scripted_40deg__both_hands_*` | scripted maneuver, both hands, ±40° | 78% (one hand 47–59%, either robot alone 0%) |
| `scripted_40deg__stowed_*` | scripted maneuver, trunk pushing, ±40° | 25% |
| `scripted_60deg__*` | the same at ±60° | both hands 34%, stowed 0% |
| `cloned_policy_40deg__*` | behaviour clone of the script, before PPO | 11/16 with both hands, 0/16 with either hand locked |

Source: `evals/spot_arm/turn_inplace_40/`, `turn_inplace_60/`, `turnwire_bc_model0/`.

## Still to come (added after their evaluations finish, before the Nov 17 maintenance)
- Turn in place, learned:
  - T1 stowed, T2 hands with PPO alone, T3 hands from demonstrations;
  - `logs/evals/sa-turn-sa_turn_{stowed,hand,bc}_s0/`.
- Hardware comparison on the standard evaluator (long object, 20 and 40 kg):
  - Spot-arm pair: arms active, arms locked, alone;
  - armless Spot pair;
  - ANYmal + Spot;
  - `logs/evals/cmp-*/`.
- IPPO / MAPPO × stowed / joint arms, seeds 0–1: `logs/evals/sa-team-sa_{ippo,mappo}_{stowed,learned}60_s*/`.
