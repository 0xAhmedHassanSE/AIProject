# Maze Solver using Reinforcement Learning
### A Complete Q-Learning Implementation with Custom Gymnasium Environment

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Directory Structure](#2-directory-structure)
3. [Installation & Setup](#3-installation--setup)
4. [How to Run](#4-how-to-run)
5. [Algorithm Explanation — Q-Learning](#5-algorithm-explanation--q-learning)
6. [Exploration vs. Exploitation](#6-exploration-vs-exploitation)
7. [Environment Design](#7-environment-design)
8. [Reward System](#8-reward-system)
9. [Hyperparameter Guide](#9-hyperparameter-guide)
10. [Visualisations & Results](#10-visualisations--results)
11. [Tools & Libraries](#11-tools--libraries)
12. [Glossary of RL Terms](#12-glossary-of-rl-terms)

---

## 1. Project Overview

This project implements a **Reinforcement Learning (RL)** agent that learns to navigate a **custom 10×10 maze** purely through trial-and-error interaction with its environment — no prior knowledge of the maze layout is given.

The agent begins each episode at the top-left cell `(0,0)` and must discover the path to the exit at `(9,9)` using only **reward signals** as feedback. Over thousands of episodes the agent gradually shifts from random wandering to precise, optimal navigation.

### Core Technologies
| Component | Technology |
|-----------|-----------|
| RL Algorithm | Tabular Q-Learning (Watkins, 1989) |
| Environment Framework | OpenAI Gymnasium (modern `gymnasium` library) |
| Numerical Computing | NumPy |
| Visualisation | Matplotlib |
| Language | Python 3.10+ |

---

## 2. Directory Structure

```
maze_rl_project/
│
├── maze_env.py          # Custom Gymnasium maze environment
├── q_learning_agent.py  # Q-Learning agent (Q-table, ε-greedy, Bellman update)
├── train.py             # Training loop + metrics collection
├── visualization.py     # All matplotlib plotting functions
├── main.py              # Entry point — runs the full pipeline
├── README.md            # This document
│
└── outputs/             # Auto-created; all PNG figures saved here
    ├── 01_training_dashboard.png
    ├── 02_learning_curve.png
    ├── 03_steps_reduction.png
    ├── 04_epsilon_decay.png
    ├── 05_maze_optimal_path.png
    ├── 06_q_value_heatmap.png
    └── 07_policy_map.png
```

---

## 3. Installation & Setup

### Prerequisites
- Python **3.10** or higher  
- `pip` package manager

### Step-by-Step Installation

**Step 1 — (Recommended) Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

**Step 2 — Install all required packages:**
```bash
pip install gymnasium numpy matplotlib
```

> **Minimum versions tested:**
> - `gymnasium >= 0.29`
> - `numpy >= 1.24`
> - `matplotlib >= 3.7`

**Step 3 — Verify installation:**
```bash
python -c "import gymnasium, numpy, matplotlib; print('All packages OK')"
```

---

## 4. How to Run

**Run the complete pipeline** (train + evaluate + generate all plots):
```bash
python main.py
```

The script will:
1. Print the maze layout to the terminal
2. Display live training progress every 300 episodes
3. Print a full training summary
4. Save 7 visualisation figures to the `outputs/` folder

**Expected terminal output (excerpt):**
```
──────────────────────────────────────────────────────────
  Step 3 / 5 — Running Training Loop
──────────────────────────────────────────────────────────

  Starting Q-Learning Training
  Episodes : 3,000
  α (lr)   : 0.1
  γ (disc) : 0.99
  ε₀       : 1.0
  ε-decay  : 0.995

  Ep   300/3000 | ε=0.2238 | Avg Reward=  -87.34 | Avg Steps= 321.4 | Success%= 61.3%
  Ep   600/3000 | ε=0.0497 | Avg Reward=   12.45 | Avg Steps=  48.2 | Success%= 98.0%
  Ep   900/3000 | ε=0.0110 | Avg Reward=   85.21 | Avg Steps=  22.7 | Success%=100.0%
  ...
```

**To change hyperparameters**, edit the `CONFIG` dictionary at the top of `main.py`:
```python
CONFIG = {
    "N_EPISODES"   : 3000,    # ← increase for harder mazes
    "ALPHA"        : 0.1,     # ← learning rate
    "GAMMA"        : 0.99,    # ← discount factor
    "EPSILON_DECAY": 0.995,   # ← exploration decay speed
    ...
}
```

---

## 5. Algorithm Explanation — Q-Learning

### What is Q-Learning?

Q-Learning is a **model-free**, **off-policy** Temporal Difference (TD) algorithm introduced by Chris Watkins (1989). It learns an action-value function `Q(s, a)` that estimates the **expected cumulative discounted reward** when taking action `a` in state `s` and thereafter following the optimal policy.

### Formal Definition

The optimal action-value function is defined by the **Bellman Optimality Equation**:

```
Q*(s, a) = E[ r  +  γ · max_{a'} Q*(s', a')  |  s, a ]
```

Where:
- `s`  = current state
- `a`  = action taken
- `r`  = immediate reward received
- `s'` = resulting next state
- `γ`  = discount factor (how much future rewards are valued)

### The Update Rule

The Q-table is updated after every single step using:

```
Q(s, a)  ←  Q(s, a)  +  α · δ

where  δ = r  +  γ · max_{a'} Q(s', a')  -  Q(s, a)
            └──────────────────────────────────────┘
                         TD Error
```

**Interpretation of the TD Error δ:**
| δ > 0 | The transition was **better** than expected → increase Q(s,a) |
|-------|---------------------------------------------------------------|
| δ < 0 | The transition was **worse** than expected → decrease Q(s,a) |
| δ = 0 | Q-values have **converged** → no update needed              |

### Terminal States

When the agent reaches the exit (a terminal state), there is no future return, so the target simplifies to:
```
Q(s_exit, a)  ←  Q(s_exit, a)  +  α · (r_exit - Q(s_exit, a))
```

### Convergence Guarantee

Under the following standard conditions, Q-learning converges to Q*:
1. All state-action pairs are visited infinitely often
2. The learning rate α satisfies: Σα = ∞ and Σα² < ∞
3. The reward signal is bounded

---

## 6. Exploration vs. Exploitation

### The Dilemma

An RL agent faces a fundamental trade-off:
- **Exploit:** Take the action with the highest known Q-value (greedy). Efficient — but may miss better undiscovered paths.
- **Explore:** Take a random action. Discovers new paths — but wastes time on known bad actions.

### ε-Greedy Strategy

This project uses the **ε-greedy** policy:

```
π(s) = | random action          with probability  ε
        | argmax_a Q(s,a)        with probability  1-ε
```

### Exponential Epsilon Decay

`ε` is annealed after each episode:
```
ε_{t+1}  =  max(ε_min,  ε_t  ×  decay_rate)
```

**Why this works:**
- **Early training** (ε ≈ 1.0): Agent explores aggressively — needed when Q-table contains no useful information.
- **Mid training** (ε ≈ 0.1): Agent mostly exploits, but still corrects remaining errors.
- **Late training** (ε ≈ 0.01): Agent is near-deterministic; pure exploitation of the converged Q-table.

### Epsilon Schedule (default settings)

| Episode | ε value | Behaviour |
|---------|---------|-----------|
| 1       | 1.000   | 100% random exploration |
| 200     | 0.368   | ~37% exploration |
| 400     | 0.135   | ~14% exploration |
| 600     | 0.050   | ~5% exploration  |
| 1000+   | 0.010   | ~1% exploration (minimum) |

---

## 7. Environment Design

### Maze Layout (10×10 grid)

```
Col→  0  1  2  3  4  5  6  7  8  9
Row 0: S  .  #  .  .  .  #  .  .  .
Row 1: .  .  #  .  #  .  #  .  #  .
Row 2: .  .  .  .  #  .  .  .  #  .
Row 3: #  #  #  .  #  #  #  .  #  .
Row 4: .  .  .  .  .  .  #  .  .  .
Row 5: .  #  #  #  #  .  #  #  #  .
Row 6: .  .  .  .  #  .  .  .  .  .
Row 7: .  #  #  .  #  .  #  #  #  .
Row 8: .  #  .  .  .  .  #  .  .  .
Row 9: .  #  .  #  #  #  #  .  .  E

  # = Wall    . = Free cell    S = Start    E = Exit
```

### State Space

Each grid cell `(row, col)` is encoded as a single integer:
```
state  =  row × n_cols  +  col
```
Total states = 10 × 10 = **100 discrete states**

### Action Space

`Discrete(4)` — four cardinal directions:

| Action | ID | Δrow | Δcol |
|--------|-----|------|------|
| Up     | 0   | -1   |  0   |
| Down   | 1   | +1   |  0   |
| Left   | 2   |  0   | -1   |
| Right  | 3   |  0   | +1   |

### Q-Table Dimensions

```
Q-table shape = (n_states, n_actions) = (100, 4)
Total parameters learned = 400 values
```

---

## 8. Reward System

The reward system is carefully designed to encourage **fast, direct paths** to the exit:

| Event | Reward | Rationale |
|-------|--------|-----------|
| Each step taken | **−0.1** | Encourages the shortest path (time penalty) |
| Hitting a wall / boundary | **−5.0** | Quickly teaches the agent to avoid walls |
| Reaching the exit | **+100.0** | Strong terminal signal; dominates all step penalties |

### Why These Values?

The optimal path in this maze is ~22 steps. At −0.1 per step, that's −2.2 total penalties vs. +100.0 for the exit → **net reward ≈ +97.8** for the optimal path.

A suboptimal path of 100 steps would yield −10.0 penalties vs. +100.0 → **net ≈ +90.0**. The agent learns to prefer fewer steps.

---

## 9. Hyperparameter Guide

| Parameter | Default | Effect |
|-----------|---------|--------|
| `ALPHA` (α) | 0.1 | Learning rate. Higher → learns faster but can oscillate. Lower → more stable but slower convergence. |
| `GAMMA` (γ) | 0.99 | Discount factor. Close to 1.0 → agent values long-term rewards (good for long mazes). |
| `EPSILON_START` | 1.0 | Start with full exploration. Always recommended at 1.0. |
| `EPSILON_DECAY` | 0.995 | How quickly exploration fades. Lower → faster decay (good for simple mazes). |
| `EPSILON_MIN` | 0.01 | Never fully stop exploring. Ensures robustness. |
| `N_EPISODES` | 3000 | More episodes → better convergence for complex mazes. |
| `MAX_STEPS` | 500 | Maximum steps per episode before truncation. |

### Recommended Experiments

```python
# Faster convergence (for quick prototyping)
"ALPHA": 0.2, "EPSILON_DECAY": 0.99, "N_EPISODES": 1500

# More stable convergence (for research)
"ALPHA": 0.05, "EPSILON_DECAY": 0.998, "N_EPISODES": 5000

# Harder maze (increase grid size in maze_env.py)
# Replace DEFAULT_MAZE with a 15×15 or 20×20 layout
```

---

## 10. Visualisations & Results

The following figures are automatically generated to `outputs/`:

### 01 — Training Dashboard
Four-panel summary: Learning Curve, Steps Reduction, ε Decay, TD Error convergence. The most comprehensive single view of training progress.

### 02 — Learning Curve (Rewards per Episode)
Shows total reward increasing from large negative values toward ~+90. The smoothed line reveals the underlying learning trend despite noisy exploration.

**Expected shape:** Initially flat/negative (random exploration) → rapid rise (discovery of path) → plateau (optimal policy).

### 03 — Steps Reduction
Shows how many steps the agent takes per episode. Should decrease dramatically as the agent learns the optimal route.

**Expected shape:** High steps (~500 truncations) early → rapid drop → plateau at optimal path length (~22 steps).

### 04 — Epsilon Decay
Shows the exponential decay of ε. Confirms exploration schedule is working correctly.

### 05 — Maze Optimal Path
Visual overlay of the agent's final greedy path on the maze grid. Arrows show direction of travel at each step. Numbers indicate step count.

### 06 — Q-Value Heatmap
Shows `V*(s) = max_a Q(s,a)` for every free cell. Green cells = high value (close to exit in terms of discounted reward). Red cells = low value (far or blocked). The gradient should visually "flow" toward the exit.

### 07 — Policy Arrow Map
Shows the greedy policy action at every free cell. Arrows should converge toward the exit, forming a coherent "flow field".

---

## 11. Tools & Libraries

### `gymnasium` (OpenAI Gymnasium)
The standard framework for building RL environments. Replaced the legacy `gym` package. Key API used:
- `gym.Env` — base class for all environments
- `spaces.Discrete(n)` — discrete observation/action spaces
- `env.reset()` → initial state + info
- `env.step(action)` → (next_state, reward, terminated, truncated, info)

### `numpy`
Used for the Q-table (2D array), maze layout (2D int array), and all vectorised computations. The Q-table is a `numpy.ndarray` of shape `(n_states, n_actions)`.

### `matplotlib`
Complete plotting library used for all 7 visualisation figures. Key features used: `imshow` for maze grids, `annotate` for arrows, `semilogy` for TD error plot, `GridSpec` for dashboard layout.

---

## 12. Glossary of RL Terms

| Term | Definition |
|------|-----------|
| **Agent** | The learner/decision-maker (our maze navigator) |
| **Environment** | The world the agent interacts with (the maze) |
| **State (s)** | Current situation of the agent (grid cell coordinates) |
| **Action (a)** | A choice made by the agent (Up/Down/Left/Right) |
| **Reward (r)** | Scalar feedback signal from the environment |
| **Policy (π)** | Mapping from states to actions |
| **Episode** | One complete run from start to exit (or timeout) |
| **Q-value Q(s,a)** | Expected cumulative discounted reward for (state, action) |
| **Q-table** | Matrix of all Q-values; the agent's "memory" |
| **Bellman Equation** | Recursive definition of optimal Q-values |
| **TD Error (δ)** | Difference between predicted and target Q-value |
| **Discount factor (γ)** | How much future rewards are weighted vs. immediate rewards |
| **Greedy Policy** | Always pick argmax_a Q(s,a) — pure exploitation |
| **ε-greedy Policy** | Pick random action with prob ε, greedy with prob 1-ε |
| **Convergence** | When Q-values stop changing significantly (TD error → 0) |
| **Off-policy** | Learning about optimal policy while following a different (exploratory) policy |
| **Model-free** | Does not build an internal model of the environment's dynamics |

---

*Project developed as a complete, production-ready Reinforcement Learning demonstration.*  
*All code is extensively documented with RL mathematics and implementation rationale.*
