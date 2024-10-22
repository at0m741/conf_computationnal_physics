import numpy as np
import plotly.graph_objects as go

M = 1.0
a_initial = 0.5
epsilon = 1e-6  

def kerr_surfaces(M, a, theta, phi):
    if a > M:
        a = M
    r_plus = M + np.sqrt(M**2 - a**2)
    r_minus = M - np.sqrt(M**2 - a**2)
    r_static = 2 * M * np.ones_like(theta)
    r_ergosphere_outer = M + np.sqrt(M**2 - a**2 * np.cos(theta)**2)
    r_ergosphere_inner = M - np.sqrt(M**2 - a**2 * np.cos(theta)**2)
    r_redshift_surface = r_plus
    return r_plus, r_minus, r_static, r_ergosphere_outer, r_ergosphere_inner, r_redshift_surface

def generate_kerr_surface(a, resolution=75):
    theta = np.linspace(0, np.pi, resolution)
    phi = np.linspace(0, 2 * np.pi, resolution)
    theta, phi = np.meshgrid(theta, phi)

    r_plus, r_minus, r_static, r_ergosphere_outer, r_ergosphere_inner, r_redshift_surface = kerr_surfaces(M, a, theta, phi)
    
    x_ergosphere_outer = r_ergosphere_outer * np.sin(theta) * np.cos(phi)
    y_ergosphere_outer = r_ergosphere_outer * np.sin(theta) * np.sin(phi)
    z_ergosphere_outer = r_ergosphere_outer * np.cos(theta)
    
    x_ergosphere_inner = r_ergosphere_inner * np.sin(theta) * np.cos(phi)
    y_ergosphere_inner = r_ergosphere_inner * np.sin(theta) * np.sin(phi)
    z_ergosphere_inner = r_ergosphere_inner * np.cos(theta)

    x_horizon_plus = r_plus * np.sin(theta) * np.cos(phi)
    y_horizon_plus = r_plus * np.sin(theta) * np.sin(phi)
    z_horizon_plus = r_plus * np.cos(theta)

    if r_minus > 0:
        x_horizon_minus = r_minus * np.sin(theta) * np.cos(phi)
        y_horizon_minus = r_minus * np.sin(theta) * np.sin(phi)
        z_horizon_minus = r_minus * np.cos(theta)
    else:
        x_horizon_minus, y_horizon_minus, z_horizon_minus = None, None, None
    
    x_redshift_surface = r_redshift_surface * np.sin(theta) * np.cos(phi)
    y_redshift_surface = r_redshift_surface * np.sin(theta) * np.sin(phi)
    z_redshift_surface = r_redshift_surface * np.cos(theta)

    phi_ring = np.linspace(0, 2 * np.pi, resolution)
    x_ring = a * np.cos(phi_ring)
    y_ring = a * np.sin(phi_ring)
    z_ring = np.zeros_like(x_ring) + 0.01

    return (x_ergosphere_outer, y_ergosphere_outer, z_ergosphere_outer), (x_ergosphere_inner, y_ergosphere_inner, z_ergosphere_inner), (x_horizon_plus, y_horizon_plus, z_horizon_plus), (x_horizon_minus, y_horizon_minus, z_horizon_minus), (x_redshift_surface, y_redshift_surface, z_redshift_surface), (x_ring, y_ring, z_ring)

def create_3d_plot(a):
    (x_ergosphere_outer, y_ergosphere_outer, z_ergosphere_outer), (x_ergosphere_inner, y_ergosphere_inner, z_ergosphere_inner), (x_horizon_plus, y_horizon_plus, z_horizon_plus), (x_horizon_minus, y_horizon_minus, z_horizon_minus), (x_redshift_surface, y_redshift_surface, z_redshift_surface), (x_ring, y_ring, z_ring) = generate_kerr_surface(a)
    
    fig = go.Figure()
    
    fig.add_trace(go.Surface(x=x_ergosphere_outer, y=y_ergosphere_outer, z=z_ergosphere_outer, colorscale='reds', opacity=0.3))
    
    fig.add_trace(go.Surface(x=x_ergosphere_inner, y=y_ergosphere_inner, z=z_ergosphere_inner, colorscale='oranges', opacity=1.0))
    
    fig.add_trace(go.Surface(x=x_horizon_plus, y=y_horizon_plus, z=z_horizon_plus, colorscale='gray', opacity=0.5))
    
    if x_horizon_minus is not None:
        fig.add_trace(go.Surface(x=x_horizon_minus, y=y_horizon_minus, z=z_horizon_minus, colorscale='Blues', opacity=0.5))
    
    fig.add_trace(go.Surface(x=x_redshift_surface, y=y_redshift_surface, z=z_redshift_surface, colorscale='Greens', opacity=0.6))
    
    fig.add_trace(go.Scatter3d(x=x_ring, y=y_ring, z=z_ring, mode='lines', line=dict(color='red', width=10)))

    fig.update_layout(scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
        aspectratio=dict(x=1, y=1, z=1),
        camera=dict(eye=dict(x=1.25, y=1.25, z=1.25))
    ), title=f'Visualisation 3D du trou noir de Kerr (a = {a:.2f})', showlegend=False)
    
    return fig

def create_interactive_plot():
    fig = create_3d_plot(a_initial)
    
    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Paramètre de rotation a: "},
        pad={"t": 50},
        steps=[dict(method='animate', args=[[f'frame{int(i)}'], dict(mode='immediate', frame=dict(duration=0, redraw=True), transition=dict(duration=0))], label=f'{a:.2f}') for i, a in enumerate(np.linspace(0, M, 30))]
    )]

    fig.update_layout(sliders=sliders)

    frames = [go.Frame(name=f'frame{int(i)}', data=[
        go.Surface(z=generate_kerr_surface(a)[0][2], 
                   x=generate_kerr_surface(a)[0][0], 
                   y=generate_kerr_surface(a)[0][1], 
                   colorscale='reds', opacity=0.3),
        go.Surface(z=generate_kerr_surface(a)[1][2], 
                   x=generate_kerr_surface(a)[1][0], 
                   y=generate_kerr_surface(a)[1][1], 
                   colorscale='oranges', opacity=1.0),
        go.Surface(z=generate_kerr_surface(a)[2][2], 
                   x=generate_kerr_surface(a)[2][0], 
                   y=generate_kerr_surface(a)[2][1], 
                   colorscale='gray', opacity=0.5),
        go.Surface(z=generate_kerr_surface(a)[3][2], 
                   x=generate_kerr_surface(a)[3][0], 
                   y=generate_kerr_surface(a)[3][1], 
                   colorscale='Blues', opacity=0.5),
        go.Surface(z=generate_kerr_surface(a)[4][2], 
                   x=generate_kerr_surface(a)[4][0], 
                   y=generate_kerr_surface(a)[4][1], 
                   colorscale='Greens', opacity=0.6),
        go.Scatter3d(x=generate_kerr_surface(a)[5][0], 
                     y=generate_kerr_surface(a)[5][1], 
                     z=generate_kerr_surface(a)[5][2], 
                     mode='lines', line=dict(color='red', width=10))
    ]) for i, a in enumerate(np.linspace(0, M, 30))]

    fig.frames = frames

    fig.write_html('kerr_plot_interactive.html')
    return fig

create_interactive_plot()
import subprocess
subprocess.run(['flatpak', 'run', 'org.mozilla.firefox', 'kerr_plot_interactive.html'])
