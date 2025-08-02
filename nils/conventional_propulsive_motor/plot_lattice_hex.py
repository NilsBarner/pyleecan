"""
This script plots the cross-section of the lattice heat exchanger described in
appendix C.2 and chapter 5 of high_PhDthesis_2023_techdemomegawattintegrmotordriveacprop_chen.
"""

__all__ = ["plot_lattice_hex"]

import numpy as np

def plot_lattice_hex(
    fig=None,
    ax=None,
    r_in=None,  # inner radius [m]
    r_out=None,  # outer radius [m]
    h=None,  # radial spacing (ring thickness) [m]
    w=None,  # desired arc width in each ring [m]
    d=None,  # mean strut thickness [m]
    angle_start=0,  # start angle (in radians)
    angle_end=2 * np.pi,  # end angle (in radians)
    alpha=1
) -> tuple([object, object]):
    
    # Ensure valid angle range
    if angle_start >= angle_end:
        raise ValueError("angle_start must be less than angle_end")
    
    # Prepare Radii
    num_rings = int(np.floor((r_out - r_in) / h))
    r_values = r_in + np.arange(num_rings + 1) * h
    if r_values[-1] < r_out:
        r_values = np.append(r_values, r_out)
    
    # Precompute angles for the limited section
    angles_fine = np.linspace(angle_start, angle_end, 300)
    
    for i in range(len(r_values) - 1):
        # Inner and outer radii for the current ring
        r1 = r_values[i]
        r2 = r_values[i + 1]
        r_mid = 0.5 * (r1 + r2)
        
        # Draw partial ring boundaries (arcs at r1 and r2)
        ax.plot(r1 * np.cos(angles_fine), r1 * np.sin(angles_fine), 'k-', linewidth=1, alpha=alpha)
        ax.plot(r2 * np.cos(angles_fine), r2 * np.sin(angles_fine), 'k-', linewidth=1, alpha=alpha)
        
        # Determine number of arcs based on the partial angle range
        dtheta_est = w / r_mid
        n_arc = int(np.floor((angle_end - angle_start) / dtheta_est))
        dtheta = (angle_end - angle_start) / n_arc
        
        # Compute radial division angles within the restricted range
        angles = np.linspace(angle_start, angle_end, n_arc, endpoint=False)
        
        # Compute endpoints for the radial lines
        x_lines = np.outer([r1, r2], np.cos(angles))
        y_lines = np.outer([r1, r2], np.sin(angles))
        
        # Draw radial lines
        ax.plot(x_lines, y_lines, 'k-', linewidth=1.0, alpha=alpha)
        
        # Draw the two boundary radii (to close the section)
        ax.plot([r1 * np.cos(angle_start), r2 * np.cos(angle_start)],
                [r1 * np.sin(angle_start), r2 * np.sin(angle_start)], 'k-', linewidth=1, alpha=alpha)
        
        ax.plot([r1 * np.cos(angle_end), r2 * np.cos(angle_end)],
                [r1 * np.sin(angle_end), r2 * np.sin(angle_end)], 'k-', linewidth=1, alpha=alpha)

    return fig, ax
