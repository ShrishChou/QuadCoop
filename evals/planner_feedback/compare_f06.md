16 matched tasks per arm; arms {'A': 'fbA-f06', 'B': 'fbB-f06'}

| group | arm | n | success | pos_err | yaw_err | yaw_unint | fell | time | settled | share_req | share_deliv | share_err | v_err | w_err | duty_both | duty_each | switches | share_corr | v_corr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | A | 16 | 0.000 | 0.801 | 8.281 | 6.046 | 0.312 | 20.000 | 0.000 | 0.497 | 0.421 | 0.166 | 0.265 | 7.368 | 0.570 | 0.743 | 0.688 | 0.000 | 0.000 |
| all | B | 16 | 0.000 | 0.706 | 8.344 | 8.660 | 0.125 | 20.000 | 0.000 | 0.518 | 0.457 | 0.204 | 0.262 | 7.567 | 0.522 | 0.711 | 0.812 | 0.000 | 0.014 |
| 60 kg | A | 16 | 0.000 | 0.801 | 8.281 | 6.046 | 0.312 | 20.000 | 0.000 | 0.497 | 0.421 | 0.166 | 0.265 | 7.368 | 0.570 | 0.743 | 0.688 | 0.000 | 0.000 |
| 60 kg | B | 16 | 0.000 | 0.706 | 8.344 | 8.660 | 0.125 | 20.000 | 0.000 | 0.518 | 0.457 | 0.204 | 0.262 | 7.567 | 0.522 | 0.711 | 0.812 | 0.000 | 0.014 |
| S_moveturn | A | 8 | 0.000 | 0.906 | 12.250 | nan | 0.250 | 20.000 | 0.000 | 0.497 | 0.391 | 0.177 | 0.274 | 11.773 | 0.534 | 0.707 | 1.250 | 0.000 | 0.000 |
| S_moveturn | B | 8 | 0.000 | 0.787 | 9.512 | nan | 0.250 | 20.000 | 0.000 | 0.516 | 0.498 | 0.182 | 0.270 | 11.147 | 0.474 | 0.665 | 1.000 | 0.000 | 0.012 |
| S_straight | A | 8 | 0.000 | 0.697 | 4.312 | 6.046 | 0.375 | 20.000 | 0.000 | 0.497 | 0.452 | 0.155 | 0.255 | 2.963 | 0.606 | 0.778 | 0.125 | 0.000 | 0.000 |
| S_straight | B | 8 | 0.000 | 0.625 | 7.175 | 8.660 | 0.000 | 20.000 | 0.000 | 0.521 | 0.417 | 0.225 | 0.253 | 3.987 | 0.571 | 0.757 | 0.625 | 0.000 | 0.016 |

Paired differences vs A (mean [95% CI]): success / fell in points, errors in m and deg, time in s
| group | arm | success | fell | pos_err | yaw_err | yaw_unint | time | share_err | v_err | w_err | duty_both | switches |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | B | +0.00 [+0.00, +0.00] | -18.75 [-43.75, +6.25] | -0.10 [-0.24, +0.04] | +0.06 [-4.61, +4.10] | +2.61 [+0.11, +5.74] | +0.00 [+0.00, +0.00] | +0.04 [-0.02, +0.08] | -0.00 [-0.01, +0.00] | +0.20 [-1.24, +1.60] | -4.73 [-11.39, +1.94] | +0.12 [-0.38, +0.62] |
| 60 kg | B | +0.00 [+0.00, +0.00] | -18.75 [-43.75, +6.25] | -0.10 [-0.24, +0.04] | +0.06 [-4.61, +4.10] | +2.61 [+0.11, +5.74] | +0.00 [+0.00, +0.00] | +0.04 [-0.02, +0.08] | -0.00 [-0.01, +0.00] | +0.20 [-1.24, +1.60] | -4.73 [-11.39, +1.94] | +0.12 [-0.38, +0.62] |
| S_moveturn | B | +0.00 [+0.00, +0.00] | +0.00 [-37.50, +37.50] | -0.12 [-0.40, +0.14] | -2.74 [-10.95, +5.17] | +nan [+nan, +nan] | +0.00 [+0.00, +0.00] | +0.01 [-0.08, +0.08] | -0.00 [-0.02, +0.01] | -0.63 [-3.25, +2.08] | -5.98 [-14.37, +4.43] | -0.25 [-1.00, +0.50] |
| S_straight | B | +0.00 [+0.00, +0.00] | -37.50 [-75.00, -12.50] | -0.07 [-0.18, +0.02] | +2.86 [+0.49, +5.85] | +2.61 [+0.11, +5.74] | +0.00 [+0.00, +0.00] | +0.07 [+0.03, +0.12] | -0.00 [-0.01, +0.01] | +1.02 [+0.18, +2.25] | -3.49 [-12.48, +2.63] | +0.50 [+0.00, +1.25] |

B vs A: gained 0, lost 0

Per task: outcome, final pos err m / heading err deg, switches: A | B
  S_moveturn 60 kg rep 0: fell_anymal1 1.07/14 sw 4 | horizon 0.54/1 sw 2
  S_moveturn 60 kg rep 1: horizon 0.57/5 sw 2 | fell_anymal1 0.85/12 sw 2
  S_moveturn 60 kg rep 2: horizon 0.78/8 sw 0 | horizon 0.69/1 sw 2
  S_moveturn 60 kg rep 3: horizon 0.70/2 sw 2 | horizon 0.66/6 sw 2
  S_moveturn 60 kg rep 4: horizon 1.31/29 sw 0 | horizon 0.64/8 sw 0
  S_moveturn 60 kg rep 5: horizon 0.57/1 sw 2 | horizon 0.74/11 sw 0
  S_moveturn 60 kg rep 6: horizon 1.28/22 sw 0 | horizon 0.76/10 sw 0
  S_moveturn 60 kg rep 7: fell_anymal1 0.96/17 sw 0 | fell_anymal1 1.43/28 sw 0
  S_straight 60 kg rep 0: horizon 0.96/9 sw 1 | horizon 0.60/19 sw 3
  S_straight 60 kg rep 1: fell_anymal2 1.46/1 sw 0 | horizon 1.45/1 sw 0
  S_straight 60 kg rep 2: horizon 0.36/8 sw 0 | horizon 0.35/8 sw 0
  S_straight 60 kg rep 3: fell_anymal1 1.11/1 sw 0 | horizon 1.05/9 sw 0
  S_straight 60 kg rep 4: fell_anymal2 0.51/3 sw 0 | horizon 0.28/5 sw 0
  S_straight 60 kg rep 5: horizon 0.26/3 sw 0 | horizon 0.31/5 sw 0
  S_straight 60 kg rep 6: horizon 0.77/10 sw 0 | horizon 0.85/9 sw 0
  S_straight 60 kg rep 7: horizon 0.13/0 sw 0 | horizon 0.11/1 sw 2
