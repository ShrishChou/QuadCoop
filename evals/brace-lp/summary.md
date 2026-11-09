# Brace posture search: evals/brace-lp

Static LP, no simulation: the largest push the front bumper can hold with the feet planted, joint torques within the limit (80 Nm x margin), feet inside their friction cone (min 10 N each). Robot 45.0 kg (weight 441 N). 5463 reachable postures on the grid (base height 0.38-0.56 m, pitch -10..10 deg, front feet -0.15..+0.15 m, hind feet -0.30..+0.10 m fore-aft from nominal, stance +0/5/10 cm wider each side). 'slides' = heaviest object of friction 0.45 this push slides: F (cos a + mu_o sin a) / (mu_o g).

## Ceiling by foot friction (push level, a = 0)

| foot mu | friction bound mu m g (N) | nominal stance, 4 feet, full torque (N) | best brace, full torque (N) | best brace, 80% torque (N) | best, front foot lifted (N) | best, hind foot lifted (N) |
|---|---|---|---|---|---|---|
| 0.6 | 265 | 244 | 244 | 244 | 244 | 244 |
| 0.8 | 353 | 326 | 326 | 326 | 326 | 251 |
| 1.0 | 441 | 364 | 408 | 408 | 408 | 251 |

## Torque headroom: smallest peak joint torque that holds 250 N (foot mu 0.8, a = 0)

5450 of 5463 postures can hold it at all.

| posture | height (m) | pitch (deg) | front feet dx (m) | hind feet dx (m) | wider (m) | peak torque (Nm) | % of 80 Nm |
|---|---|---|---|---|---|---|---|
| nominal | 0.53 | 0.0 | +0.0 | -0.0 | 0.0 | 27 | 34% |
| #1 | 0.56 | -10.0 | -0.15 | -0.3 | 0.0 | 9 | 11% |
| #2 | 0.56 | -10.0 | -0.15 | -0.25 | 0.05 | 9 | 12% |
| #3 | 0.56 | -10.0 | -0.1 | -0.25 | 0.05 | 10 | 12% |
| #4 | 0.56 | -10.0 | -0.05 | -0.25 | 0.05 | 10 | 12% |
| #5 | 0.56 | -10.0 | -0.1 | -0.3 | 0.0 | 11 | 14% |
| #6 | 0.53 | -10.0 | -0.15 | -0.3 | 0.05 | 11 | 14% |
| #7 | 0.56 | -5.0 | -0.15 | -0.2 | 0.05 | 11 | 14% |
| #8 | 0.56 | -5.0 | -0.15 | -0.25 | 0.0 | 12 | 14% |
| worst feasible | 0.56 | 5.0 | +0.05 | +0.1 | 0.1 | 65 | 81% |

## Upward push component (best brace, full torque): push N / heaviest object it slides (kg)

| foot mu | a = 0 deg | a = 10 deg | a = 20 deg |
|---|---|---|---|
| 0.6 | 244 N / 55 kg | 275 N / 66 kg | 326 N / 81 kg |
| 0.8 | 326 N / 74 kg | 381 N / 92 kg | 475 N / 118 kg |
| 1.0 | 408 N / 92 kg | 494 N / 119 kg | 653 N / 162 kg |

## What matters: smallest peak torque (Nm) holding 250 N with one variable fixed, the rest free (lower = more headroom)

- **h**: 0.38: 21, 0.41: 21, 0.44: 19, 0.47: 17, 0.5: 14, 0.53: 11, 0.56: 9
- **pitch_deg**: -10: 9, -5: 11, 0: 15, 5: 19, 10: 22
- **dx_front**: -0.15: 9, -0.1: 10, -0.05: 10, 0: 13, 0.05: 13, 0.1: 14, 0.15: 14
- **dx_hind**: -0.3: 9, -0.25: 9, -0.2: 11, -0.15: 14, -0.1: 16, -0.05: 19, -0: 21, 0.05: 22, 0.1: 24
- **dwidth**: 0: 9, 0.05: 9, 0.1: 12

## Posture handed to the sim check (most headroom at 250 N)

height 0.56 m, pitch -10.0 deg, front feet -0.15 m, hind feet -0.3 m, 0.0 m wider; static ceiling 326 N at foot mu 0.8. At 250 N: foot normal forces (N) LF/RF/LH/RH 75, 75, 146, 146, peak joint torque 9 Nm.
