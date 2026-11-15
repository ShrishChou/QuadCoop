# Turn in place, MAPPO it 0 (hand_rate) logs/marl2/sa_turnwire_bc_check/model_0.pt: +-40 deg, 20 kg long object

4 placements per direction x swap, horizon 20 s, seed 7200. Success: centre < 0.1 m and heading < 6 deg held 1 s.

| condition | turn | episodes | success | falls | time to success, median s | largest centre drift, median m | end centre error, median m | end heading error, median abs deg | hand contact (robot 1 / 2) | trunk contact (1 / 2) |
|---|---|---|---|---|---|---|---|---|---|---|
| both_hands | ccw | 8 | 100% | 0% | 10.2 | 0.10 | 0.096 | 7.7 | 66% / 82% | 0% / 0% |
| both_hands | cw | 8 | 38% | 0% | 11.8 | 0.20 | 0.198 | 13.6 | 66% / 83% | 4% / 9% |
| both_hands | both | 16 | 69% | 0% | 10.3 | 0.10 | 0.096 | 13.3 | 66% / 82% | 2% / 4% |
| hand_1 | ccw | 8 | 0% | 0% | nan | 0.20 | 0.203 | 22.0 | 82% / 0% | 0% / 0% |
| hand_1 | cw | 8 | 0% | 0% | nan | 0.22 | 0.219 | 21.0 | 84% / 0% | 0% / 0% |
| hand_1 | both | 16 | 0% | 0% | nan | 0.21 | 0.211 | 21.1 | 83% / 0% | 0% / 0% |
| hand_2 | ccw | 8 | 0% | 0% | nan | 0.24 | 0.239 | 18.2 | 0% / 83% | 0% / 0% |
| hand_2 | cw | 8 | 0% | 0% | nan | 0.31 | 0.309 | 10.7 | 0% / 84% | 20% / 0% |
| hand_2 | both | 16 | 0% | 0% | nan | 0.28 | 0.283 | 13.5 | 0% / 83% | 10% / 0% |
| stowed | ccw | 8 | 0% | 0% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 0% |
| stowed | cw | 8 | 0% | 0% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 0% |
| stowed | both | 16 | 0% | 0% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 0% |
| solo_1 | ccw | 8 | 0% | 0% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 0% |
| solo_1 | cw | 8 | 0% | 0% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 0% |
| solo_1 | both | 16 | 0% | 0% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 0% |
| solo_2 | ccw | 8 | 0% | 50% | nan | 0.91 | 0.908 | 62.9 | 0% / 4% | 0% / 12% |
| solo_2 | cw | 8 | 0% | 50% | nan | 0.47 | 0.469 | 38.1 | 0% / 20% | 0% / 9% |
| solo_2 | both | 16 | 0% | 50% | nan | 0.47 | 0.469 | 42.4 | 0% / 12% | 0% / 10% |
