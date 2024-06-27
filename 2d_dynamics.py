from pickle import dump
from lgca import get_lgca
import numpy as np

lx = 250
ly = round(lx * 1.1547)  # distance in y direction is smaller than in x direction
ly += 1 if ly % 2 == 1 else 0
dims = lx, ly
capacity = 50
tmax = 300
restchannels = 1
kappa_max = 4
kappa_std = 0.05 * kappa_max
params = [{'r_d': 0.2, 'theta': 0.9}, {'r_d': 0.2, 'theta': 0.2}, {'r_d': 0., 'theta': 0.5}]
for param in params:
    r_d = param['r_d']
    theta = param['theta']
    nodes = np.zeros(dims + (6 + restchannels,), dtype=int)
    nodes[lx // 2, ly // 2, -1] = capacity
    kappa = np.random.random(capacity) * kappa_max * 2 - kappa_max
    lgca = get_lgca(geometry='hx', dims=dims, interaction='go_or_grow_kappa', ve=False, ib=True, bc='reflect', restchannels=1,
                r_b=1., capacity=capacity, nodes=nodes, kappa=kappa, kappa_std=kappa_std, r_d=r_d, theta=theta)
    lgca.timeevo(tmax, record=True)
    with open(f'r_d_{r_d}_theta_{theta}_lgca.pkl', 'wb') as f:
        dump(lgca, f)

    del lgca


