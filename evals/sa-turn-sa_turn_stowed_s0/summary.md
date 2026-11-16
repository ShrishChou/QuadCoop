# Turn in place, MAPPO it 2000 (stowed) logs/marl2/sa_turn_stowed_s0/model_2000.pt: +-40 deg, 20 kg long object

8 placements per direction x swap, horizon 20 s, seed 7200. Success: centre < 0.1 m and heading < 6 deg held 1 s.

| condition | turn | episodes | success | falls | time to success, median s | largest centre drift, median m | end centre error, median m | end heading error, median abs deg | hand contact (robot 1 / 2) | trunk contact (1 / 2) |
|---|---|---|---|---|---|---|---|---|---|---|
| stowed | ccw | 16 | 100% | 6% | 2.7 | 0.15 | 0.148 | 5.4 | 0% / 0% | 35% / 39% |
| stowed | cw | 16 | 100% | 0% | 2.8 | 0.60 | 0.596 | 19.2 | 0% / 0% | 0% / 2% |
| stowed | both | 32 | 100% | 3% | 2.8 | 0.51 | 0.513 | 7.3 | 0% / 0% | 18% / 20% |
| solo_1 | ccw | 16 | 0% | 0% | nan | 0.69 | 0.693 | 40.0 | 0% / 0% | 0% / 0% |
| solo_1 | cw | 16 | 0% | 0% | nan | 0.34 | 0.335 | 40.0 | 0% / 0% | 0% / 0% |
| solo_1 | both | 32 | 0% | 0% | nan | 0.34 | 0.335 | 40.0 | 0% / 0% | 0% / 0% |
| solo_2 | ccw | 16 | 0% | 0% | nan | 0.04 | 0.037 | 40.0 | 0% / 0% | 0% / 0% |
| solo_2 | cw | 16 | 0% | 0% | nan | 0.30 | 0.298 | 40.0 | 0% / 0% | 0% / 30% |
| solo_2 | both | 32 | 0% | 0% | nan | 0.05 | 0.047 | 40.0 | 0% / 0% | 0% / 15% |
