# Scripted turn in place, +-60 deg, 20 kg long object

8 placements per direction x swap, horizon 20 s, seed 7200. Success: centre < 0.1 m and heading < 6 deg held 1 s.

| condition | turn | episodes | success | falls | time to success, median s | largest centre drift, median m | end centre error, median m | end heading error, median abs deg | hand contact (robot 1 / 2) | trunk contact (1 / 2) |
|---|---|---|---|---|---|---|---|---|---|---|
| both_hands | ccw | 16 | 56% | 0% | 12.8 | 0.03 | 0.013 | 3.1 | 70% / 70% | 5% / 6% |
| both_hands | cw | 16 | 12% | 0% | 19.5 | 0.04 | 0.010 | 9.9 | 81% / 81% | 22% / 25% |
| both_hands | both | 32 | 34% | 0% | 14.5 | 0.03 | 0.010 | 6.9 | 75% / 75% | 14% / 16% |
| hand_1 | ccw | 16 | 56% | 0% | 17.4 | 0.09 | 0.053 | 2.7 | 77% / 0% | 7% / 59% |
| hand_1 | cw | 16 | 0% | 0% | nan | 0.07 | 0.017 | 20.1 | 82% / 0% | 26% / 66% |
| hand_1 | both | 32 | 28% | 0% | 17.4 | 0.08 | 0.040 | 11.7 | 79% / 0% | 17% / 62% |
| hand_2 | ccw | 16 | 31% | 0% | 14.8 | 0.09 | 0.059 | 8.5 | 0% / 75% | 57% / 7% |
| hand_2 | cw | 16 | 0% | 0% | nan | 0.07 | 0.017 | 22.5 | 0% / 82% | 67% / 27% |
| hand_2 | both | 32 | 16% | 0% | 14.8 | 0.08 | 0.034 | 13.8 | 0% / 78% | 62% / 17% |
| stowed | ccw | 16 | 0% | 0% | nan | 0.04 | 0.014 | 17.6 | 0% / 0% | 64% / 65% |
| stowed | cw | 16 | 0% | 0% | nan | 0.04 | 0.017 | 21.8 | 0% / 0% | 69% / 67% |
| stowed | both | 32 | 0% | 0% | nan | 0.04 | 0.014 | 18.9 | 0% / 0% | 66% / 66% |
| solo_1 | ccw | 16 | 0% | 0% | nan | 0.17 | 0.171 | 45.5 | 82% / 0% | 0% / 0% |
| solo_1 | cw | 16 | 0% | 0% | nan | 0.20 | 0.195 | 43.6 | 81% / 0% | 0% / 0% |
| solo_1 | both | 32 | 0% | 0% | nan | 0.18 | 0.184 | 44.4 | 82% / 0% | 0% / 0% |
| solo_2 | ccw | 16 | 0% | 0% | nan | 0.16 | 0.158 | 46.5 | 0% / 83% | 0% / 0% |
| solo_2 | cw | 16 | 0% | 0% | nan | 0.19 | 0.192 | 43.8 | 0% / 81% | 0% / 0% |
| solo_2 | both | 32 | 0% | 0% | nan | 0.18 | 0.182 | 44.7 | 0% / 82% | 0% / 0% |
