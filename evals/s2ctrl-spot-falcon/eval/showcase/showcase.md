# Showcase: s2ctrl-spot-falcon

Each cell: scenarios A / B / C as successful attempts out of 3 (S = filmed success, F = all 3 failed).

| object | 10 kg | 25 kg | 40 kg |
|---|---|---|---|
| cube | 3S / 3S / 2S | 3S / 2S / 3S | 3S / 1S / 2S |
| long | 3S / 3S / 3S | 3S / 1S / 3S | 1S / 1S / 3S |
| sphere | 3S / 3S / 3S | 3S / 3S / 3S | 3S / 3S / 3S |
| cylinder | 3S / 1S / 0F | 3S / 3S / 0F | 3S / 2S / 0F |
| arch | 0F / 0F / 1S | 0F / 0F / 1S | 0F / 0F / 0F |
| dumbbell | 3S / 1S / 3S | 2S / 2S / 0F | 2S / 0F / 0F |
| t_shape | 3S / 2S / 3S | 3S / 2S / 3S | 3S / 3S / 1S |
| beam (unseen) | 3S / 1S / 1S | 1S / 2S / 1S | 1S / 0F / 0F |
| l_shape (unseen) | 3S / 2S / 3S | 3S / 3S / 3S | 2S / 0F / 1S |
| asym (unseen) | 3S / 3S / 3S | 1S / 1S / 2S | 0F / 0F / 0F |
| u_channel (unseen) | 2S / 2S / 1S | 3S / 0F / 3S | 3S / 1S / 1S |
| plus (unseen) | 1S / 1S / 0F | 0F / 0F / 0F | 0F / 0F / 0F |

Succeeded (any attempt): 10 kg 32/36, 25 kg 28/36, 40 kg 21/36

Failures (all 3 attempts failed):

- cylinder 10 kg C_backright: horizon horizon horizon; final error 0.078 m / 54.1 deg, closest 0.003 m 
- arch 10 kg A_straight: horizon horizon horizon; final error 0.283 m / 50.4 deg, closest 0.198 m 
- arch 10 kg B_left: horizon horizon horizon; final error 0.107 m / 45.4 deg, closest 0.031 m 
- plus 10 kg C_backright: fell horizon horizon; final error 0.655 m / 8.4 deg, closest 0.652 m on its side (tilt 61 deg)
- cylinder 25 kg C_backright: horizon horizon horizon; final error 0.08 m / 61.9 deg, closest 0.031 m 
- arch 25 kg A_straight: horizon fell horizon; final error 0.656 m / 79.0 deg, closest 0.656 m 
- arch 25 kg B_left: horizon horizon horizon; final error 0.239 m / 6.0 deg, closest 0.024 m 
- dumbbell 25 kg C_backright: horizon horizon fell; final error 0.247 m / 77.6 deg, closest 0.163 m 
- u_channel 25 kg B_left: fell fell horizon; final error 0.252 m / 12.7 deg, closest 0.032 m on its side (tilt 62 deg)
- plus 25 kg A_straight: horizon horizon horizon; final error 1.129 m / 6.3 deg, closest 1.129 m 
- plus 25 kg B_left: fell horizon horizon; final error 1.748 m / 38.9 deg, closest 1.631 m on its side (tilt 60 deg)
- plus 25 kg C_backright: horizon horizon horizon; final error 0.5 m / 2.1 deg, closest 0.5 m 
- cylinder 40 kg C_backright: horizon fell horizon; final error 0.045 m / 69.0 deg, closest 0.003 m 
- arch 40 kg A_straight: fell horizon horizon; final error 1.708 m / 38.8 deg, closest 1.708 m on its side (tilt 63 deg)
- arch 40 kg B_left: fell horizon horizon; final error 0.096 m / 34.5 deg, closest 0.08 m on its side (tilt 61 deg)
- arch 40 kg C_backright: horizon horizon horizon; final error 1.306 m / 17.8 deg, closest 1.306 m 
- dumbbell 40 kg B_left: horizon horizon fell; final error 0.143 m / 88.2 deg, closest 0.143 m 
- dumbbell 40 kg C_backright: fell horizon horizon; final error 1.14 m / 9.7 deg, closest 1.14 m on its side (tilt 63 deg)
- beam 40 kg B_left: horizon horizon fell; final error 0.507 m / 70.6 deg, closest 0.428 m 
- beam 40 kg C_backright: fell fell fell; final error 3.131 m / 46.5 deg, closest 3.0 m on its side (tilt 63 deg)
- l_shape 40 kg B_left: fell fell fell; final error 0.132 m / 17.0 deg, closest 0.132 m on its side (tilt 60 deg)
- asym 40 kg A_straight: fell horizon fell; final error 1.794 m / 4.3 deg, closest 1.794 m on its side (tilt 60 deg)
- asym 40 kg B_left: fell horizon horizon; final error 2.171 m / 79.5 deg, closest 2.171 m on its side (tilt 62 deg)
- asym 40 kg C_backright: horizon fell fell; final error 0.81 m / 6.3 deg, closest 0.779 m 
- plus 40 kg A_straight: horizon fell fell; final error 2.124 m / 23.7 deg, closest 2.124 m 
- plus 40 kg B_left: fell horizon horizon; final error 2.647 m / 2.9 deg, closest 2.647 m on its side (tilt 60 deg)
- plus 40 kg C_backright: horizon fell fell; final error 0.208 m / 15.3 deg, closest 0.208 m 
