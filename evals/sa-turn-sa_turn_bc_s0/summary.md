# Turn in place, MAPPO it 2000 (hand_rate) logs/marl2/sa_turn_bc_s0/model_2000.pt: +-40 deg, 20 kg long object

8 placements per direction x swap, horizon 20 s, seed 7200. Success: centre < 0.1 m and heading < 6 deg held 1 s.

| condition | turn | episodes | success | falls | time to success, median s | largest centre drift, median m | end centre error, median m | end heading error, median abs deg | hand contact (robot 1 / 2) | trunk contact (1 / 2) |
|---|---|---|---|---|---|---|---|---|---|---|
| both_hands | ccw | 16 | 100% | 0% | 2.7 | 0.35 | 0.347 | 10.3 | 2% / 1% | 12% / 2% |
| both_hands | cw | 16 | 94% | 0% | 2.9 | 0.12 | 0.087 | 4.1 | 0% / 1% | 24% / 13% |
| both_hands | both | 32 | 97% | 0% | 2.8 | 0.24 | 0.202 | 4.7 | 1% / 1% | 18% / 8% |
| hand_1 | ccw | 16 | 100% | 0% | 2.6 | 0.14 | 0.100 | 4.3 | 1% / 0% | 18% / 10% |
| hand_1 | cw | 16 | 94% | 0% | 2.9 | 0.12 | 0.095 | 4.0 | 0% / 0% | 23% / 14% |
| hand_1 | both | 32 | 97% | 0% | 2.7 | 0.12 | 0.095 | 4.0 | 0% / 0% | 21% / 12% |
| hand_2 | ccw | 16 | 100% | 0% | 2.7 | 0.44 | 0.437 | 6.8 | 0% / 7% | 9% / 8% |
| hand_2 | cw | 16 | 94% | 0% | 3.0 | 0.12 | 0.091 | 1.7 | 0% / 1% | 23% / 13% |
| hand_2 | both | 32 | 97% | 0% | 2.8 | 0.17 | 0.150 | 3.2 | 0% / 4% | 16% / 10% |
| stowed | ccw | 16 | 100% | 0% | 2.7 | 0.10 | 0.096 | 3.1 | 0% / 0% | 18% / 13% |
| stowed | cw | 16 | 100% | 0% | 3.0 | 0.11 | 0.094 | 3.5 | 0% / 0% | 21% / 13% |
| stowed | both | 32 | 100% | 0% | 2.8 | 0.10 | 0.094 | 3.1 | 0% / 0% | 20% / 13% |
| solo_1 | ccw | 16 | 0% | 0% | nan | 0.33 | 0.334 | 44.9 | 0% / 0% | 13% / 0% |
| solo_1 | cw | 16 | 0% | 0% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 0% |
| solo_1 | both | 32 | 0% | 0% | nan | 0.03 | 0.026 | 40.0 | 0% / 0% | 7% / 0% |
| solo_2 | ccw | 16 | 0% | 0% | nan | 0.49 | 0.486 | 40.0 | 0% / 0% | 0% / 0% |
| solo_2 | cw | 16 | 0% | 0% | nan | 0.01 | 0.009 | 40.0 | 0% / 0% | 0% / 0% |
| solo_2 | both | 32 | 0% | 0% | nan | 0.01 | 0.009 | 40.0 | 0% / 0% | 0% / 0% |
