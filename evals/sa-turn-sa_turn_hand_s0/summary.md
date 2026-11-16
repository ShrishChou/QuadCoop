# Turn in place, MAPPO it 2000 (hand_rate) logs/marl2/sa_turn_hand_s0/model_2000.pt: +-40 deg, 20 kg long object

8 placements per direction x swap, horizon 20 s, seed 7200. Success: centre < 0.1 m and heading < 6 deg held 1 s.

| condition | turn | episodes | success | falls | time to success, median s | largest centre drift, median m | end centre error, median m | end heading error, median abs deg | hand contact (robot 1 / 2) | trunk contact (1 / 2) |
|---|---|---|---|---|---|---|---|---|---|---|
| both_hands | ccw | 16 | 100% | 6% | 4.7 | 0.22 | 0.220 | 14.8 | 0% / 0% | 4% / 6% |
| both_hands | cw | 16 | 69% | 0% | 5.5 | 0.24 | 0.237 | 10.2 | 0% / 0% | 2% / 4% |
| both_hands | both | 32 | 84% | 3% | 4.8 | 0.22 | 0.220 | 12.4 | 0% / 0% | 3% / 5% |
| hand_1 | ccw | 16 | 100% | 0% | 4.7 | 0.19 | 0.139 | 9.0 | 0% / 0% | 3% / 5% |
| hand_1 | cw | 16 | 56% | 6% | 5.1 | 0.17 | 0.115 | 10.3 | 0% / 0% | 1% / 6% |
| hand_1 | both | 32 | 78% | 3% | 4.7 | 0.17 | 0.138 | 9.9 | 0% / 0% | 2% / 6% |
| hand_2 | ccw | 16 | 94% | 6% | 4.7 | 0.16 | 0.147 | 13.6 | 0% / 0% | 3% / 7% |
| hand_2 | cw | 16 | 88% | 0% | 5.2 | 0.27 | 0.259 | 16.8 | 0% / 0% | 1% / 2% |
| hand_2 | both | 32 | 91% | 3% | 4.8 | 0.21 | 0.202 | 15.2 | 0% / 0% | 2% / 5% |
| stowed | ccw | 16 | 100% | 0% | 4.8 | 0.25 | 0.202 | 15.1 | 0% / 0% | 5% / 7% |
| stowed | cw | 16 | 44% | 0% | 5.2 | 0.21 | 0.166 | 8.7 | 0% / 0% | 1% / 5% |
| stowed | both | 32 | 72% | 0% | 4.8 | 0.21 | 0.175 | 9.8 | 0% / 0% | 3% / 6% |
| solo_1 | ccw | 16 | 0% | 0% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 0% |
| solo_1 | cw | 16 | 0% | 0% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 0% |
| solo_1 | both | 32 | 0% | 0% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 0% |
| solo_2 | ccw | 16 | 0% | 0% | nan | 0.76 | 0.761 | 52.7 | 0% / 0% | 0% / 5% |
| solo_2 | cw | 16 | 0% | 0% | nan | 0.74 | 0.458 | 30.8 | 0% / 0% | 0% / 6% |
| solo_2 | both | 32 | 0% | 0% | nan | 0.75 | 0.593 | 40.0 | 0% / 0% | 0% / 6% |
