# Spot-arm walker under load

32 envs per row; no objects; force against the commanded travel (scripts/spot_arm/walker_load_test.py)

## Ramp: forward 0.3 m/s against a force rising 20 N/s to 250 N

| policy | arm (force on) | torso | held force N, median (25%) | displacement m | yaw drift deg | foot slip m/s | torque sat | peak torque / limit | falls |
|---|---|---|---|---|---|---|---|---|---|
| rai | stowed (trunk) | default | 71 (70) | 0.62 | 3.0 | 0.020 | 0.000 | 0.36 | 0.00 |
| rai | stowed (trunk) | lowered | 73 (72) | 0.62 | 3.3 | 0.021 | 0.000 | 0.37 | 0.00 |
| rai | braced (hand) | default | 71 (65) | 0.58 | 3.3 | 0.019 | 0.000 | 0.34 | 0.00 |
| rai | braced (hand) | lowered | 71 (64) | 0.57 | 3.1 | 0.019 | 0.000 | 0.34 | 0.00 |
| s1 | stowed (trunk) | default | 118 (118) | 1.26 | 10.8 | 0.045 | 0.000 | 0.57 | 0.00 |
| s1 | stowed (trunk) | lowered | 83 (82) | 1.07 | 1.2 | 0.028 | 0.000 | 0.48 | 0.00 |
| s1 | braced (hand) | default | 123 (116) | 1.30 | 20.1 | 0.043 | 0.004 | 0.59 | 0.00 |
| s1 | braced (hand) | lowered | 106 (105) | 1.16 | 2.0 | 0.031 | 0.002 | 0.57 | 0.00 |
| s2 | stowed (trunk) | default | 104 (103) | 1.34 | 13.2 | 0.033 | 0.001 | 0.66 | 0.00 |
| s2 | stowed (trunk) | lowered | 123 (122) | 1.18 | 12.6 | 0.038 | 0.002 | 0.64 | 0.00 |
| s2 | braced (hand) | default | 105 (103) | 1.33 | 17.8 | 0.044 | 0.029 | 0.79 | 0.03 |
| s2 | braced (hand) | lowered | 100 (98) | 1.17 | 10.9 | 0.045 | 0.000 | 0.64 | 0.00 |

## Sweep: 8 s per command, arm stowed, torso default, force on the trunk

| policy | force | command | planar vel err m/s | yaw-rate err rad/s | yaw drift deg | foot slip m/s | falls |
|---|---|---|---|---|---|---|---|
| rai | 0 N | forward | 0.057 | 0.042 | 1.0 | 0.040 | 0.00 |
| rai | 0 N | sideways | 0.067 | 0.059 | 7.5 | 0.043 | 0.00 |
| rai | 0 N | backward | 0.092 | 0.030 | 8.0 | 0.043 | 0.00 |
| rai | 0 N | turn | 0.053 | 0.057 | nan | 0.040 | 0.00 |
| rai | 0 N | stop | 0.008 | 0.011 | 4.1 | 0.006 | 0.00 |
| rai | 60 N | forward | 0.243 | 0.041 | 0.7 | 0.021 | 0.00 |
| rai | 60 N | sideways | 0.226 | 0.057 | 1.8 | 0.031 | 0.00 |
| rai | 60 N | backward | 0.278 | 0.023 | 7.0 | 0.023 | 0.00 |
| rai | 60 N | turn | 0.116 | 0.087 | nan | 0.054 | 0.00 |
| rai | 60 N | stop | 0.022 | 0.013 | 6.1 | 0.014 | 0.00 |
| s1 | 0 N | forward | 0.058 | 0.040 | 11.9 | 0.038 | 0.00 |
| s1 | 0 N | sideways | 0.107 | 0.047 | 12.2 | 0.053 | 0.00 |
| s1 | 0 N | backward | 0.097 | 0.051 | 3.9 | 0.064 | 0.00 |
| s1 | 0 N | turn | 0.115 | 0.054 | nan | 0.032 | 0.00 |
| s1 | 0 N | stop | 0.027 | 0.026 | 10.6 | 0.013 | 0.00 |
| s1 | 60 N | forward | 0.182 | 0.067 | 11.3 | 0.028 | 0.00 |
| s1 | 60 N | sideways | 0.182 | 0.072 | 23.6 | 0.037 | 0.00 |
| s1 | 60 N | backward | 0.132 | 0.033 | 8.1 | 0.045 | 0.00 |
| s1 | 60 N | turn | 0.189 | 0.052 | nan | 0.051 | 0.00 |
| s1 | 60 N | stop | 0.051 | 0.027 | 10.0 | 0.021 | 0.00 |
| s2 | 0 N | forward | 0.126 | 0.040 | 10.6 | 0.043 | 0.00 |
| s2 | 0 N | sideways | 0.112 | 0.038 | 1.4 | 0.047 | 0.00 |
| s2 | 0 N | backward | 0.116 | 0.057 | 20.4 | 0.058 | 0.00 |
| s2 | 0 N | turn | 0.150 | 0.056 | nan | 0.031 | 0.00 |
| s2 | 0 N | stop | 0.102 | 0.044 | 14.0 | 0.025 | 0.00 |
| s2 | 60 N | forward | 0.140 | 0.067 | 23.0 | 0.035 | 0.00 |
| s2 | 60 N | sideways | 0.161 | 0.039 | 1.8 | 0.041 | 0.00 |
| s2 | 60 N | backward | 0.159 | 0.047 | 15.8 | 0.042 | 0.00 |
| s2 | 60 N | turn | 0.173 | 0.088 | nan | 0.060 | 0.00 |
| s2 | 60 N | stop | 0.265 | 0.069 | 23.2 | 0.065 | 0.00 |
