# Turn in place, MAPPO it 2000 (hand_rate) logs/marl2/sa_turn_bc_s1/model_2000.pt: +-40 deg, 20 kg long object

8 placements per direction x swap, horizon 20 s, seed 7200. Success: centre < 0.1 m and heading < 6 deg held 1 s.

| condition | turn | episodes | success | falls | time to success, median s | largest centre drift, median m | end centre error, median m | end heading error, median abs deg | hand contact (robot 1 / 2) | trunk contact (1 / 2) |
|---|---|---|---|---|---|---|---|---|---|---|
| both_hands | ccw | 16 | 88% | 0% | 2.7 | 0.61 | 0.613 | 7.5 | 1% / 1% | 7% / 7% |
| both_hands | cw | 16 | 94% | 0% | 3.0 | 0.12 | 0.110 | 3.4 | 5% / 0% | 4% / 16% |
| both_hands | both | 32 | 91% | 0% | 2.8 | 0.39 | 0.385 | 5.5 | 3% / 1% | 5% / 11% |
| hand_1 | ccw | 16 | 88% | 0% | 2.7 | 0.57 | 0.568 | 14.4 | 1% / 0% | 7% / 13% |
| hand_1 | cw | 16 | 100% | 0% | 3.5 | 0.12 | 0.116 | 2.0 | 4% / 0% | 10% / 20% |
| hand_1 | both | 32 | 94% | 0% | 2.8 | 0.27 | 0.241 | 4.9 | 3% / 0% | 9% / 16% |
| hand_2 | ccw | 16 | 100% | 0% | 2.7 | 0.17 | 0.091 | 2.3 | 0% / 2% | 10% / 20% |
| hand_2 | cw | 16 | 100% | 0% | 3.0 | 0.11 | 0.096 | 1.2 | 0% / 0% | 1% / 22% |
| hand_2 | both | 32 | 100% | 0% | 2.8 | 0.12 | 0.094 | 2.0 | 0% / 1% | 6% / 21% |
| stowed | ccw | 16 | 100% | 0% | 2.7 | 0.15 | 0.119 | 1.5 | 0% / 0% | 12% / 27% |
| stowed | cw | 16 | 100% | 0% | 3.2 | 0.14 | 0.104 | 2.9 | 0% / 0% | 3% / 20% |
| stowed | both | 32 | 100% | 0% | 2.8 | 0.15 | 0.104 | 2.1 | 0% / 0% | 7% / 24% |
| solo_1 | ccw | 16 | 0% | 0% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 0% |
| solo_1 | cw | 16 | 0% | 0% | nan | 0.05 | 0.049 | 40.0 | 0% / 0% | 0% / 0% |
| solo_1 | both | 32 | 0% | 0% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 0% |
| solo_2 | ccw | 16 | 0% | 0% | nan | 0.35 | 0.338 | 34.3 | 0% / 0% | 0% / 10% |
| solo_2 | cw | 16 | 0% | 0% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 0% |
| solo_2 | both | 32 | 0% | 0% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 5% |
