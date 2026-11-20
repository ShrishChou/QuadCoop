# Comparison: Single robot, IPPO, MAPPO, Contact planner

Same protocol for every system: the same objects, start positions, masses and seed, 10 trials per case. Success = 10 cm / 6 deg held 1 s within 80 s; time = mean seconds to success over successful trials (n).

## By mass

| mass | Single robot success | Single robot time (s) | Single robot fell | IPPO success | IPPO time (s) | IPPO fell | MAPPO success | MAPPO time (s) | MAPPO fell | Contact planner success | Contact planner time (s) | Contact planner fell |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 89% | 18.6 (n 427) | 1% | 90% | 18.0 (n 431) | 5% | 90% | 20.8 (n 433) | 4% | 72% | 28.7 (n 348) | 2% |
| 40 kg | 64% | 30.8 (n 309) | 6% | 82% | 23.4 (n 396) | 8% | 78% | 24.9 (n 375) | 11% | 67% | 33.2 (n 323) | 4% |
| 60 kg | 25% | 37.9 (n 121) | 15% | 53% | 36.2 (n 255) | 24% | 53% | 34.7 (n 255) | 22% | 50% | 37.8 (n 238) | 8% |
| 80 kg | 11% | 19.0 (n 52) | 16% | 24% | 36.0 (n 113) | 26% | 24% | 36.0 (n 115) | 27% | 33% | 41.3 (n 159) | 17% |

Overall: Single robot 47% success, 25.3 s; IPPO 62% success, 25.4 s; MAPPO 61% success, 26.6 s; Contact planner 56% success, 34.0 s.

## 20 kg: by object (success / mean time)

| object | Single robot | IPPO | MAPPO | Contact planner |
|---|---|---|---|---|
| cube | 100% / 11.1 s | 98% / 11.7 s | 100% / 13.2 s | 90% / 18.0 s |
| long | 100% / 16.3 s | 98% / 14.9 s | 100% / 16.8 s | 88% / 26.1 s |
| sphere | 100% / 9.7 s | 92% / 12.4 s | 95% / 22.5 s | 100% / 18.5 s |
| cylinder | 60% / 18.9 s | 62% / 16.8 s | 65% / 17.9 s | 42% / 29.5 s |
| arch | 57% / 30.9 s | 55% / 30.8 s | 72% / 32.9 s | 92% / 28.3 s |
| dumbbell | 95% / 15.8 s | 100% / 20.1 s | 100% / 21.0 s | 68% / 31.0 s |
| t_shape | 100% / 15.7 s | 98% / 13.9 s | 98% / 17.2 s | 65% / 36.4 s |
| beam | 80% / 27.1 s | 95% / 29.2 s | 78% / 32.9 s | 52% / 34.2 s |
| l_shape | 100% / 16.5 s | 100% / 14.7 s | 95% / 16.2 s | 72% / 36.4 s |
| asym | 98% / 18.0 s | 95% / 14.4 s | 92% / 16.3 s | 50% / 30.7 s |
| u_channel | 100% / 18.1 s | 100% / 17.9 s | 100% / 19.8 s | 88% / 30.0 s |
| plus | 78% / 35.7 s | 85% / 25.6 s | 88% / 28.1 s | 62% / 36.6 s |

## 40 kg: by object (success / mean time)

| object | Single robot | IPPO | MAPPO | Contact planner |
|---|---|---|---|---|
| cube | 98% / 22.3 s | 98% / 19.2 s | 92% / 20.3 s | 90% / 24.3 s |
| long | 90% / 31.7 s | 100% / 18.8 s | 100% / 21.5 s | 75% / 33.8 s |
| sphere | 100% / 10.3 s | 90% / 11.7 s | 92% / 17.6 s | 95% / 14.1 s |
| cylinder | 65% / 25.2 s | 68% / 18.7 s | 50% / 16.5 s | 32% / 41.6 s |
| arch | 38% / 41.5 s | 52% / 41.4 s | 57% / 44.2 s | 92% / 29.6 s |
| dumbbell | 48% / 29.3 s | 82% / 24.8 s | 65% / 23.6 s | 65% / 37.9 s |
| t_shape | 85% / 35.1 s | 98% / 19.8 s | 95% / 19.8 s | 70% / 37.8 s |
| beam | 28% / 46.8 s | 68% / 33.2 s | 52% / 42.5 s | 35% / 34.6 s |
| l_shape | 82% / 33.8 s | 95% / 24.8 s | 95% / 21.1 s | 82% / 41.5 s |
| asym | 12% / 72.2 s | 68% / 31.6 s | 65% / 27.9 s | 28% / 58.4 s |
| u_channel | 80% / 36.8 s | 98% / 21.4 s | 92% / 24.6 s | 75% / 31.1 s |
| plus | 48% / 46.8 s | 75% / 28.8 s | 80% / 32.6 s | 68% / 44.5 s |

## 60 kg: by object (success / mean time)

| object | Single robot | IPPO | MAPPO | Contact planner |
|---|---|---|---|---|
| cube | 55% / 53.2 s | 55% / 46.7 s | 57% / 41.0 s | 65% / 40.2 s |
| long | 25% / 59.2 s | 70% / 35.1 s | 75% / 33.1 s | 60% / 46.3 s |
| sphere | 98% / 11.5 s | 90% / 11.5 s | 92% / 14.8 s | 98% / 15.9 s |
| cylinder | 38% / 31.4 s | 30% / 32.4 s | 35% / 20.7 s | 32% / 29.7 s |
| arch | 18% / 48.9 s | 28% / 51.7 s | 18% / 52.0 s | 72% / 40.7 s |
| dumbbell | 10% / 65.4 s | 45% / 29.2 s | 52% / 29.3 s | 65% / 40.7 s |
| t_shape | 20% / 49.3 s | 72% / 42.6 s | 78% / 41.5 s | 65% / 44.8 s |
| beam | 0% | 15% / 41.9 s | 15% / 33.3 s | 2% / 41.6 s |
| l_shape | 25% / 56.7 s | 65% / 41.1 s | 78% / 39.0 s | 42% / 40.4 s |
| asym | 0% | 38% / 50.6 s | 32% / 50.6 s | 10% / 58.3 s |
| u_channel | 5% / 59.9 s | 78% / 39.4 s | 57% / 44.8 s | 52% / 38.0 s |
| plus | 10% / 55.7 s | 52% / 37.9 s | 48% / 37.9 s | 30% / 55.1 s |

## 80 kg: by object (success / mean time)

| object | Single robot | IPPO | MAPPO | Contact planner |
|---|---|---|---|---|
| cube | 5% / 78.5 s | 10% / 38.9 s | 12% / 48.0 s | 12% / 52.0 s |
| long | 0% | 35% / 52.4 s | 42% / 50.0 s | 45% / 46.7 s |
| sphere | 95% / 13.2 s | 95% / 11.6 s | 95% / 13.9 s | 95% / 13.0 s |
| cylinder | 25% / 18.3 s | 30% / 19.6 s | 28% / 19.3 s | 28% / 39.9 s |
| arch | 2% / 75.5 s | 8% / 66.8 s | 2% / 68.5 s | 50% / 54.0 s |
| dumbbell | 0% | 15% / 48.6 s | 15% / 56.6 s | 30% / 51.1 s |
| t_shape | 2% / 71.0 s | 28% / 64.0 s | 20% / 56.2 s | 35% / 53.1 s |
| beam | 0% | 2% / 61.7 s | 0% | 0% |
| l_shape | 0% | 12% / 46.1 s | 28% / 56.2 s | 25% / 39.5 s |
| asym | 0% | 5% / 68.6 s | 2% / 70.9 s | 0% |
| u_channel | 0% | 10% / 59.0 s | 15% / 44.3 s | 40% / 50.9 s |
| plus | 0% | 32% / 49.4 s | 28% / 45.0 s | 38% / 59.3 s |

