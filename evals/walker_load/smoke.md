# Spot-arm walker under load

4 envs per row; no objects; force against the commanded travel (scripts/spot_arm/walker_load_test.py)

## Ramp: forward 0.3 m/s against a force rising 20 N/s to 250 N

| policy | arm (force on) | torso | held force N, median (25%) | displacement m | yaw drift deg | foot slip m/s | torque sat | falls |
|---|---|---|---|---|---|---|---|---|
| rai | stowed (trunk) | default | 70 (70) | 0.61 | 2.9 | 0.019 | 0.000 | 0.00 |
| rai | stowed (trunk) | lowered | 73 (73) | 0.63 | 3.5 | 0.021 | 0.000 | 0.00 |
| rai | braced (hand) | default | 71 (69) | 0.58 | 3.1 | 0.019 | 0.000 | 0.00 |
| rai | braced (hand) | lowered | 71 (69) | 0.58 | 2.9 | 0.018 | 0.000 | 0.00 |

## Sweep: 8 s per command, arm stowed, torso default, force on the trunk

| policy | force | command | planar vel err m/s | yaw-rate err rad/s | yaw drift deg | foot slip m/s | falls |
|---|---|---|---|---|---|---|---|
| rai | 0 N | forward | 0.057 | 0.042 | 0.9 | 0.040 | 0.00 |
| rai | 0 N | sideways | 0.067 | 0.059 | 7.3 | 0.042 | 0.00 |
| rai | 0 N | backward | 0.092 | 0.030 | 8.0 | 0.043 | 0.00 |
| rai | 0 N | turn | 0.052 | 0.058 | nan | 0.040 | 0.00 |
| rai | 0 N | stop | 0.007 | 0.011 | 4.7 | 0.006 | 0.00 |
| rai | 60 N | forward | 0.242 | 0.042 | 0.8 | 0.022 | 0.00 |
| rai | 60 N | sideways | 0.224 | 0.057 | 1.7 | 0.031 | 0.00 |
| rai | 60 N | backward | 0.279 | 0.023 | 7.0 | 0.022 | 0.00 |
| rai | 60 N | turn | 0.117 | 0.090 | nan | 0.055 | 0.00 |
| rai | 60 N | stop | 0.022 | 0.013 | 5.8 | 0.014 | 0.00 |
