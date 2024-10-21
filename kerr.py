import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

M = 1.0
a_initial = 0.5

def kerr_surfaces(M, a, theta):
    if a > M:
        a = M
    r_plus = M + np.sqrt(M**2 - a**2)
    r_minus = M - np.sqrt(M**2 - a**2)
    r_static = 2 * M * np.ones_like(theta)
    r_ergosphere = M + np.sqrt(M**2 - a**2 * np.cos(theta)**2)
    return r_plus, r_minus, r_static, r_ergosphere

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.1, bottom=0.25)

phi = np.linspace(0, 2 * np.pi, 100)
theta = np.linspace(0, np.pi, 100)
theta, phi = np.meshgrid(theta, phi)

def update(a):
    ax.clear()
    r_plus, r_minus, r_static, r_ergosphere = kerr_surfaces(M, a, theta)
    
    # Convertir en coordonnées cartésiennes pour la visualisation
    x_ergosphere = r_ergosphere * np.sin(theta) * np.cos(phi)
    y_ergosphere = r_ergosphere * np.sin(theta) * np.sin(phi)
    z_ergosphere = r_ergosphere * np.cos(theta)
    
    x_horizon_plus = r_plus * np.sin(theta) * np.cos(phi)
    y_horizon_plus = r_plus * np.sin(theta) * np.sin(phi)
    z_horizon_plus = r_plus * np.cos(theta)
    
    x_horizon_minus = r_minus * np.sin(theta) * np.cos(phi)
    y_horizon_minus = r_minus * np.sin(theta) * np.sin(phi)
    z_horizon_minus = r_minus * np.cos(theta)
    
    x_static = r_static * np.sin(theta) * np.cos(phi)
    y_static = r_static * np.sin(theta) * np.sin(phi)
    z_static = r_static * np.cos(theta)
    
    # Appliquer une découpe le long de l'axe Y pour visualiser l'intérieur
    cut = (phi > np.pi / 2) & (phi < 3 * np.pi / 2)
    
    # Limite statique
    ax.plot_surface(x_static[~cut], y_static[~cut], z_static[~cut], color='blue', alpha=0.3, label='Limite statique')
    
    # Ergospère
    ax.plot_surface(x_ergosphere[~cut], y_ergosphere[~cut], z_ergosphere[~cut], color='red', alpha=0.2, label='Ergosphère')
    
    # Horizon extérieur
    ax.plot_surface(x_horizon_plus[~cut], y_horizon_plus[~cut], z_horizon_plus[~cut], color='black', alpha=0.8, label='Horizon extérieur')
    
    # Horizon intérieur (si r_minus > 0)
    if r_minus > 0:
        ax.plot_surface(x_horizon_minus[~cut], y_horizon_minus[~cut], z_horizon_minus[~cut], color='gray', alpha=0.5, label='Horizon intérieur')
    
    # Singularité en anneau
    phi_ring = np.linspace(0, 2 * np.pi, 100)
    x_ring = a * np.cos(phi_ring)
    y_ring = a * np.sin(phi_ring)
    z_ring = np.zeros_like(phi_ring)
    ax.plot(x_ring, y_ring, z_ring, color='red', linewidth=2, label='Singularité en anneau')
    
    # Configuration du plot
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Trou noir de Kerr (a = {a:.2f} M)')
    ax.set_box_aspect([1, 1, 1])
    ax.legend(loc='upper right')
    plt.draw()

update(a_initial)

ax_slider = plt.axes([0.1, 0.1, 0.8, 0.03])
slider_a = Slider(
    ax=ax_slider,
    label='Paramètre de rotation a',
    valmin=0.0,
    valmax=M,
    valinit=a_initial,
    valstep=0.01,
    color='green'
)

def on_change(val):
    update(slider_a.val)

slider_a.on_changed(on_change)

plt.show()
