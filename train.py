"""
================================================================================
  train.py — Training Loop for the RL Maze Solver
================================================================================
  Author  : Expert AI Researcher / Senior Python Developer
  Project : Maze Solver using Reinforcement Learning

  Description:
    Contains the TrainingLoop class that orchestrates the interaction between
    the CustomMazeEnv and the QLearningAgent.  Collects all episode-level
    metrics needed for post-training analysis.

  Training Flow (per episode):
    1.  env.reset()              → obtain initial state s₀
    2.  For each timestep t:
          a. agent.select_action(s)       → pick action aₜ  (ε-greedy)
          b. env.step(aₜ)                 → receive (s', r, done, trunc, info)
          c. agent.update(s,a,r,s',done)  → Q-Learning Bellman update
          d. s ← s'
          e. Accumulate episode reward
    3.  agent.decay_epsilon()    → anneal exploration rate
    4.  Store episode metrics
================================================================================
"""

import time
from dataclasses import dataclass, field
from typing import List, Optional

from maze_env import CustomMazeEnv
from q_learning_agent import QLearningAgent


# ---------------------------------------------------------------------------
# Data container for training results
# ---------------------------------------------------------------------------

@dataclass
class TrainingMetrics:
    """
    Stores all per-episode statistics collected during training.

    Attributes
    ----------
    episode_rewards      : Total (undiscounted) reward accumulated per episode.
    episode_steps        : Number of timesteps taken per episode.
    episode_success      : Whether the agent reached the exit each episode.
    epsilon_per_episode  : ε value recorded at the end of each episode.
    td_errors_mean       : Mean |TD error| per episode (proxy for learning stability).
    training_time_sec    : Wall-clock time for the entire training run.
    """
    episode_rewards:     List[float] = field(default_factory=list)
    episode_steps:       List[int]   = field(default_factory=list)
    episode_success:     List[bool]  = field(default_factory=list)
    epsilon_per_episode: List[float] = field(default_factory=list)
    td_errors_mean:      List[float] = field(default_factory=list)
    sample_paths:        dict        = field(default_factory=dict)
    training_time_sec:   float       = 0.0

    # ── Derived properties ──────────────────────────────────────────────────

    @property
    def n_episodes(self) -> int:
        return len(self.episode_rewards)

    @property
    def success_rate(self) -> float:
        """Overall fraction of episodes where the agent reached the exit."""
        if not self.episode_success:
            return 0.0
        return sum(self.episode_success) / len(self.episode_success)

    @property
    def best_episode_steps(self) -> int:
        """Fewest steps taken in any successful episode."""
        successful_steps = [
            s for s, ok in zip(self.episode_steps, self.episode_success) if ok
        ]
        return min(successful_steps) if successful_steps else -1

    def smoothed_rewards(self, window: int = 50) -> List[float]:
        """Moving average of episode rewards for smoother plotting."""
        smoothed = []
        for i in range(len(self.episode_rewards)):
            start = max(0, i - window + 1)
            smoothed.append(sum(self.episode_rewards[start:i+1]) / (i - start + 1))
        return smoothed

    def smoothed_steps(self, window: int = 50) -> List[float]:
        """Moving average of episode steps."""
        smoothed = []
        for i in range(len(self.episode_steps)):
            start = max(0, i - window + 1)
            smoothed.append(sum(self.episode_steps[start:i+1]) / (i - start + 1))
        return smoothed

    def summary(self) -> str:
        """Return a human-readable training summary."""
        return (
            f"\n{'='*60}\n"
            f"  TRAINING SUMMARY\n"
            f"{'='*60}\n"
            f"  Total Episodes   : {self.n_episodes:,}\n"
            f"  Success Rate     : {100 * self.success_rate:.1f}%\n"
            f"  Best Path Length : {self.best_episode_steps} steps\n"
            f"  Final ε          : {self.epsilon_per_episode[-1]:.4f}\n"
            f"  Training Time    : {self.training_time_sec:.2f} seconds\n"
            f"{'='*60}\n"
        )


# ---------------------------------------------------------------------------
# Training Loop
# ---------------------------------------------------------------------------

class TrainingLoop:
    """
    Manages the training of a QLearningAgent on a CustomMazeEnv.

    Usage
    -----
        env    = CustomMazeEnv()
        agent  = QLearningAgent(n_states=env.n_states, n_actions=env.n_actions)
        loop   = TrainingLoop(env, agent, n_episodes=3000)
        metrics = loop.run()
    """

    def __init__(
        self,
        env:          CustomMazeEnv,
        agent:        QLearningAgent,
        n_episodes:   int = 3000,
        log_interval: int = 200,
        verbose:      bool = True,
        **kwargs
    ):
        """
        Parameters
        ----------
        env          : CustomMazeEnv instance.
        agent        : QLearningAgent instance.
        n_episodes   : Number of training episodes.
        log_interval : Print a progress line every `log_interval` episodes.
        verbose      : Whether to print progress during training.
        """
        self.env          = env
        self.agent        = agent
        self.n_episodes   = n_episodes
        self.log_interval = log_interval
        self.verbose      = verbose

    def run(self) -> TrainingMetrics:
        """
        Execute the full training loop.

        Returns
        -------
        metrics : TrainingMetrics — all collected statistics.
        """
        metrics    = TrainingMetrics()
        start_time = time.time()
        best_successful_steps = float('inf')

        if self.verbose:
            print(f"\n{'='*60}")
            print(f"  Starting Q-Learning Training")
            print(f"  Episodes : {self.n_episodes:,}")
            print(f"  α (lr)   : {self.agent.alpha}")
            print(f"  γ (disc) : {self.agent.gamma}")
            print(f"  ε₀       : {self.agent.epsilon}")
            print(f"  ε-decay  : {self.agent.epsilon_decay}")
            print(f"{'='*60}\n")

        for episode in range(1, self.n_episodes + 1):

            # ── Episode Initialisation ──────────────────────────────────────
            state, _      = self.env.reset()
            total_reward  = 0.0
            total_abs_tde = 0.0   # accumulated |TD error| for this episode
            n_steps       = 0
            success       = False
            current_path  = [self.env.state_to_pos(state)]

            # ── Episode Loop ────────────────────────────────────────────────
            while True:
                # 1. Select action using ε-greedy policy
                action = self.agent.select_action(state)

                # 2. Take a step in the environment
                next_state, reward, terminated, truncated, _ = self.env.step(action)

                # 3. Apply the Q-Learning Bellman update
                #    Q(s,a) ← Q(s,a) + α·[r + γ·max Q(s',·) - Q(s,a)]
                td_error = self.agent.update(
                    state      = state,
                    action     = action,
                    reward     = reward,
                    next_state = next_state,
                    terminated = terminated,
                )

                # 4. Accumulate episode statistics
                total_reward  += reward
                total_abs_tde += abs(td_error)
                n_steps       += 1
                state          = next_state
                current_path.append(self.env.state_to_pos(state))

                # 5. Check episode end conditions
                if terminated:
                    success = True
                    break
                if truncated:
                    break

            # ── End of Episode ───────────────────────────────────────────────
            # Decay exploration rate: ε ← max(ε_min, ε · decay)
            self.agent.decay_epsilon()

            # Record metrics
            metrics.episode_rewards.append(total_reward)
            metrics.episode_steps.append(n_steps)
            metrics.episode_success.append(success)
            metrics.epsilon_per_episode.append(self.agent.epsilon)
            metrics.td_errors_mean.append(
                total_abs_tde / n_steps if n_steps > 0 else 0.0
            )
            
            # Save paths for milestones (Record every improvement!)
            if episode == 1:
                metrics.sample_paths[episode] = current_path
            elif success and n_steps < best_successful_steps:
                best_successful_steps = n_steps
                metrics.sample_paths[episode] = current_path

            # ── Periodic Logging ────────────────────────────────────────────
            if self.verbose and episode % self.log_interval == 0:
                # Recent window stats
                w        = min(self.log_interval, episode)
                r_recent = metrics.episode_rewards[-w:]
                s_recent = metrics.episode_steps[-w:]
                ok_rate  = 100 * sum(metrics.episode_success[-w:]) / w

                print(
                    f"  Ep {episode:>5}/{self.n_episodes} | "
                    f"ε={self.agent.epsilon:.4f} | "
                    f"Avg Reward={sum(r_recent)/w:>8.2f} | "
                    f"Avg Steps={sum(s_recent)/w:>6.1f} | "
                    f"Success%={ok_rate:>5.1f}%"
                )

        # ── Training Complete ────────────────────────────────────────────────
        metrics.training_time_sec = time.time() - start_time

        if self.verbose:
            print(metrics.summary())
            print(self.agent.q_table_summary())

        return metrics
