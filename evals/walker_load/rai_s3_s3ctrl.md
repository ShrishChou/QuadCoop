# Spot-arm walker under load

32 envs per row; no objects; force against the commanded travel (scripts/spot_arm/walker_load_test.py)

## Ramp: forward 0.3 m/s against a force rising 20 N/s to 250 N

| policy | arm (force on) | torso | held force N, median (25%) | displacement m | yaw drift deg | foot slip m/s | torque sat | peak torque / limit | falls |
|---|---|---|---|---|---|---|---|---|---|
| rai | stowed (trunk) | default | 71 (70) | 0.62 | 3.1 | 0.019 | 0.000 | 0.36 | 0.00 |
| rai | stowed (trunk) | lowered | 73 (72) | 0.62 | 3.3 | 0.021 | 0.000 | 0.37 | 0.00 |
| rai | braced (hand) | default | 69 (64) | 0.57 | 3.3 | 0.019 | 0.000 | 0.34 | 0.00 |
| rai | braced (hand) | lowered | 72 (65) | 0.58 | 3.2 | 0.019 | 0.000 | 0.34 | 0.00 |
| s3 | stowed (trunk) | default | 170 (157) | 2.75 | 12.1 | 0.073 | 0.015 | 0.76 | 0.00 |
| s3 | stowed (trunk) | lowered | 176 (173) | 2.99 | 16.7 | 0.081 | 0.014 | 0.76 | 0.00 |
| s3 | braced (hand) | default | 151 (135) | 2.05 | 15.4 | 0.072 | 0.027 | 0.78 | 0.19 |
| s3 | braced (hand) | lowered | 158 (146) | 2.63 | 5.1 | 0.083 | 0.039 | 0.86 | 0.00 |
| s3ctrl | stowed (trunk) | default | 92 (91) | 1.09 | 2.7 | 0.050 | 0.009 | 0.79 | 0.00 |
| s3ctrl | stowed (trunk) | lowered | 108 (104) | 1.10 | 9.2 | 0.052 | 0.008 | 0.73 | 0.00 |
| s3ctrl | braced (hand) | default | 89 (87) | 0.96 | 3.9 | 0.064 | 0.052 | 0.89 | 0.00 |
| s3ctrl | braced (hand) | lowered | 99 (94) | 1.05 | 3.9 | 0.073 | 0.039 | 0.86 | 0.00 |

## Sweep: 8 s per command, arm stowed, torso default, force on the trunk

| policy | force | command | planar vel err m/s | yaw-rate err rad/s | yaw drift deg | foot slip m/s | falls |
|---|---|---|---|---|---|---|---|
| rai | 0 N | forward | 0.057 | 0.042 | 1.1 | 0.040 | 0.00 |
| rai | 0 N | sideways | 0.067 | 0.059 | 7.5 | 0.043 | 0.00 |
| rai | 0 N | backward | 0.092 | 0.030 | 8.0 | 0.043 | 0.00 |
| rai | 0 N | turn | 0.053 | 0.058 | nan | 0.040 | 0.00 |
| rai | 0 N | stop | 0.008 | 0.011 | 4.1 | 0.006 | 0.00 |
| rai | 60 N | forward | 0.243 | 0.041 | 0.7 | 0.021 | 0.00 |
| rai | 60 N | sideways | 0.226 | 0.057 | 1.8 | 0.031 | 0.00 |
| rai | 60 N | backward | 0.278 | 0.023 | 6.9 | 0.023 | 0.00 |
| rai | 60 N | turn | 0.116 | 0.087 | nan | 0.055 | 0.00 |
| rai | 60 N | stop | 0.022 | 0.011 | 5.1 | 0.014 | 0.00 |
| s3 | 0 N | forward | 0.161 | 0.050 | 1.3 | 0.047 | 0.00 |
| s3 | 0 N | sideways | 0.250 | 0.054 | 9.7 | 0.081 | 0.00 |
| s3 | 0 N | backward | 0.186 | 0.075 | 25.3 | 0.081 | 0.00 |
| s3 | 0 N | turn | 0.173 | 0.105 | nan | 0.039 | 0.00 |
| s3 | 0 N | stop | 0.115 | 0.062 | 13.9 | 0.029 | 0.00 |
| s3 | 60 N | forward | 0.139 | 0.059 | 18.5 | 0.050 | 0.00 |
| s3 | 60 N | sideways | 0.078 | 0.042 | 0.5 | 0.051 | 0.00 |
| s3 | 60 N | backward | 0.108 | 0.089 | 23.1 | 0.056 | 0.00 |
| s3 | 60 N | turn | 0.157 | 0.092 | nan | 0.057 | 0.00 |
| s3 | 60 N | stop | 0.137 | 0.063 | 17.6 | 0.055 | 0.00 |
| s3ctrl | 0 N | forward | 0.122 | 0.053 | 13.0 | 0.033 | 0.00 |
| s3ctrl | 0 N | sideways | 0.110 | 0.048 | 4.4 | 0.058 | 0.00 |
| s3ctrl | 0 N | backward | 0.165 | 0.049 | 14.0 | 0.065 | 0.00 |
| s3ctrl | 0 N | turn | 0.141 | 0.109 | nan | 0.049 | 0.00 |
| s3ctrl | 0 N | stop | 0.160 | 0.061 | 10.8 | 0.041 | 0.00 |
| s3ctrl | 60 N | forward | 0.217 | 0.123 | 11.5 | 0.051 | 0.00 |
| s3ctrl | 60 N | sideways | 0.135 | 0.062 | 20.6 | 0.043 | 0.00 |
| s3ctrl | 60 N | backward | 0.141 | 0.061 | 24.3 | 0.051 | 0.00 |
| s3ctrl | 60 N | turn | 0.625 | 0.188 | nan | 0.234 | 0.25 |
| s3ctrl | 60 N | stop | 0.298 | 0.082 | 22.4 | 0.074 | 0.00 |
