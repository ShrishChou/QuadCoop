# Turn in place, MAPPO it 2000 (stowed) logs/marl2/sa_turn_stowed_s1/model_2000.pt: +-40 deg, 20 kg long object

8 placements per direction x swap, horizon 20 s, seed 7200. Success: centre < 0.1 m and heading < 6 deg held 1 s.

| condition | turn | episodes | success | falls | time to success, median s | largest centre drift, median m | end centre error, median m | end heading error, median abs deg | hand contact (robot 1 / 2) | trunk contact (1 / 2) |
|---|---|---|---|---|---|---|---|---|---|---|
| stowed | ccw | 16 | 94% | 0% | 2.7 | 0.28 | 0.196 | 8.8 | 0% / 0% | 1% / 3% |
| stowed | cw | 16 | 94% | 0% | 4.6 | 0.34 | 0.344 | 12.1 | 0% / 0% | 3% / 4% |
| stowed | both | 32 | 94% | 0% | 4.5 | 0.31 | 0.284 | 10.1 | 0% / 0% | 2% / 3% |
| solo_1 | ccw | 16 | 0% | 0% | nan | 0.08 | 0.076 | 44.8 | 0% / 0% | 0% / 0% |
| solo_1 | cw | 16 | 0% | 0% | nan | 0.04 | 0.037 | 40.0 | 0% / 0% | 0% / 0% |
| solo_1 | both | 32 | 0% | 0% | nan | 0.04 | 0.037 | 40.0 | 0% / 0% | 0% / 0% |
| solo_2 | ccw | 16 | 0% | 0% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 0% |
| solo_2 | cw | 16 | 0% | 0% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 0% |
| solo_2 | both | 32 | 0% | 0% | nan | 0.00 | 0.000 | 40.0 | 0% / 0% | 0% / 0% |
