"""
================================================================================
  q_learning_agent.py — Q-Learning Agent
================================================================================
  Author  : Expert AI Researcher / Senior Python Developer
  Project : Maze Solver using Reinforcement Learning

  Description:
    Implements the classic tabular Q-Learning algorithm with an ε-greedy
    exploration strategy and exponential epsilon decay.

  ─── Q-Learning (Watkins, 1989) — The Math ─────────────────────────────────

    Q-Learning is a model-free, off-policy Temporal Difference (TD) algorithm.
    It estimates the optimal action-value function Q*(s, a), defined as:

        Q*(s, a) = E[ Σ_{t=0}^{∞}  γ^t · r_{t+1}  |  s_0=s, a_0=a, π* ]

    where γ ∈ [0,1) is the discount factor and π* is the optimal policy.

    The Bellman Optimality Equation gives us the update target:

        Q*(s, a) = r  +  γ · max_{a'} Q*(s', a')
                   └──────────────────────────────┘
                           "TD Target"

    The agent iteratively updates its Q-table using:

        Q(s, a)  ←  Q(s, a)  +  α · [ r  +  γ · max_{a'} Q(s', a')  -  Q(s, a) ]
                                       └────────────────────────────────────────┘
                                                    "TD Error" (δ)

    Intuition:
      • If the TD error δ > 0 → the new experience was BETTER than expected
        → increase Q(s,a) to make this action more attractive in the future.
      • If δ < 0 → worse than expected → decrease Q(s,a).
      • Over many episodes, Q converges to Q* under standard conditions.

  ─── Exploration vs. Exploitation (ε-greedy) ───────────────────────────────

    Dilemma: The agent must balance:
        • Exploration : Try random actions to discover new, possibly better paths.
        • Exploitation: Take the greedy action argmax_a Q(s,a) to maximise reward.

    ε-greedy strategy:
        With probability  ε  → choose a random action  (explore)
        With probability 1-ε → choose argmax_a Q(s,a) (exploit)

    Epsilon Decay:
        ε is annealed exponentially each episode:
            ε_{t+1} = max(ε_min,  ε_t · decay_rate)

        This ensures heavy exploration early (when Q-values are uninformed) and
        gradual shift to exploitation as the Q-table becomes accurate.
================================================================================
"""

import numpy as np
from typing import Optional


class QLearningAgent:
    """
    Tabular Q-Learning agent for discrete state & action spaces.

    The agent maintains a Q-table Q[s, a] of shape (n_states, n_actions).
    All values are initialised to zero (optimistic initialisation is optional).

    Parameters
    ----------
    n_states    : int   — Total number of discrete states.
    n_actions   : int   — Total number of discrete actions.
    alpha       : float — Learning rate α ∈ (0, 1].
                          High α → fast learning but noisy; low α → stable but slow.
    gamma       : float — Discount factor γ ∈ [0, 1).
                          Close to 1 → values long-term rewards; 0 → myopic.
    epsilon     : float — Initial exploration probability ε₀ ∈ [0, 1].
    epsilon_min : float — Minimum ε after decay (keeps residual exploration).
    epsilon_decay: float— Multiplicative decay applied after each episode.
    seed        : int   — Random seed for reproducibility.
    """

    def __init__(
        self,
        n_states:      int,
        n_actions:     int,
        alpha:         float = 0.1,
        gamma:         float = 0.99,
        epsilon:       float = 1.0,
        epsilon_min:   float = 0.01,
        epsilon_decay: float = 0.995,
        seed:          Optional[int] = 42,
    ):
        self.n_states      = n_states
        self.n_actions     = n_actions
        self.alpha         = alpha       # α: learning rate
        self.gamma         = gamma       # γ: discount factor
        self.epsilon       = epsilon     # ε: current exploration rate
        self.epsilon_min   = epsilon_min
        self.epsilon_decay = epsilon_decay

        # Seeded RNG for reproducible action sampling
        self._rng = np.random.default_rng(seed)

        # ── Q-Table Initialisation ──────────────────────────────────────────
        # Shape: (n_states, n_actions)
        # Initialise to zero → neutral prior; agent learns from scratch.
        # Alternative: small positive values ("optimistic initialisation") can
        # boost early exploration but zero-init is standard for Q-learning.
        self.q_table = np.zeros((n_states, n_actions), dtype=np.float64)

        # ── Tracking metrics ────────────────────────────────────────────────
        self.episode_count = 0
        self.epsilon_history: list[float] = []   # ε value after each episode

    # ------------------------------------------------------------------
    # Action Selection
    # ------------------------------------------------------------------

    def select_action(self, state: int) -> int:
        """
        Choose an action using the ε-greedy policy.

        With probability ε  → explore: uniform random action.
        With probability 1-ε → exploit: argmax_a Q(state, a).

        Parameters
        ----------
        state : int — Current flat state index.

        Returns
        -------
        action : int — Chosen action index.
        """
        if self._rng.random() < self.epsilon:
            # ── Exploration: random action ──────────────────────────────────
            return int(self._rng.integers(0, self.n_actions))
        else:
            # ── Exploitation: greedy action ─────────────────────────────────
            # Ties broken randomly to avoid systematic bias
            q_row  = self.q_table[state]
            max_q  = np.max(q_row)
            best   = np.where(q_row == max_q)[0]
            return int(self._rng.choice(best))

    def greedy_action(self, state: int) -> int:
        """
        Always return the greedy (best-known) action — used at test / render time
        where we want to evaluate learned policy without any randomness.
        """
        q_row = self.q_table[state]
        max_q = np.max(q_row)
        best  = np.where(q_row == max_q)[0]
        return int(self._rng.choice(best))

    # ------------------------------------------------------------------
    # Q-Table Update
    # ------------------------------------------------------------------

    def update(
        self,
        state:      int,
        action:     int,
        reward:     float,
        next_state: int,
        terminated: bool,
    ) -> float:
        """
        Apply one Q-Learning update using the Bellman equation.

        Update rule:
            δ      = r  +  γ · max_{a'} Q(s', a')  -  Q(s, a)
                     └────────────────────────────────────────┘
                                  TD Error
            Q(s,a) ← Q(s,a)  +  α · δ

        When `terminated=True` (terminal state), there is no future reward,
        so the target collapses to just the immediate reward r:
            Q(s,a) ← Q(s,a)  +  α · (r - Q(s,a))

        Parameters
        ----------
        state      : int   — Current state s.
        action     : int   — Action taken a.
        reward     : float — Immediate reward r.
        next_state : int   — Resulting next state s'.
        terminated : bool  — Whether s' is a terminal state.

        Returns
        -------
        td_error : float — The TD error δ (useful for diagnostics/logging).
        """
        # Current Q-value estimate
        current_q = self.q_table[state, action]

        # Bootstrapped TD target
        if terminated:
            # No future returns from a terminal state
            td_target = reward
        else:
            # Bellman optimality: use the best known future value
            best_next_q = np.max(self.q_table[next_state])
            td_target   = reward + self.gamma * best_next_q

        # TD Error δ
        td_error = td_target - current_q

        # In-place Q-table update
        self.q_table[state, action] += self.alpha * td_error

        return td_error

    # ------------------------------------------------------------------
    # Epsilon Decay
    # ------------------------------------------------------------------

    def decay_epsilon(self) -> None:
        """
        Anneal ε after each episode:
            ε ← max(ε_min,  ε · decay_rate)

        Call this once at the end of every training episode.
        """
        self.episode_count += 1
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        self.epsilon_history.append(self.epsilon)

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def get_best_path(self, env) -> list[tuple[int, int]]:
        """
        Follow the greedy policy from start to exit (or until max_steps).
        Used after training to extract and visualise the optimal path.

        Parameters
        ----------
        env : CustomMazeEnv — the maze environment.

        Returns
        -------
        path : list of (row, col) tuples representing the agent's trajectory.
        """
        obs, _ = env.reset()
        path   = [env.state_to_pos(obs)]

        for _ in range(env._max_steps):
            action       = self.greedy_action(obs)
            obs, _, terminated, truncated, _ = env.step(action)
            path.append(env.state_to_pos(obs))
            if terminated or truncated:
                break

        return path

    def q_table_summary(self) -> str:
        """Return a compact summary string of the current Q-table statistics."""
        return (
            f"Q-Table shape : {self.q_table.shape}\n"
            f"  Min Q-value : {self.q_table.min():.4f}\n"
            f"  Max Q-value : {self.q_table.max():.4f}\n"
            f"  Mean Q-value: {self.q_table.mean():.4f}\n"
            f"  Nonzero %   : {100*(self.q_table != 0).mean():.1f}%\n"
            f"  Current ε   : {self.epsilon:.4f}\n"
            f"  Episodes    : {self.episode_count}"
        )
