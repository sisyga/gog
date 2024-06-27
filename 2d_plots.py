import string
from pickle import load
import numpy as np
import matplotlib.pyplot as plt
import string
from plot_funcs import label_axes
figsize = 7.086614, 8.858268

# %%
lgca1 = load(open('r_d_0.2_theta_0.2_lgca.pkl', 'rb'))

# %%
capacity = lgca1.interaction_params['capacity']
resting = lgca1.channel_pop[..., -1]
moving = lgca1.cell_density - resting
resting = resting[lgca1.nonborder]
moving = moving[lgca1.nonborder]
# %%
lgca1.plot_density(cbar=True, vmax=capacity, cmap='hot_r')
plt.yticks(ticks=np.arange(0, lgca1.dims[1], 50), labels=np.arange(0, lgca1.dims[1], 50))
plt.title('Total cell density')
# plt.savefig('total_cell_density_attractive_regime.png', dpi=300)
plt.show()
# %%
fig, _, _ = lgca1.plot_density(cbar=True, vmax=capacity, channels=[0, 1, 2, 3, 4, 5], cmap='Reds')
plt.yticks(ticks=np.arange(0, lgca1.dims[1], 50), labels=np.arange(0, lgca1.dims[1], 50))
plt.title('Cell density of migrating cells')
# plt.savefig('migrating_cells_attractive_regime.png', dpi=300)
plt.show()

# %%
fig, _, _ = lgca1.plot_density(cbar=True, vmax=capacity, channels=[-1], cmap='Blues')
plt.yticks(ticks=np.arange(0, lgca1.dims[1], 50), labels=np.arange(0, lgca1.dims[1], 50))
plt.title('Cell density of resting cells')
# plt.savefig('resting_cells_attractive_regime.png', dpi=300)
plt.show()
# %%
lgca1.plot_prop_spatial(vmin=-5, vmax=5, cmap='coolwarm')
plt.yticks(ticks=np.arange(0, lgca1.dims[1], 50), labels=np.arange(0, lgca1.dims[1], 50))
plt.title('Local switch parameter')
# plt.savefig('local_switch_parameter_attractive_regime.png', dpi=300)
plt.show()
# %%
# plt.hist(lgca.get_prop())
# plt.show()
# %%
fig, axes = plt.subplots(2, 2, sharex=True, sharey=True, figsize=figsize)

plt.sca(axes[0, 0])
lgca1.plot_scalarfield(lgca1.cell_density, cbar=True, cmap='hot_r', vmin=0, vmax=capacity, cbarlabel=None)
# lgca1.plot_density(cbar=True, vmax=capacity, cmap='hot_r')
plt.yticks(ticks=np.arange(0, lgca1.dims[1], 50), labels=np.arange(0, lgca1.dims[1], 50))
plt.title('Total cell density')
plt.xlabel('')
plt.sca(axes[0, 1])

lgca1.plot_scalarfield(moving, cbar=True, cmap='Reds', vmin=0, vmax=capacity, mask=moving == 0, cbarlabel=None)
# lgca1.plot_density(cbar=True, vmax=capacity, channels=[0, 1, 2, 3, 4, 5], cmap='Reds')
plt.yticks(ticks=np.arange(0, lgca1.dims[1], 50), labels=np.arange(0, lgca1.dims[1], 50))
plt.title('Migrating cells')
plt.ylabel('')
plt.xlabel('')

plt.sca(axes[1, 0])
lgca1.plot_scalarfield(resting, cbar=True, cmap='Blues', vmin=0, vmax=capacity, mask=resting==0, cbarlabel=None)
# lgca1.plot_density(cbar=True, vmax=capacity, channels=[-1], cmap='Blues')
plt.yticks(ticks=np.arange(0, lgca1.dims[1], 50), labels=np.arange(0, lgca1.dims[1], 50))
plt.title('Proliferating cells')

plt.sca(axes[1, 1])
lgca1.plot_prop_spatial(vmin=-5, vmax=5, cmap='coolwarm', cbarlabel=None)
plt.yticks(ticks=np.arange(0, lgca1.dims[1], 50), labels=np.arange(0, lgca1.dims[1], 50))
plt.title('Switch parameter')
# add suptitle in bold and big font
plt.suptitle('Cell death, high switch threshold', fontsize=12, fontweight='bold')
label_axes(axes.flat, fontsize=10, usetex=False, labels=string.ascii_uppercase)
# plt.savefig('repelling_regime.png', dpi=300)
# plt.savefig('repelling_regime.eps', dpi=300)
plt.show()

# %%
anim = lgca1.animate_density(vmax=capacity, cmap='hot_r', interval=10)
plt.yticks(ticks=np.arange(0, lgca1.dims[1], 50), labels=np.arange(0, lgca1.dims[1], 50))
plt.suptitle('Cell death, low switch threshold')
# anim.save('attractive_regime.mp4', dpi=300, bitrate=-1, fps=24)
plt.show()

# %%
from matplotlib import animation

# %%
fig, pc, cmap = lgca1.plot_prop_spatial(lgca1.nodes_t[0], vmin=-5, vmax=5, cmap='coolwarm', cbarlabel='Switch parameter')
title = plt.title('Time $k =$0')
plt.yticks(ticks=np.arange(0, lgca1.dims[1], 50), labels=np.arange(0, lgca1.dims[1], 50))

def update(n):
    title.set_text('Time $k =${}'.format(n))
    pc.set(facecolor=cmap.to_rgba(lgca1.mean_prop_t['kappa'][n, ...].ravel()), alpha=np.heaviside(lgca1.dens_t[n, ...].ravel(), 0), edgecolor='none')
    # pc.set(alpha=np.heaviside(lgca1.dens_t[n, ...].ravel(), 0))
    return pc, title


ani = animation.FuncAnimation(fig, update, interval=10, frames=lgca1.dens_t.shape[0], repeat=True)
plt.suptitle('Cell death, low switch threshold')
anim.save('attractive_regime_kappa.mp4', dpi=300, bitrate=-1, fps=24)
plt.show()

