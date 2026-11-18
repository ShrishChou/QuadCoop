# Spot-arm walker under load

32 envs per row; no objects; force against the commanded travel (scripts/spot_arm/walker_load_test.py)

## Ramp: forward 0.3 m/s against a force rising 20 N/s to 250 N

| policy | arm (force on) | torso | held force N, median (25%) | displacement m | yaw drift deg | foot slip m/s | torque sat | peak torque / limit | falls |
|---|---|---|---|---|---|---|---|---|---|
| rai | stowed (trunk) | default | 71 (70) | 0.61 | 2.9 | 0.019 | 0.000 | 0.35 | 0.00 |
| rai | stowed (trunk) | lowered | 73 (72) | 0.62 | 3.4 | 0.021 | 0.000 | 0.37 | 0.00 |
| rai | braced (hand) | default | 66 (65) | 0.57 | 3.3 | 0.018 | 0.000 | 0.34 | 0.00 |
| rai | braced (hand) | lowered | 66 (64) | 0.57 | 3.2 | 0.018 | 0.000 | 0.34 | 0.00 |
| s1 | stowed (trunk) | default | 118 (117) | 1.27 | 11.6 | 0.041 | 0.000 | 0.56 | 0.00 |
| s1 | stowed (trunk) | lowered | 82 (81) | 1.06 | 1.3 | 0.029 | 0.000 | 0.48 | 0.00 |
| s1 | braced (hand) | default | 118 (113) | 1.29 | 19.0 | 0.041 | 0.003 | 0.58 | 0.00 |
| s1 | braced (hand) | lowered | 105 (105) | 1.14 | 1.7 | 0.030 | 0.002 | 0.58 | 0.00 |
| s2 | stowed (trunk) | default | 104 (103) | 1.33 | 13.1 | 0.035 | 0.001 | 0.68 | 0.00 |
| s2 | stowed (trunk) | lowered | 124 (122) | 1.19 | 12.4 | 0.038 | 0.002 | 0.63 | 0.00 |
| s2 | braced (hand) | default | 104 (103) | 1.38 | 17.7 | 0.048 | 0.027 | 0.79 | 0.00 |
| s2 | braced (hand) | lowered | 98 (98) | 1.14 | 12.5 | 0.043 | 0.000 | 0.63 | 0.00 |
| s3 | stowed (trunk) | default | 170 (162) | 2.74 | 11.1 | 0.072 | 0.014 | 0.75 | 0.00 |
| s3 | stowed (trunk) | lowered | 175 (166) | 2.92 | 16.9 | 0.085 | 0.012 | 0.75 | 0.00 |
| s3 | braced (hand) | default | 148 (130) | 1.97 | 19.7 | 0.079 | 0.029 | 0.80 | 0.19 |
| s3 | braced (hand) | lowered | 153 (143) | 2.58 | 4.0 | 0.098 | 0.039 | 0.86 | 0.00 |

## Sweep: 8 s per command, arm stowed, torso default, force on the trunk

| policy | force | command | planar vel err m/s | yaw-rate err rad/s | yaw drift deg | foot slip m/s | falls |
|---|---|---|---|---|---|---|---|
| rai | 0 N | forward | 0.057 | 0.042 | 1.0 | 0.040 | 0.00 |
| rai | 0 N | sideways | 0.067 | 0.059 | 7.6 | 0.043 | 0.00 |
| rai | 0 N | backward | 0.092 | 0.030 | 8.0 | 0.042 | 0.00 |
| rai | 0 N | turn | 0.053 | 0.057 | nan | 0.041 | 0.00 |
| rai | 0 N | stop | 0.008 | 0.011 | 3.8 | 0.006 | 0.00 |
| rai | 60 N | forward | 0.242 | 0.041 | 0.7 | 0.021 | 0.00 |
| rai | 60 N | sideways | 0.225 | 0.057 | 2.0 | 0.031 | 0.00 |
| rai | 60 N | backward | 0.278 | 0.023 | 7.0 | 0.023 | 0.00 |
| rai | 60 N | turn | 0.116 | 0.087 | nan | 0.055 | 0.00 |
| rai | 60 N | stop | 0.022 | 0.011 | 4.9 | 0.014 | 0.00 |
| s1 | 0 N | forward | 0.058 | 0.040 | 12.0 | 0.038 | 0.00 |
| s1 | 0 N | sideways | 0.107 | 0.047 | 12.3 | 0.053 | 0.00 |
| s1 | 0 N | backward | 0.097 | 0.051 | 4.0 | 0.062 | 0.00 |
| s1 | 0 N | turn | 0.116 | 0.052 | nan | 0.033 | 0.00 |
| s1 | 0 N | stop | 0.028 | 0.027 | 11.1 | 0.013 | 0.00 |
| s1 | 60 N | forward | 0.180 | 0.066 | 12.1 | 0.027 | 0.00 |
| s1 | 60 N | sideways | 0.183 | 0.073 | 23.6 | 0.037 | 0.00 |
| s1 | 60 N | backward | 0.132 | 0.033 | 8.1 | 0.044 | 0.00 |
| s1 | 60 N | turn | 0.191 | 0.054 | nan | 0.051 | 0.00 |
| s1 | 60 N | stop | 0.054 | 0.028 | 10.2 | 0.022 | 0.00 |
| s2 | 0 N | forward | 0.126 | 0.040 | 10.7 | 0.043 | 0.00 |
| s2 | 0 N | sideways | 0.112 | 0.038 | 1.3 | 0.048 | 0.00 |
| s2 | 0 N | backward | 0.115 | 0.057 | 20.4 | 0.057 | 0.00 |
| s2 | 0 N | turn | 0.150 | 0.055 | nan | 0.031 | 0.00 |
| s2 | 0 N | stop | 0.108 | 0.046 | 16.1 | 0.026 | 0.00 |
| s2 | 60 N | forward | 0.141 | 0.067 | 22.7 | 0.035 | 0.00 |
| s2 | 60 N | sideways | 0.161 | 0.038 | 1.6 | 0.040 | 0.00 |
| s2 | 60 N | backward | 0.160 | 0.047 | 16.0 | 0.043 | 0.00 |
| s2 | 60 N | turn | 0.173 | 0.088 | nan | 0.059 | 0.00 |
| s2 | 60 N | stop | 0.265 | 0.069 | 23.2 | 0.067 | 0.00 |
| s3 | 0 N | forward | 0.161 | 0.051 | 1.3 | 0.047 | 0.00 |
| s3 | 0 N | sideways | 0.250 | 0.053 | 9.6 | 0.082 | 0.00 |
| s3 | 0 N | backward | 0.186 | 0.076 | 25.6 | 0.080 | 0.00 |
| s3 | 0 N | turn | 0.172 | 0.104 | nan | 0.039 | 0.00 |
| s3 | 0 N | stop | 0.120 | 0.064 | 15.7 | 0.030 | 0.00 |
| s3 | 60 N | forward | 0.138 | 0.058 | 18.5 | 0.051 | 0.00 |
| s3 | 60 N | sideways | 0.077 | 0.042 | 0.7 | 0.052 | 0.00 |
| s3 | 60 N | backward | 0.108 | 0.089 | 23.2 | 0.055 | 0.00 |
| s3 | 60 N | turn | 0.156 | 0.095 | nan | 0.059 | 0.00 |
| s3 | 60 N | stop | 0.135 | 0.062 | 18.5 | 0.053 | 0.00 |
