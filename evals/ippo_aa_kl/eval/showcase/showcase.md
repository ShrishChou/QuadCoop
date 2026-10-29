# Two-robot showcase: ippo_aa_kl

policy: checkpoint logs/marl2/ippo_aa_kl_s0/model_3000.pt (iteration 3000, ippo, pair anymal)

Each cell: scenarios A / B / C / D as successful attempts out of 3 (S = filmed success, F = all 3 failed).

| object | 40 kg | 60 kg | 80 kg |
|---|---|---|---|
| cube | 3S / 3S / 3S / 3S | 2S / 1S / 2S / 0F | 1S / 0F / 1S / 0F |
| long | 3S / 2S / 3S / 3S | 3S / 2S / 2S / 2S | 3S / 0F / 0F / 0F |
| sphere | 3S / 2S / 2S / 3S | 3S / 3S / 3S / 3S | 3S / 3S / 2S / 3S |
| cylinder | 2S / 2S / 3S / 0F | 2S / 2S / 1S / 0F | 2S / 0F / 0F / 0F |
| arch | 1S / 1S / 2S / 0F | 0F / 0F / 2S / 0F | 0F / 0F / 0F / 0F |
| dumbbell | 3S / 3S / 2S / 3S | 1S / 2S / 2S / 2S | 0F / 0F / 0F / 0F |
| t_shape | 3S / 3S / 3S / 3S | 1S / 2S / 1S / 1S | 0F / 0F / 0F / 0F |
| beam (unseen) | 3S / 1S / 1S / 3S | 1S / 0F / 0F / 0F | 0F / 0F / 0F / 0F |
| l_shape (unseen) | 3S / 3S / 2S / 2S | 3S / 0F / 1S / 0F | 1S / 0F / 0F / 1S |
| asym (unseen) | 3S / 3S / 1S / 3S | 3S / 2S / 1S / 0F | 0F / 0F / 0F / 0F |
| u_channel (unseen) | 2S / 3S / 3S / 3S | 3S / 3S / 3S / 0F | 1S / 0F / 0F / 0F |
| plus (unseen) | 3S / 2S / 1S / 1S | 3S / 1S / 0F / 1S | 2S / 0F / 0F / 0F |

Succeeded (any attempt): 40 kg 46/48, 60 kg 35/48, 80 kg 12/48
