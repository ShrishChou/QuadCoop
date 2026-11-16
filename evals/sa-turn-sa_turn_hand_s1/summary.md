# Turn in place, MAPPO it 2000 (hand_rate) logs/marl2/sa_turn_hand_s1/model_2000.pt: +-40 deg, 20 kg long object

8 placements per direction x swap, horizon 20 s, seed 7200. Success: centre < 0.1 m and heading < 6 deg held 1 s.

| condition | turn | episodes | success | falls | time to success, median s | largest centre drift, median m | end centre error, median m | end heading error, median abs deg | hand contact (robot 1 / 2) | trunk contact (1 / 2) |
|---|---|---|---|---|---|---|---|---|---|---|
| both_hands | ccw | 16 | 100% | 25% | 2.8 | 0.22 | 0.224 | 7.0 | 0% / 0% | 5% / 7% |
| both_hands | cw | 16 | 100% | 0% | 2.8 | 0.34 | 0.341 | 6.4 | 0% / 0% | 0% / 1% |
| both_hands | both | 32 | 100% | 12% | 2.8 | 0.25 | 0.253 | 6.5 | 0% / 0% | 2% / 4% |
| hand_1 | ccw | 16 | 94% | 12% | 2.7 | 0.15 | 0.114 | 7.3 | 0% / 0% | 4% / 6% |
| hand_1 | cw | 16 | 100% | 0% | 2.8 | 0.35 | 0.351 | 6.4 | 0% / 0% | 0% / 1% |
| hand_1 | both | 32 | 97% | 6% | 2.8 | 0.27 | 0.269 | 7.2 | 0% / 0% | 2% / 3% |
| hand_2 | ccw | 16 | 100% | 6% | 2.8 | 0.33 | 0.329 | 4.8 | 0% / 0% | 5% / 7% |
| hand_2 | cw | 16 | 100% | 6% | 2.8 | 0.29 | 0.288 | 5.6 | 2% / 0% | 1% / 1% |
| hand_2 | both | 32 | 100% | 6% | 2.8 | 0.32 | 0.317 | 5.4 | 1% / 0% | 3% / 4% |
| stowed | ccw | 16 | 100% | 19% | 2.8 | 0.15 | 0.118 | 11.0 | 3% / 0% | 6% / 8% |
| stowed | cw | 16 | 100% | 0% | 2.8 | 0.36 | 0.364 | 6.8 | 0% / 0% | 0% / 1% |
| stowed | both | 32 | 100% | 9% | 2.8 | 0.32 | 0.317 | 7.6 | 2% / 0% | 3% / 5% |
| solo_1 | ccw | 16 | 0% | 0% | nan | 0.05 | 0.046 | 40.0 | 0% / 0% | 0% / 0% |
| solo_1 | cw | 16 | 0% | 0% | nan | 0.49 | 0.489 | 42.8 | 0% / 0% | 2% / 0% |
| solo_1 | both | 32 | 0% | 0% | nan | 0.05 | 0.046 | 40.0 | 0% / 0% | 1% / 0% |
| solo_2 | ccw | 16 | 0% | 44% | nan | 0.01 | 0.012 | 40.0 | 0% / 0% | 0% / 0% |
| solo_2 | cw | 16 | 0% | 25% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 1% |
| solo_2 | both | 32 | 0% | 34% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 0% |
