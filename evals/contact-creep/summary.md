# Contact creep test: evals/contact-creep

45 kg block on four 3 cm sphere feet, foot friction 0.8, a steady horizontal push at a share of mu m g (353 N) for 3 s after settling. Creep = mean sliding speed (a rigid Coulomb contact: 0 below share 1, sliding above it). Sink = foot penetration at rest.

| contact settings | sink (mm) | push 10% of the limit (35 N): creep mm/s | push 50% of the limit (177 N): creep mm/s | push 90% of the limit (318 N): creep mm/s | push 110% of the limit (388 N): creep mm/s | push 150% of the limit (530 N): creep mm/s |
|---|---|---|---|---|---|---|
| walker env: solimp (0.015,1,0.03), pyramidal, impratio 1 | 9.4 | 12.0 | 64.5 | 396.7 | 1537.4 | 6009.7 |
| same, impratio 10 | 5.8 | 3.2 | 17.5 | 104.6 | 1524.4 | 5864.5 |
| same, elliptic, impratio 10 | 10.6 | 0.6 | 2.9 | 5.9 | 1059.0 | 5712.0 |
| MuJoCo default solimp (0.9,0.95,0.001), pyramidal, impratio 1 | 0.1 | 0.3 | 1.9 | 13.6 | 1053.4 | 5492.1 |
| default solimp, elliptic, impratio 10 | 0.1 | 0.0 | 0.1 | 0.3 | 1047.1 | 5625.4 |
