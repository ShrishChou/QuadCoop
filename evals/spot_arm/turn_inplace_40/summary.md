# Scripted turn in place, +-40 deg, 20 kg long object

8 placements per direction x swap, horizon 20 s, seed 7200. Success: centre < 0.1 m and heading < 6 deg held 1 s.

| condition | turn | episodes | success | falls | time to success, median s | largest centre drift, median m | end centre error, median m | end heading error, median abs deg | hand contact (robot 1 / 2) | trunk contact (1 / 2) |
|---|---|---|---|---|---|---|---|---|---|---|
| both_hands | ccw | 16 | 69% | 0% | 11.7 | 0.02 | 0.010 | 2.4 | 58% / 59% | 0% / 0% |
| both_hands | cw | 16 | 88% | 0% | 14.3 | 0.02 | 0.013 | 1.7 | 64% / 64% | 4% / 3% |
| both_hands | both | 32 | 78% | 0% | 13.1 | 0.02 | 0.011 | 2.3 | 61% / 61% | 2% / 2% |
| hand_1 | ccw | 16 | 81% | 0% | 14.3 | 0.07 | 0.038 | 2.3 | 66% / 0% | 1% / 51% |
| hand_1 | cw | 16 | 38% | 0% | 18.1 | 0.06 | 0.032 | 12.9 | 78% / 0% | 6% / 65% |
| hand_1 | both | 32 | 59% | 0% | 16.0 | 0.06 | 0.035 | 3.0 | 72% / 0% | 4% / 58% |
| hand_2 | ccw | 16 | 69% | 0% | 14.7 | 0.06 | 0.040 | 2.3 | 0% / 68% | 52% / 2% |
| hand_2 | cw | 16 | 25% | 0% | 16.0 | 0.05 | 0.026 | 11.9 | 0% / 78% | 67% / 6% |
| hand_2 | both | 32 | 47% | 0% | 15.4 | 0.06 | 0.030 | 5.9 | 0% / 73% | 59% / 4% |
| stowed | ccw | 16 | 50% | 0% | 18.7 | 0.02 | 0.008 | 7.0 | 0% / 0% | 63% / 63% |
| stowed | cw | 16 | 0% | 0% | nan | 0.03 | 0.013 | 13.2 | 0% / 0% | 68% / 69% |
| stowed | both | 32 | 25% | 0% | 18.7 | 0.03 | 0.012 | 8.8 | 0% / 0% | 65% / 66% |
| solo_1 | ccw | 16 | 0% | 0% | nan | 0.12 | 0.118 | 30.3 | 82% / 0% | 0% / 0% |
| solo_1 | cw | 16 | 0% | 0% | nan | 0.14 | 0.142 | 27.8 | 81% / 0% | 0% / 0% |
| solo_1 | both | 32 | 0% | 0% | nan | 0.13 | 0.130 | 28.8 | 82% / 0% | 0% / 0% |
| solo_2 | ccw | 16 | 0% | 0% | nan | 0.10 | 0.104 | 31.1 | 0% / 83% | 0% / 0% |
| solo_2 | cw | 16 | 0% | 0% | nan | 0.14 | 0.140 | 28.0 | 0% / 81% | 0% / 0% |
| solo_2 | both | 32 | 0% | 0% | nan | 0.13 | 0.128 | 28.8 | 0% / 82% | 0% / 0% |
