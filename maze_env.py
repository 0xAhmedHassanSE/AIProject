"""
================================================================================
  maze_env.py — Custom Gymnasium Maze Environment
================================================================================
  Author  : Expert AI Researcher / Senior Python Developer
  Project : Maze Solver using Reinforcement Learning
  
  Description:
    This module defines a fully custom OpenAI Gymnasium-compatible 2D maze
    environment.  The agent starts at the top-left cell and must find its way
    to the bottom-right exit using only reward signals — no map knowledge.

  Key RL Concepts Implemented Here:
    • State Space  : Every (row, col) grid cell is a unique integer state.
    • Action Space : Discrete(4) → 0=Up, 1=Down, 2=Left, 3=Right.
    • Reward Shaping: Carefully designed rewards guide learning speed:
        -1.0  per step        → agent prefers shorter paths
        -5.0  hitting a wall  → agent avoids walls quickly
        +100  reaching exit   → strong terminal signal
================================================================================
"""

import numpy as np
import gymnasium as gym
from gymnasium import spaces
from typing import Optional, Tuple, Dict, Any


# ---------------------------------------------------------------------------
# Maze Layout Definition
# ---------------------------------------------------------------------------
# 0 = free cell  |  1 = wall
# Agent starts at (0,0) — top-left corner (marked S below for reference)
# Exit is at (9,9)       — bottom-right corner (marked E below for reference)
#
#   Col→  0  1  2  3  4  5  6  7  8  9
# Row 0: [S, 0, 1, 0, 0, 0, 1, 0, 0, 0]
# Row 1: [0, 0, 1, 0, 1, 0, 1, 0, 1, 0]
# Row 2: [0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
# Row 3: [1, 1, 1, 0, 1, 1, 1, 0, 1, 0]
# Row 4: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
# Row 5: [0, 1, 1, 1, 1, 0, 1, 1, 1, 0]
# Row 6: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
# Row 7: [0, 1, 1, 0, 1, 0, 1, 1, 1, 0]
# Row 8: [0, 1, 0, 0, 0, 0, 1, 0, 0, 0]
# Row 9: [0, 1, 0, 1, 1, 1, 1, 0, 0, E]

DEFAULT_MAZE = np.array([
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 1, 0, 0, 0],   # Exit at (9,9)
], dtype=np.int32)


# ---------------------------------------------------------------------------
# Action Constants  (used externally to make code readable)
# ---------------------------------------------------------------------------
ACTION_UP    = 0
ACTION_DOWN  = 1
ACTION_LEFT  = 2
ACTION_RIGHT = 3

# Maps each action to a (delta_row, delta_col) movement vector
ACTION_DELTAS: Dict[int, Tuple[int, int]] = {
    ACTION_UP:    (-1,  0),   # row decreases → move north
    ACTION_DOWN:  ( 1,  0),   # row increases → move south
    ACTION_LEFT:  ( 0, -1),   # col decreases → move west
    ACTION_RIGHT: ( 0,  1),   # col increases → move east
}

ACTION_NAMES = {
    ACTION_UP:    "Up",
    ACTION_DOWN:  "Down",
    ACTION_LEFT:  "Left",
    ACTION_RIGHT: "Right",
}


# ---------------------------------------------------------------------------
# Reward Constants  (centralised so they're easy to tune)
# ---------------------------------------------------------------------------
REWARD_STEP        = -0.1   # Small penalty for each timestep → shortest path
REWARD_WALL        = -5.0   # Penalty for bumping into a wall / boundary
REWARD_EXIT        = +100.0 # Large positive reward for reaching the goal


class CustomMazeEnv(gym.Env):
    """
    A custom 2-D grid maze environment compatible with the Gymnasium API.

    Observation Space
    -----------------
    A single integer in [0, n_rows * n_cols) that uniquely identifies the
    current (row, col) cell:  state = row * n_cols + col

    Action Space
    ------------
    Discrete(4):
        0 → Up     (-1,  0)
        1 → Down   (+1,  0)
        2 → Left   ( 0, -1)
        3 → Right  ( 0, +1)

    Transition Dynamics
    -------------------
    • If the target cell is a wall or outside the grid bounds:
          - Agent stays in place (state unchanged)
          - Receives REWARD_WALL
    • If the target cell is free:
          - Agent moves to the target cell
          - Receives REWARD_STEP (time penalty)
    • If the target cell is the exit:
          - Agent moves to exit
          - Receives REWARD_EXIT
          - Episode terminates (terminated=True)
    • If max_steps is reached without exit:
          - Episode terminates with truncated=True
    """

    # Gymnasium metadata — enables render_mode="human" / "rgb_array" etc.
    metadata = {"render_modes": ["ansi", "human"], "render_fps": 4}

    def __init__(
        self,
        maze: Optional[np.ndarray] = None,
        start: Tuple[int, int] = (0, 0),
        exit_: Tuple[int, int] = (9, 9),
        max_steps: int = 500,
        render_mode: Optional[str] = None,
    ):
        """
        Parameters
        ----------
        maze        : 2-D numpy int array (0=free, 1=wall). Defaults to the
                      built-in 10×10 maze.
        start       : (row, col) of the agent's starting cell.
        exit_       : (row, col) of the goal cell.
        max_steps   : Maximum steps before the episode is truncated.
        render_mode : 'ansi' prints a text grid; 'human' is an alias.
        """
        super().__init__()

        # --- Maze layout -------------------------------------------------------
        self.maze      = maze if maze is not None else DEFAULT_MAZE.copy()
        self.n_rows, self.n_cols = self.maze.shape
        self.n_states  = self.n_rows * self.n_cols   # total discrete states
        self.n_actions = 4                           # Up / Down / Left / Right

        # --- Start & Exit positions --------------------------------------------
        self.start_pos = start
        self.exit_pos  = exit_

        # Sanity checks
        assert self.maze[start[0], start[1]] == 0, "Start cell must be free (0)."
        assert self.maze[exit_[0], exit_[1]] == 0, "Exit cell must be free (0)."

        # --- Gymnasium spaces --------------------------------------------------
        # observation_space: a single integer encoding the agent's (row, col)
        self.observation_space = spaces.Discrete(self.n_states)

        # action_space: four cardinal directions
        self.action_space = spaces.Discrete(self.n_actions)

        # --- Episode state (initialised in reset()) ----------------------------
        self._agent_pos: Tuple[int, int] = self.start_pos
        self._step_count: int = 0
        self._max_steps: int  = max_steps

        self.render_mode = render_mode

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def pos_to_state(self, row: int, col: int) -> int:
        """Convert a (row, col) grid position to a flat integer state index."""
        return row * self.n_cols + col

    def state_to_pos(self, state: int) -> Tuple[int, int]:
        """Convert a flat state index back to a (row, col) position."""
        return divmod(state, self.n_cols)

    # ------------------------------------------------------------------
    # Core Gymnasium API
    # ------------------------------------------------------------------

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[Dict] = None,
    ) -> Tuple[int, Dict[str, Any]]:
        """
        Reset the environment to its initial state.

        Returns
        -------
        observation : int  — initial flat state index
        info        : dict — optional diagnostic info
        """
        super().reset(seed=seed)   # seeds self.np_random (Gymnasium requirement)

        self._agent_pos  = self.start_pos
        self._step_count = 0

        obs  = self.pos_to_state(*self._agent_pos)
        info = {"agent_pos": self._agent_pos, "step": self._step_count}
        return obs, info

    def step(
        self, action: int
    ) -> Tuple[int, float, bool, bool, Dict[str, Any]]:
        """
        Execute one timestep of the environment.

        Parameters
        ----------
        action : int  — one of {0, 1, 2, 3}

        Returns
        -------
        observation : int   — new flat state after transition
        reward      : float — reward received for this transition
        terminated  : bool  — True if agent reached the exit
        truncated   : bool  — True if max_steps exceeded
        info        : dict  — diagnostic data (useful for debugging)
        """
        assert self.action_space.contains(action), f"Invalid action: {action}"

        self._step_count += 1
        row, col = self._agent_pos

        # --- Compute intended next position ------------------------------------
        dr, dc      = ACTION_DELTAS[action]
        next_row    = row + dr
        next_col    = col + dc

        # --- Check boundary & wall collisions ----------------------------------
        out_of_bounds = (
            next_row < 0 or next_row >= self.n_rows or
            next_col < 0 or next_col >= self.n_cols
        )
        hits_wall = (not out_of_bounds) and (self.maze[next_row, next_col] == 1)

        if out_of_bounds or hits_wall:
            # Agent stays put; incurs wall penalty
            reward = REWARD_WALL
            # State unchanged
        else:
            # Valid move — update position
            self._agent_pos = (next_row, next_col)
            row, col        = self._agent_pos

            if self._agent_pos == self.exit_pos:
                reward = REWARD_EXIT
            else:
                reward = REWARD_STEP

        # --- Termination conditions -------------------------------------------
        terminated = (self._agent_pos == self.exit_pos)
        truncated  = (self._step_count >= self._max_steps) and not terminated

        obs  = self.pos_to_state(*self._agent_pos)
        info = {
            "agent_pos" : self._agent_pos,
            "step"      : self._step_count,
            "hit_wall"  : out_of_bounds or hits_wall,
        }

        # Optional ANSI render after each step
        if self.render_mode in ("ansi", "human"):
            self.render()

        return obs, reward, terminated, truncated, info

    def render(self) -> Optional[str]:
        """
        Render the maze as a simple ASCII grid.

        Legend:
            #  Wall
            .  Free cell
            A  Agent's current position
            E  Exit
            S  Start (when agent is not there)
        """
        lines = []
        for r in range(self.n_rows):
            row_str = ""
            for c in range(self.n_cols):
                if (r, c) == self._agent_pos:
                    row_str += " A"
                elif (r, c) == self.exit_pos:
                    row_str += " E"
                elif (r, c) == self.start_pos and self._agent_pos != self.start_pos:
                    row_str += " S"
                elif self.maze[r, c] == 1:
                    row_str += " #"
                else:
                    row_str += " ."
            lines.append(row_str)
        grid_str = "\n".join(lines)
        if self.render_mode == "human":
            print(grid_str)
            print()
        return grid_str

    def get_maze_copy(self) -> np.ndarray:
        """Return a copy of the underlying maze array (for visualisation)."""
        return self.maze.copy()
