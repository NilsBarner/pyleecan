"""Draw a zig-zag line based on a starting and end point and other custom settings."""

__all__ = ["draw_zigzag"]

import numpy as np
import matplotlib.pyplot as plt

def draw_zigzag(ax, start, end, pitch=0.1, fraction_zigzag=0.5, amplitude=0.1, color='black'):
    """
    Draws a connection between two points with a central zigzag (spring-like) region.
    The zigzag pattern has a user-defined pitch (distance between successive peaks),
    and the number of half-cycles is the largest integer that fits within the central
    zigzag region (a fraction of the total distance).
    
    Parameters:
      ax             : The matplotlib axis to draw on.
      x_start, y_start: Coordinates of the start point.
      x_end, y_end    : Coordinates of the end point.
      pitch           : Desired distance between subsequent zig or zag peaks.
      fraction_zigzag : Fraction of the total connection length that will be zigzagged.
                        (E.g., 0.5 means the inner 50% is zigzagged, leaving 25% straight at each end.)
      amplitude       : Maximum perpendicular displacement for the zigzag peaks.
    """
    x_start, y_start = start
    x_end, y_end = end
    
    # Overall displacement and length.
    dx = x_end - x_start
    dy = y_end - y_start
    L_total = np.hypot(dx, dy)
    
    # Determine the straight portions at each end.
    straight_frac = (1 - fraction_zigzag) / 2.0
    # Coordinates for the start and end of the zigzag region.
    p_zig_start = (x_start + straight_frac * dx, y_start + straight_frac * dy)
    p_zig_end   = (x_start + (1 - straight_frac) * dx, y_start + (1 - straight_frac) * dy)
    
    # Length of the zigzag region.
    L_zig = np.hypot(p_zig_end[0] - p_zig_start[0], p_zig_end[1] - p_zig_start[1])
    
    # Calculate the number of half-cycles (i.e. peaks) that fit within the zigzag region.
    n_half = int(np.floor(L_zig / pitch))
    if n_half < 1:
        n_half = 1  # Ensure at least one half-cycle.
    
    # Number of points along the zigzag region is n_half + 1.
    num_points_zig = n_half + 1
    t = np.linspace(0, 1, num_points_zig)
    
    # Baseline coordinates along the zigzag region.
    x_zig = p_zig_start[0] + t * (p_zig_end[0] - p_zig_start[0])
    y_zig = p_zig_start[1] + t * (p_zig_end[1] - p_zig_start[1])
    
    # Compute the normalized perpendicular vector.
    if L_total == 0:
        return
    perp_x = -dy / L_total
    perp_y = dx / L_total
    
    # For each odd-indexed point, add a perpendicular displacement.
    for i in range(num_points_zig):
        if i % 2 == 1:
            # Alternate the displacement sign.
            sign = 1 if ((i // 2) % 2 == 0) else -1
            x_zig[i] += amplitude * sign * perp_x
            y_zig[i] += amplitude * sign * perp_y
    
    # Create left (start) and right (end) straight segments.
    num_straight = 5  # Number of sample points for the straight portions.
    left_t = np.linspace(0, 1, num_straight)
    x_left = x_start + left_t * (p_zig_start[0] - x_start)
    y_left = y_start + left_t * (p_zig_start[1] - y_start)
    
    right_t = np.linspace(0, 1, num_straight)
    x_right = p_zig_end[0] + right_t * (x_end - p_zig_end[0])
    y_right = p_zig_end[1] + right_t * (y_end - p_zig_end[1])
    
    # Concatenate segments (omit duplicate endpoints).
    x_full = np.concatenate([x_left[:-1], x_zig, x_right[1:]])
    y_full = np.concatenate([y_left[:-1], y_zig, y_right[1:]])
    
    ax.plot(x_full, y_full, color=color, linewidth=1.5)


if __name__ == "__main__":

    # --------------------------
    # Example usage:
    # --------------------------
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')

    # Test the function:
    # For a connection from (0,0) to (1,0), with a pitch of 0.1, inner 25% zigzagged, and amplitude of 0.05.
    draw_zigzag(ax, 0, 0, 1, 0, pitch=0.01, fraction_zigzag=0.5, amplitude=0.05)

    # Mark endpoints for clarity.
    ax.plot(0, 0, 'ro')
    ax.plot(1, 0, 'ro')

    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.2, 0.2)
    plt.title("Zigzag with Pitch-Controlled Peaks (Inner 25% Zigzagged)")
    plt.show()

    
    
    
    
