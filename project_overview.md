# Artificial Intelligence Real-World Simulation Project
## Maze Solver using Reinforcement Learning

### 1. Introduction
This project implements an autonomous agent that learns to navigate a complex maze environment using Reinforcement Learning (RL). The agent begins with no prior knowledge of the maze layout and must discover the optimal path to the exit purely through trial-and-error interactions, guided by a reward system.

### 2. AI Algorithms and Concepts
The core of this project is built upon the concepts discussed in the AI curriculum (Lectures 6 to 10):

#### 2.1 Markov Decision Process (MDP) [Reference: Lectures 7 & 8]
The maze is formulated as an MDP:
*   **States (S):** Each cell in the grid represents a unique discrete state.
*   **Actions (A):** The agent can move in four cardinal directions (Up, Down, Left, Right).
*   **Transition Model (T):** The environment determines the next state based on the action (e.g., moving into a wall keeps the agent in the same state).
*   **Rewards (R):** The agent receives a penalty of -0.1 for every step (encouraging the shortest path), a penalty of -5.0 for hitting a wall, and a large reward of +100 for reaching the exit.

#### 2.2 Q-Learning (Model-Free RL) [Reference: Lecture 9]
Since the agent does not have access to the transition probabilities or the reward function initially, it uses **Q-Learning**, a model-free Temporal Difference (TD) algorithm. 
The agent maintains a Q-Table, updating the Q-values $Q(S, A)$ after every step using the Bellman Optimality Equation:
$$Q(S,A) \leftarrow Q(S,A) + \alpha [R + \gamma \max_{a'} Q(S', a') - Q(S,A)]$$
Where $\alpha$ is the learning rate and $\gamma$ is the discount factor.

#### 2.3 Exploration vs. Exploitation ($\epsilon$-greedy) [Reference: Lecture 10]
To ensure the agent explores the maze rather than getting stuck in local optima, an $\epsilon$-greedy policy is employed. The agent chooses a random action with probability $\epsilon$ and the best-known action with probability $1-\epsilon$. The value of $\epsilon$ is exponentially decayed over time, allowing the agent to shift from exploration to exploitation as it learns.

#### 2.4 Hyperparameter Analysis & Practical Implications
Through experimental tuning, we observed the critical impact of the Q-Learning hyperparameters on the agent's behavior:

*   **Discount Factor ($\gamma$): Far-sightedness vs. Myopia**
    *   **Optimal ($\approx 0.95$):** Allows the reward of the exit (+100) to propagate backward through the maze, enabling the agent to "see" the goal from the starting point and find the optimal shortest path.
    *   **Extreme Low ($\approx 0.0$):** The agent becomes completely myopic, evaluating only the immediate next step. Since all non-exit cells yield zero or negative rewards, the agent perceives all paths as equally poor, resulting in infinite loops and failure to solve the maze.

*   **Learning Rate ($\alpha$): Adaptability vs. Stability**
    *   **Optimal ($0.1$ - $0.5$):** The agent accumulates knowledge gradually, weighing past experiences against new discoveries, leading to a stable and reliable convergence to the optimal path.
    *   **Extreme High ($\approx 1.0$):** The agent exhibits "zero memory" of past trials, instantly overriding its Q-table with the most recent observation. This causes severe instability; the agent constantly changes its mind after a single bad step, leading to a chaotic learning curve that struggles to converge.

*   **Exploration Rate ($\epsilon$): Randomness & Discovery**
    *   **Pure Exploration ($\epsilon = 1.0$):** The agent wanders completely randomly. While it discovers the entire map, it never utilizes this knowledge to optimize its path, failing to act intelligently.
    *   **Pure Exploitation ($\epsilon = 0.0$):** The agent relies solely on its initial (empty or flawed) knowledge. It often gets stuck in a corner after receiving a penalty, refusing to explore alternative routes to the exit.
    *   **Decay Strategy (The Solution):** Starting with $\epsilon=1.0$ and decaying it gradually over episodes ensures the agent first maps the environment (Exploration) and subsequently exploits the learned Q-values to take the shortest route (Exploitation).

### 3. Tools and Simulation Platform
*   **Simulation Platform:** The environment is built using **OpenAI Gymnasium** (`gymnasium` library), fulfilling the project requirement. It defines the state space, action space, and transition logic.
*   **Implementation Language:** Python.
*   **Data Structures:** NumPy is used for efficient Q-table matrix operations.
*   **Visualizations:** Matplotlib is used to track learning progress and visualize the learned policy.

### 4. Results and Outcomes
The agent was trained over 3000 episodes. The results clearly demonstrate the effectiveness of the Q-Learning algorithm:
*   **Learning Curve:** Initially, the agent accumulated large negative rewards due to random exploration. Over time, the reward converged to a maximum positive value, indicating the agent consistently found the exit.
*   **Steps Reduction:** The number of steps per episode dropped from the maximum limit (500 steps) to the optimal path length.
*   **Q-Value Heatmap & Policy Map:** The generated visualizations show a clear gradient of Q-values flowing toward the exit, proving the agent successfully mapped the environment.

*Note: The generated plots (e.g., `01_training_dashboard.png`, `05_maze_optimal_path.png`) are included in the `outputs/` folder of the source code and should be attached to this report as figures.*
