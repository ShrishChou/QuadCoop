32 matched tasks per arm; arms {'A': 'fbA-f05', 'B': 'fbB-f05'}

| group | arm | n | success | pos_err | yaw_err | yaw_unint | fell | time | settled | share_req | share_deliv | share_err | v_err | w_err | duty_both | duty_each | switches | share_corr | v_corr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | A | 32 | 0.219 | 0.343 | 6.609 | 8.962 | 0.094 | 17.414 | 0.219 | 0.512 | 0.474 | 0.170 | 0.224 | 7.162 | 0.329 | 0.540 | 1.688 | 0.000 | 0.000 |
| all | B | 32 | 0.219 | 0.430 | 6.528 | 8.697 | 0.219 | 18.012 | 0.156 | 0.514 | 0.486 | 0.219 | 0.224 | 7.113 | 0.298 | 0.524 | 1.906 | 0.000 | 0.038 |
| 40 kg | A | 16 | 0.250 | 0.213 | 7.162 | 10.977 | 0.000 | 16.668 | 0.250 | 0.504 | 0.486 | 0.185 | 0.215 | 7.836 | 0.209 | 0.431 | 1.875 | 0.000 | 0.000 |
| 40 kg | B | 16 | 0.438 | 0.206 | 7.138 | 11.239 | 0.062 | 16.024 | 0.312 | 0.498 | 0.515 | 0.247 | 0.208 | 8.085 | 0.191 | 0.429 | 2.625 | 0.000 | 0.048 |
| 60 kg | A | 16 | 0.188 | 0.473 | 6.056 | 6.946 | 0.188 | 18.161 | 0.188 | 0.520 | 0.462 | 0.154 | 0.233 | 6.488 | 0.449 | 0.649 | 1.500 | 0.000 | 0.000 |
| 60 kg | B | 16 | 0.000 | 0.654 | 5.919 | 6.154 | 0.375 | 20.000 | 0.000 | 0.528 | 0.460 | 0.193 | 0.241 | 6.141 | 0.405 | 0.619 | 1.188 | 0.000 | 0.028 |
| S_moveturn | A | 16 | 0.000 | 0.385 | 8.387 | nan | 0.188 | 20.000 | 0.000 | 0.504 | 0.515 | 0.165 | 0.233 | 8.316 | 0.220 | 0.446 | 1.500 | 0.000 | 0.000 |
| S_moveturn | B | 16 | 0.000 | 0.425 | 8.244 | nan | 0.250 | 20.000 | 0.000 | 0.510 | 0.509 | 0.230 | 0.236 | 8.724 | 0.226 | 0.475 | 1.812 | 0.000 | 0.037 |
| S_straight | A | 16 | 0.438 | 0.301 | 4.831 | 8.962 | 0.000 | 14.829 | 0.438 | 0.520 | 0.432 | 0.174 | 0.215 | 6.008 | 0.438 | 0.634 | 1.875 | 0.000 | 0.000 |
| S_straight | B | 16 | 0.438 | 0.435 | 4.812 | 8.697 | 0.188 | 16.024 | 0.312 | 0.517 | 0.465 | 0.209 | 0.212 | 5.502 | 0.370 | 0.572 | 2.000 | 0.000 | 0.039 |

Paired differences vs A (mean [95% CI]): success / fell in points, errors in m and deg, time in s
| group | arm | success | fell | pos_err | yaw_err | yaw_unint | time | share_err | v_err | w_err | duty_both | switches |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | B | +0.00 [-15.62, +15.62] | +12.50 [-3.12, +28.12] | +0.09 [-0.03, +0.20] | -0.08 [-1.98, +1.99] | -0.26 [-1.40, +0.79] | +0.60 [-0.94, +2.08] | +0.05 [+0.02, +0.08] | +0.00 [-0.02, +0.02] | -0.05 [-1.06, +1.22] | -3.11 [-6.66, +0.58] | +0.22 [-0.31, +0.75] |
| 40 kg | B | +18.75 [+0.00, +37.50] | +6.25 [+0.00, +18.75] | -0.01 [-0.11, +0.12] | -0.02 [-2.64, +3.40] | +0.26 [-1.22, +1.72] | -0.64 [-2.83, +1.64] | +0.06 [+0.03, +0.10] | -0.01 [-0.04, +0.03] | +0.25 [-1.41, +2.62] | -1.80 [-5.95, +1.49] | +0.75 [-0.06, +1.50] |
| 60 kg | B | -18.75 [-37.50, +0.00] | +18.75 [-12.50, +50.00] | +0.18 [-0.00, +0.37] | -0.14 [-3.12, +2.51] | -0.79 [-2.45, +0.69] | +1.84 [+0.00, +3.77] | +0.04 [-0.00, +0.07] | +0.01 [-0.01, +0.02] | -0.35 [-1.52, +0.85] | -4.41 [-10.21, +2.05] | -0.31 [-0.94, +0.31] |
| S_moveturn | B | +0.00 [+0.00, +0.00] | +6.25 [-18.75, +31.25] | +0.04 [-0.11, +0.20] | -0.14 [-3.80, +4.24] | +nan [+nan, +nan] | +0.00 [+0.00, +0.00] | +0.07 [+0.04, +0.10] | +0.00 [-0.02, +0.03] | +0.41 [-1.48, +2.98] | +0.56 [-2.43, +4.16] | +0.31 [-0.50, +1.06] |
| S_straight | B | +0.00 [-31.25, +31.25] | +18.75 [+0.00, +37.50] | +0.13 [-0.01, +0.31] | -0.02 [-1.11, +0.84] | -0.26 [-1.40, +0.79] | +1.19 [-1.83, +4.18] | +0.03 [-0.01, +0.07] | -0.00 [-0.03, +0.02] | -0.51 [-1.34, +0.26] | -6.77 [-12.44, -0.76] | +0.12 [-0.62, +0.88] |

B vs A: gained 3, lost 3
  + S_straight 40 kg rep 0 (horizon -> success)
  + S_straight 40 kg rep 3 (horizon -> success)
  + S_straight 40 kg rep 6 (horizon -> success)
  - S_straight 60 kg rep 4 (success -> horizon)
  - S_straight 60 kg rep 5 (success -> horizon)
  - S_straight 60 kg rep 7 (success -> fell_anymal1)

Per task: outcome, final pos err m / heading err deg, switches: A | B
  S_moveturn 40 kg rep 0: horizon 0.53/11 sw 0 | horizon 0.14/5 sw 2
  S_moveturn 40 kg rep 1: horizon 0.40/10 sw 0 | horizon 0.17/4 sw 2
  S_moveturn 40 kg rep 2: horizon 0.08/15 sw 1 | horizon 0.15/12 sw 2
  S_moveturn 40 kg rep 3: horizon 0.18/11 sw 1 | horizon 0.15/10 sw 2
  S_moveturn 40 kg rep 4: horizon 0.11/0 sw 3 | fell_anymal1 0.82/21 sw 0
  S_moveturn 40 kg rep 5: horizon 0.14/7 sw 2 | horizon 0.13/0 sw 4
  S_moveturn 40 kg rep 6: horizon 0.14/2 sw 3 | horizon 0.19/8 sw 2
  S_moveturn 40 kg rep 7: horizon 0.11/12 sw 1 | horizon 0.14/11 sw 2
  S_moveturn 60 kg rep 0: fell_anymal1 0.12/2 sw 2 | horizon 0.33/2 sw 2
  S_moveturn 60 kg rep 1: horizon 0.46/8 sw 3 | fell_anymal1 0.48/5 sw 2
  S_moveturn 60 kg rep 2: horizon 0.65/10 sw 2 | horizon 0.67/6 sw 2
  S_moveturn 60 kg rep 3: horizon 0.50/4 sw 2 | fell_anymal1 1.03/15 sw 0
  S_moveturn 60 kg rep 4: horizon 0.17/4 sw 2 | horizon 0.25/2 sw 2
  S_moveturn 60 kg rep 5: fell_anymal1 1.17/21 sw 0 | horizon 0.43/4 sw 3
  S_moveturn 60 kg rep 6: horizon 0.58/6 sw 2 | horizon 0.55/3 sw 2
  S_moveturn 60 kg rep 7: fell_anymal1 0.84/13 sw 0 | fell_anymal1 1.18/21 sw 0
  S_straight 40 kg rep 0: horizon 0.25/6 sw 0 | success 0.09/5 sw 4
  S_straight 40 kg rep 1: horizon 0.85/26 sw 1 | horizon 0.87/26 sw 1
  S_straight 40 kg rep 2: success 0.03/2 sw 4 | success 0.05/1 sw 4
  S_straight 40 kg rep 3: horizon 0.25/7 sw 1 | success 0.10/1 sw 2
  S_straight 40 kg rep 4: success 0.03/0 sw 4 | success 0.06/1 sw 4
  S_straight 40 kg rep 5: success 0.03/1 sw 3 | success 0.05/1 sw 4
  S_straight 40 kg rep 6: horizon 0.23/4 sw 3 | success 0.09/5 sw 2
  S_straight 40 kg rep 7: success 0.06/1 sw 3 | success 0.09/2 sw 5
  S_straight 60 kg rep 0: horizon 0.20/4 sw 0 | horizon 0.69/1 sw 0
  S_straight 60 kg rep 1: horizon 1.41/3 sw 0 | horizon 1.37/5 sw 0
  S_straight 60 kg rep 2: horizon 0.23/6 sw 1 | horizon 0.20/9 sw 1
  S_straight 60 kg rep 3: horizon 0.22/1 sw 2 | fell_anymal1 0.85/2 sw 1
  S_straight 60 kg rep 4: success 0.05/1 sw 4 | horizon 0.12/2 sw 1
  S_straight 60 kg rep 5: success 0.02/4 sw 2 | horizon 0.23/2 sw 2
  S_straight 60 kg rep 6: horizon 0.90/8 sw 0 | fell_anymal1 0.93/9 sw 1
  S_straight 60 kg rep 7: success 0.05/3 sw 2 | fell_anymal1 1.17/5 sw 0
