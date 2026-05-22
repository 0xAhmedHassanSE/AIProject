"""
================================================================================
  visualization.py — Visualisation Suite for the RL Maze Solver
================================================================================
  Author  : Expert AI Researcher / Senior Python Developer
  Project : Maze Solver using Reinforcement Learning

  Description:
    Provides all matplotlib-based visualisation functions:

    1. plot_learning_curve()     — Rewards per Episode + smoothed trend
    2. plot_steps_reduction()    — Steps taken per Episode (efficiency gains)
    3. plot_epsilon_decay()      — Exploration rate decay over episodes
    4. plot_td_errors()          — Mean |TD error| per episode (convergence signal)
    5. plot_training_dashboard() — Combined 2×2 summary figure
    6. render_maze_path()        — Heatmap of maze + optimal path overlay
    7. render_q_value_heatmap()  — Max Q-value per cell (value function V*(s))

  Each function returns the matplotlib Figure so callers can save or display it.
================================================================================
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.gridspec import GridSpec
from typing import List, Optional, Tuple

# Use non-interactive backend by default so plots can be saved without a display
# matplotlib.use("Agg")


# ---------------------------------------------------------------------------
# Colour palette (consistent across all figures)
# ---------------------------------------------------------------------------
COLOURS = {
    "reward_raw"  : "#B0BEC5",   # light steel for raw noisy data
    "reward_smooth": "#1565C0",  # strong blue for smoothed line
    "steps_raw"   : "#FFCC80",   # soft orange raw
    "steps_smooth": "#E65100",   # deep orange smoothed
    "epsilon"     : "#7B1FA2",   # purple for epsilon
    "td_error"    : "#2E7D32",   # green for TD error
    "wall"        : "#37474F",   # dark slate for walls
    "free"        : "#ECEFF1",   # near-white for free cells
    "start"       : "#43A047",   # green for start
    "exit"        : "#E53935",   # red for exit
    "path"        : "#FDD835",   # yellow for path
    "path_arrow"  : "#F57F17",   # amber for arrows
}

FIGURE_DPI  = 150
FIGURE_FONT = "DejaVu Sans"


# ---------------------------------------------------------------------------
# Helper: smooth a 1-D list with a moving average
# ---------------------------------------------------------------------------

def _moving_avg(data: List[float], window: int) -> np.ndarray:
    """Return the centred moving average of `data` over `window` steps."""
    kernel = np.ones(window) / window
    return np.convolve(data, kernel, mode="same")


# ---------------------------------------------------------------------------
# 1. Learning Curve — Rewards per Episode
# ---------------------------------------------------------------------------

def plot_learning_curve(
    episode_rewards: List[float],
    window:          int = 50,
    title:           str = "Learning Curve — Reward per Episode",
    save_path:       Optional[str] = None,
) -> plt.Figure:
    """
    Plot the agent's total reward per episode alongside a smoothed trend line.

    The raw reward trace is noisy because of stochastic exploration.
    The smoothed line reveals the true learning trend.

    Parameters
    ----------
    episode_rewards : List of total reward per episode.
    window          : Smoothing window size (episodes).
    title           : Figure title.
    save_path       : If given, save the figure to this file path.

    Returns
    -------
    fig : matplotlib Figure.
    """
    episodes = np.arange(1, len(episode_rewards) + 1)
    smoothed  = _moving_avg(episode_rewards, window)

    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=FIGURE_DPI)

    # Raw rewards (faint background)
    ax.plot(
        episodes, episode_rewards,
        color=COLOURS["reward_raw"], linewidth=0.6,
        alpha=0.5, label="Raw reward"
    )

    # Smoothed trend
    ax.plot(
        episodes, smoothed,
        color=COLOURS["reward_smooth"], linewidth=2.2,
        label=f"Smoothed (window={window})"
    )

    # Reference line at 0
    ax.axhline(0, color="#90A4AE", linewidth=0.8, linestyle="--")

    ax.set_xlabel("Episode", fontsize=12)
    ax.set_ylabel("Total Reward", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=FIGURE_DPI, bbox_inches="tight")
        print(f"  [Saved] {save_path}")

    return fig


# ---------------------------------------------------------------------------
# 2. Step Reduction — Efficiency over Time
# ---------------------------------------------------------------------------

def plot_steps_reduction(
    episode_steps: List[int],
    window:        int = 50,
    title:         str = "Path Efficiency — Steps per Episode",
    save_path:     Optional[str] = None,
) -> plt.Figure:
    """
    Plot steps taken per episode.  A downward trend shows the agent is
    finding the exit more efficiently as it learns.

    Parameters
    ----------
    episode_steps : List of step counts per episode.
    window        : Smoothing window size.
    save_path     : Optional file path to save the figure.

    Returns
    -------
    fig : matplotlib Figure.
    """
    episodes = np.arange(1, len(episode_steps) + 1)
    smoothed  = _moving_avg(episode_steps, window)

    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=FIGURE_DPI)

    ax.plot(
        episodes, episode_steps,
        color=COLOURS["steps_raw"], linewidth=0.6,
        alpha=0.5, label="Raw steps"
    )
    ax.plot(
        episodes, smoothed,
        color=COLOURS["steps_smooth"], linewidth=2.2,
        label=f"Smoothed (window={window})"
    )

    # Annotate the minimum steps achieved
    best_ep  = int(np.argmin(episode_steps)) + 1
    best_val = min(episode_steps)
    ax.annotate(
        f"Best: {best_val} steps\n(ep {best_ep})",
        xy=(best_ep, best_val),
        xytext=(best_ep + len(episodes) * 0.04, best_val + max(episode_steps) * 0.06),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", color=COLOURS["steps_smooth"]),
        color=COLOURS["steps_smooth"],
    )

    ax.set_xlabel("Episode", fontsize=12)
    ax.set_ylabel("Steps Taken", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=FIGURE_DPI, bbox_inches="tight")
        print(f"  [Saved] {save_path}")

    return fig


# ---------------------------------------------------------------------------
# 3. Epsilon Decay
# ---------------------------------------------------------------------------

def plot_epsilon_decay(
    epsilon_history: List[float],
    title:           str = "Exploration Rate (ε) Decay over Episodes",
    save_path:       Optional[str] = None,
) -> plt.Figure:
    """
    Visualise how the exploration probability ε decays over training.

    The shaded regions illustrate the exploration (ε) and exploitation (1-ε)
    fractions at each episode.
    """
    episodes = np.arange(1, len(epsilon_history) + 1)
    eps      = np.array(epsilon_history)

    fig, ax = plt.subplots(figsize=(10, 4), dpi=FIGURE_DPI)

    # Shaded areas
    ax.fill_between(episodes, 0,    eps,   alpha=0.20, color=COLOURS["epsilon"], label="Explore region")
    ax.fill_between(episodes, eps,  1,     alpha=0.08, color=COLOURS["reward_smooth"], label="Exploit region")

    ax.plot(episodes, eps, color=COLOURS["epsilon"], linewidth=2.0, label="ε (epsilon)")

    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Episode", fontsize=12)
    ax.set_ylabel("ε (Exploration Probability)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=FIGURE_DPI, bbox_inches="tight")
        print(f"  [Saved] {save_path}")

    return fig


# ---------------------------------------------------------------------------
# 4. TD Error over Time (Convergence Diagnostic)
# ---------------------------------------------------------------------------

def plot_td_errors(
    td_errors:  List[float],
    window:     int = 50,
    title:      str = "Convergence — Mean |TD Error| per Episode",
    save_path:  Optional[str] = None,
) -> plt.Figure:
    """
    Plot mean absolute TD error per episode.

    The TD error δ = r + γ·maxQ(s',·) - Q(s,a) measures how surprised the
    agent is by each transition.  As Q converges, δ → 0.
    """
    episodes = np.arange(1, len(td_errors) + 1)
    smoothed  = _moving_avg(td_errors, window)

    fig, ax = plt.subplots(figsize=(10, 4), dpi=FIGURE_DPI)

    ax.semilogy(
        episodes, td_errors,
        color=COLOURS["td_error"], linewidth=0.5,
        alpha=0.4, label="Raw |TD error|"
    )
    # Smoothed on linear scale for clarity
    fig2, ax2 = plt.subplots()   # dummy for smoothed on same log axis
    plt.close(fig2)
    ax.semilogy(
        episodes, np.maximum(smoothed, 1e-8),
        color="#1B5E20", linewidth=2.2,
        label=f"Smoothed (window={window})"
    )

    ax.set_xlabel("Episode", fontsize=12)
    ax.set_ylabel("|TD Error| (log scale)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, which="both")
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=FIGURE_DPI, bbox_inches="tight")
        print(f"  [Saved] {save_path}")

    return fig


# ---------------------------------------------------------------------------
# 5. Combined Training Dashboard (2×2 grid)
# ---------------------------------------------------------------------------

def plot_training_dashboard(
    episode_rewards: List[float],
    episode_steps:   List[int],
    epsilon_history: List[float],
    td_errors:       List[float],
    window:          int = 50,
    save_path:       Optional[str] = None,
) -> plt.Figure:
    """
    Single combined figure with four panels:
        Top-left  : Learning Curve (Rewards)
        Top-right : Steps Reduction
        Bot-left  : ε Decay
        Bot-right : TD Error Convergence
    """
    fig = plt.figure(figsize=(16, 10), dpi=FIGURE_DPI)
    gs  = GridSpec(2, 2, figure=fig, hspace=0.38, wspace=0.3)

    episodes  = np.arange(1, len(episode_rewards) + 1)

    # ── Panel 1: Rewards ───────────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(episodes, episode_rewards, color=COLOURS["reward_raw"],
             linewidth=0.6, alpha=0.5, label="Raw")
    ax1.plot(episodes, _moving_avg(episode_rewards, window),
             color=COLOURS["reward_smooth"], linewidth=2.0,
             label=f"Smooth-{window}")
    ax1.axhline(0, color="#90A4AE", linewidth=0.7, linestyle="--")
    ax1.set_title("① Learning Curve (Reward / Episode)", fontweight="bold")
    ax1.set_xlabel("Episode")
    ax1.set_ylabel("Total Reward")
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.25)

    # ── Panel 2: Steps ─────────────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(episodes, episode_steps, color=COLOURS["steps_raw"],
             linewidth=0.6, alpha=0.5, label="Raw")
    ax2.plot(episodes, _moving_avg(episode_steps, window),
             color=COLOURS["steps_smooth"], linewidth=2.0,
             label=f"Smooth-{window}")
    ax2.set_title("② Path Efficiency (Steps / Episode)", fontweight="bold")
    ax2.set_xlabel("Episode")
    ax2.set_ylabel("Steps Taken")
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.25)

    # ── Panel 3: Epsilon ───────────────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 0])
    eps = np.array(epsilon_history)
    ax3.fill_between(episodes, 0, eps, alpha=0.20, color=COLOURS["epsilon"])
    ax3.plot(episodes, eps, color=COLOURS["epsilon"], linewidth=2.0)
    ax3.set_title("③ Exploration Rate ε Decay", fontweight="bold")
    ax3.set_xlabel("Episode")
    ax3.set_ylabel("ε")
    ax3.set_ylim(0, 1.05)
    ax3.grid(True, alpha=0.25)

    # ── Panel 4: TD Error ──────────────────────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.semilogy(episodes, td_errors, color=COLOURS["td_error"],
                 linewidth=0.5, alpha=0.4, label="Raw")
    ax4.semilogy(episodes, np.maximum(_moving_avg(td_errors, window), 1e-8),
                 color="#1B5E20", linewidth=2.0, label=f"Smooth-{window}")
    ax4.set_title("④ Convergence — Mean |TD Error|", fontweight="bold")
    ax4.set_xlabel("Episode")
    ax4.set_ylabel("|TD Error| (log scale)")
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.25, which="both")

    fig.suptitle(
        "Maze RL Solver — Q-Learning Training Dashboard",
        fontsize=16, fontweight="bold", y=0.96
    )
    fig.subplots_adjust(top=0.90)

    if save_path:
        fig.savefig(save_path, dpi=FIGURE_DPI)
        print(f"  [Saved] {save_path}")

    return fig


# ---------------------------------------------------------------------------
# 6. Maze Renderer with Optimal Path Overlay
# ---------------------------------------------------------------------------

def render_maze_path(
    maze:       np.ndarray,
    path:       List[Tuple[int, int]],
    start_pos:  Tuple[int, int],
    exit_pos:   Tuple[int, int],
    title:      str = "Maze — Agent's Optimal Path (Post-Training)",
    save_path:  Optional[str] = None,
) -> plt.Figure:
    """
    Render the maze grid with the learned optimal path overlaid.

    Visual encoding:
        ■ Dark grey  → Wall cell
        □ Off-white  → Free cell
        ★ Green      → Start position
        ★ Red        → Exit position
        ● Yellow     → Path cells
        → Amber arrows → Direction of travel

    Parameters
    ----------
    maze      : (n_rows, n_cols) numpy array (0=free, 1=wall).
    path      : Ordered list of (row, col) tuples from start to exit.
    start_pos : (row, col) of the start cell.
    exit_pos  : (row, col) of the exit cell.
    save_path : Optional file path to save the figure.
    """
    n_rows, n_cols = maze.shape

    # Build display grid: 0=free, 1=wall, 2=path, 3=start, 4=exit
    display = maze.astype(float)
    for (r, c) in path:
        display[r, c] = 0.5   # path cells get value 0.5

    # Custom colour map
    cmap = LinearSegmentedColormap.from_list(
        "maze",
        [
            (0.0, "#ECEFF1"),   # 0.0  → free cell (light grey)
            (0.5, "#FFF9C4"),   # 0.5  → path cell (pale yellow)
            (1.0, "#37474F"),   # 1.0  → wall      (dark slate)
        ]
    )

    fig, ax = plt.subplots(
        figsize=(max(7, n_cols * 0.7), max(7, n_rows * 0.7)),
        dpi=FIGURE_DPI
    )

    ax.imshow(display, cmap=cmap, vmin=0, vmax=1, interpolation="nearest")

    # ── Grid lines ────────────────────────────────────────────────────────
    for x in range(n_cols + 1):
        ax.axvline(x - 0.5, color="#B0BEC5", linewidth=0.4)
    for y in range(n_rows + 1):
        ax.axhline(y - 0.5, color="#B0BEC5", linewidth=0.4)

    # ── Path arrows ───────────────────────────────────────────────────────
    for i in range(len(path) - 1):
        r0, c0 = path[i]
        r1, c1 = path[i + 1]
        dr = r1 - r0
        dc = c1 - c0
        ax.annotate(
            "",
            xy     =(c1, r1),
            xytext =(c0, r0),
            arrowprops=dict(
                arrowstyle="-|>",
                color=COLOURS["path_arrow"],
                lw=1.8,
                mutation_scale=12,
            )
        )

    # ── Start & Exit markers ──────────────────────────────────────────────
    sr, sc = start_pos
    er, ec = exit_pos

    ax.text(sc, sr, "S", ha="center", va="center",
            fontsize=11, fontweight="bold", color=COLOURS["start"])
    ax.text(ec, er, "E", ha="center", va="center",
            fontsize=11, fontweight="bold", color=COLOURS["exit"])

    # ── Cell labels for path step numbers ────────────────────────────────
    for step_idx, (r, c) in enumerate(path):
        if (r, c) not in (start_pos, exit_pos):
            ax.text(c, r, str(step_idx), ha="center", va="center",
                    fontsize=5.5, color="#5D4037", alpha=0.7)

    # ── Legend ────────────────────────────────────────────────────────────
    legend_items = [
        mpatches.Patch(color="#37474F", label="Wall"),
        mpatches.Patch(color="#ECEFF1", label="Free cell"),
        mpatches.Patch(color="#FFF9C4", label="Path"),
        mpatches.Patch(color=COLOURS["start"], label="Start (S)"),
        mpatches.Patch(color=COLOURS["exit"],  label="Exit (E)"),
    ]
    ax.legend(
        handles=legend_items, loc="upper right",
        fontsize=8, framealpha=0.9,
        bbox_to_anchor=(1.18, 1.0)
    )

    ax.set_title(
        f"{title}\n"
        f"Path length: {len(path)-1} steps | "
        f"Start: {start_pos} → Exit: {exit_pos}",
        fontsize=12, fontweight="bold", pad=10
    )
    ax.set_xticks(range(n_cols))
    ax.set_yticks(range(n_rows))
    ax.set_xticklabels(range(n_cols), fontsize=7)
    ax.set_yticklabels(range(n_rows), fontsize=7)

    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=FIGURE_DPI, bbox_inches="tight")
        print(f"  [Saved] {save_path}")

    return fig


# ---------------------------------------------------------------------------
# 7. Q-Value Heatmap (Value Function V*(s))
# ---------------------------------------------------------------------------

def render_q_value_heatmap(
    q_table:    np.ndarray,
    maze:       np.ndarray,
    n_cols:     int,
    start_pos:  Tuple[int, int],
    exit_pos:   Tuple[int, int],
    title:      str = "Learned State Value Function  V*(s) = max_a Q(s,a)",
    save_path:  Optional[str] = None,
) -> plt.Figure:
    """
    Visualise the learned value function:
        V*(s) = max_a Q(s, a)

    High-value cells (warm colours) indicate states from which the agent
    believes it can reach the exit quickly.  The heatmap reveals the
    learned "gradient" guiding the agent toward the goal.

    Parameters
    ----------
    q_table   : (n_states, n_actions) Q-table array.
    maze      : (n_rows, n_cols) maze array.
    n_cols    : Number of columns (needed to reshape states → grid).
    """
    n_rows = maze.shape[0]
    n_states = n_rows * n_cols

    # Compute V*(s) = max_a Q(s,a)  for every state
    v_star = np.max(q_table, axis=1).reshape(n_rows, n_cols)

    # Mask walls: set them to NaN so they appear in a neutral colour
    mask = maze == 1
    v_star_masked = v_star.astype(float)
    v_star_masked[mask] = np.nan

    fig, ax = plt.subplots(
        figsize=(max(7, n_cols * 0.7), max(7, n_rows * 0.7)),
        dpi=FIGURE_DPI
    )

    im = ax.imshow(
        v_star_masked,
        cmap="RdYlGn",    # Red=low value, Green=high value
        interpolation="nearest",
        aspect="equal"
    )

    # Overlay wall hatching
    for r in range(n_rows):
        for c in range(n_cols):
            if maze[r, c] == 1:
                rect = plt.Rectangle(
                    (c - 0.5, r - 0.5), 1, 1,
                    color=COLOURS["wall"], zorder=2
                )
                ax.add_patch(rect)

    # Start & Exit labels
    sr, sc = start_pos
    er, ec = exit_pos
    ax.text(sc, sr, "S", ha="center", va="center",
            fontsize=12, fontweight="bold", color="white", zorder=3)
    ax.text(ec, er, "E", ha="center", va="center",
            fontsize=12, fontweight="bold", color="white", zorder=3)

    # Annotate each free cell with its V* value
    for r in range(n_rows):
        for c in range(n_cols):
            if maze[r, c] == 0:
                ax.text(c, r, f"{v_star[r,c]:.1f}",
                        ha="center", va="center",
                        fontsize=5, color="#1a1a1a", alpha=0.75)

    plt.colorbar(im, ax=ax, fraction=0.035, pad=0.04,
                 label="V*(s) = max_a Q(s,a)")
    ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
    ax.set_xticks(range(n_cols))
    ax.set_yticks(range(n_rows))
    ax.set_xticklabels(range(n_cols), fontsize=7)
    ax.set_yticklabels(range(n_rows), fontsize=7)

    # Grid
    for x in range(n_cols + 1):
        ax.axvline(x - 0.5, color="#B0BEC5", linewidth=0.3)
    for y in range(n_rows + 1):
        ax.axhline(y - 0.5, color="#B0BEC5", linewidth=0.3)

    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=FIGURE_DPI, bbox_inches="tight")
        print(f"  [Saved] {save_path}")

    return fig


# ---------------------------------------------------------------------------
# 8. Policy Arrow Map
# ---------------------------------------------------------------------------

def render_policy_map(
    q_table:    np.ndarray,
    maze:       np.ndarray,
    n_cols:     int,
    start_pos:  Tuple[int, int],
    exit_pos:   Tuple[int, int],
    title:      str = "Learned Policy — Greedy Action at Each Cell",
    save_path:  Optional[str] = None,
) -> plt.Figure:
    """
    Render an arrow at every free cell showing the greedy policy action.

    Arrow directions:
        ↑ Up    ↓ Down    ← Left    → Right
    """
    n_rows  = maze.shape[0]
    ARROW_DX = {0: 0,    1: 0,    2: -0.35, 3: 0.35}
    ARROW_DY = {0: -0.35, 1: 0.35, 2: 0,    3: 0   }

    fig, ax = plt.subplots(
        figsize=(max(7, n_cols * 0.7), max(7, n_rows * 0.7)),
        dpi=FIGURE_DPI
    )

    # Background: walls vs free
    bg = maze.astype(float)
    cmap_bg = LinearSegmentedColormap.from_list(
        "bg", [(0.0, "#FAFAFA"), (1.0, "#37474F")]
    )
    ax.imshow(bg, cmap=cmap_bg, vmin=0, vmax=1, interpolation="nearest")

    for r in range(n_rows):
        for c in range(n_cols):
            if maze[r, c] == 1:
                continue   # skip walls
            state   = r * n_cols + c
            best_a  = int(np.argmax(q_table[state]))
            dx = ARROW_DX[best_a]
            dy = ARROW_DY[best_a]
            ax.annotate(
                "",
                xy     =(c + dx, r + dy),
                xytext =(c - dx, r - dy),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color="#1565C0",
                    lw=1.5,
                    mutation_scale=10,
                )
            )

    # Start & Exit
    sr, sc = start_pos
    er, ec = exit_pos
    ax.add_patch(plt.Circle((sc, sr), 0.4, color=COLOURS["start"], zorder=3))
    ax.add_patch(plt.Circle((ec, er), 0.4, color=COLOURS["exit"],  zorder=3))
    ax.text(sc, sr, "S", ha="center", va="center",
            fontsize=9, fontweight="bold", color="white", zorder=4)
    ax.text(ec, er, "E", ha="center", va="center",
            fontsize=9, fontweight="bold", color="white", zorder=4)

    # Grid
    for x in range(n_cols + 1):
        ax.axvline(x - 0.5, color="#B0BEC5", linewidth=0.4)
    for y in range(n_rows + 1):
        ax.axhline(y - 0.5, color="#B0BEC5", linewidth=0.4)

    ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
    ax.set_xticks(range(n_cols))
    ax.set_yticks(range(n_rows))
    ax.set_xticklabels(range(n_cols), fontsize=7)
    ax.set_yticklabels(range(n_rows), fontsize=7)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=FIGURE_DPI, bbox_inches="tight")
        print(f"  [Saved] {save_path}")

    return fig
