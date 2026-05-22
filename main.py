"""
================================================================================
  main.py — Entry Point for the Maze RL Solver (Multi-Maze Edition)
================================================================================
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import gym_compat  # installs shim if needed

# ---------------------------------------------------------------------------
# ── Configuration ──────────────────────────────────────────────────────────
# ---------------------------------------------------------------------------
CONFIG = {
    "MAX_STEPS_PER_EPISODE": 500,
    "N_EPISODES"            : 3000,
    "LOG_INTERVAL"          : 500,
    "ALPHA"                 : 0.1,
    "GAMMA"                 : 0.99,
    "EPSILON_START"         : 1.0,
    "EPSILON_MIN"           : 0.01,
    "EPSILON_DECAY"         : 0.995,
    "SEED"                  : 42,
    "SAVE_PLOTS"            : True,
    "OUTPUT_DIR"            : "outputs",
    "SMOOTH_WINDOW"         : 50,
}

# ---------------------------------------------------------------------------
# ── Multiple Maze Layouts (0=Free, 1=Wall, S=(0,0), E=(9,9)) ───────────────
# ---------------------------------------------------------------------------
MAZES = {
    "Maze_1_Easy": np.array([
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    ]),

    "Maze_2_ZigZag": np.array([
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    ]),

    "Maze_3_Hard": np.array([
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    ])
}

# ---------------------------------------------------------------------------
# ── Imports ────────────────────────────────────────────────────────────────
# ---------------------------------------------------------------------------
from maze_env       import CustomMazeEnv
from q_learning_agent import QLearningAgent
from train          import TrainingLoop
from visualization  import (
    plot_training_dashboard,
    render_maze_path,
    render_q_value_heatmap,
)

# ---------------------------------------------------------------------------
# ── Helpers & Animation ────────────────────────────────────────────────────
# ---------------------------------------------------------------------------

def animate_agent(env, path, maze_name):
    """دالة لعمل أنيميشن لحركة الروبوت داخل المتاهة"""
    print(f"\n  🎬 Starting Live Visual Simulation for {maze_name}...")
    fig, ax = plt.subplots(figsize=(6, 6))

    for step, pos in enumerate(path):
        ax.clear()
        maze_img = env.get_maze_copy().astype(float)
        maze_img[pos[0], pos[1]] = 0.5

        ax.imshow(maze_img, cmap='Set3', interpolation='nearest')

        ax.set_xticks([x - 0.5 for x in range(env.n_cols + 1)], minor=True)
        ax.set_yticks([y - 0.5 for y in range(env.n_rows + 1)], minor=True)
        ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.5)

        ax.text(env.start_pos[1], env.start_pos[0], 'S', ha="center", va="center", color="green", fontweight="bold", fontsize=14)
        ax.text(env.exit_pos[1], env.exit_pos[0], 'E', ha="center", va="center", color="red", fontweight="bold", fontsize=14)

        ax.set_title(f"[{maze_name}] Navigation\nStep: {step} | Position: {pos}", fontsize=12, fontweight="bold")
        ax.set_xticks([])
        ax.set_yticks([])

        plt.pause(0.15) # سرعنا الأنيميشن شوية عشان الخرائط المتعددة

    # بعد ما يخلص الخريطة بيقفل نافذة الأنيميشن عشان يدخل على المتاهة اللي بعدها
    plt.close(fig)
    print(f"  🏁 Animation complete for {maze_name}.")

def _out(filename: str) -> str | None:
    if not CONFIG["SAVE_PLOTS"]:
        return None
    os.makedirs(CONFIG["OUTPUT_DIR"], exist_ok=True)
    return os.path.join(CONFIG["OUTPUT_DIR"], filename)

def banner(text: str) -> None:
    print(f"\n{'━'*60}\n  {text}\n{'━'*60}")

# ---------------------------------------------------------------------------
# ── Main Pipeline ──────────────────────────────────────────────────────────
# ---------------------------------------------------------------------------

def main() -> None:

    # هنلف على الـ 3 متاهات اللي عرفناهم فوق
    for maze_name, maze_layout in MAZES.items():
        banner(f"🚀 STARTING: {maze_name}")

        # 1. إنشاء البيئة باستخدام الخريطة الحالية
        env = CustomMazeEnv(maze=maze_layout, max_steps=CONFIG["MAX_STEPS_PER_EPISODE"])

        # 2. إنشاء عميل جديد يبدأ من الصفر (عشان ميعتمدش على حفظ المتاهة اللي فاتت)
        agent = QLearningAgent(
            n_states      = env.n_states,
            n_actions     = env.n_actions,
            alpha         = CONFIG["ALPHA"],
            gamma         = CONFIG["GAMMA"],
            epsilon       = CONFIG["EPSILON_START"],
            epsilon_min   = CONFIG["EPSILON_MIN"],
            epsilon_decay = CONFIG["EPSILON_DECAY"],
            seed          = CONFIG["SEED"],
        )

        # 3. تدريب العميل
        print(f"  🧠 Training Agent on {maze_name}...")
        loop = TrainingLoop(
            env          = env,
            agent        = agent,
            n_episodes   = CONFIG["N_EPISODES"],
            log_interval = CONFIG["LOG_INTERVAL"],
            verbose      = False # خليناها False عشان الكونسول ميبقاش زحمة
        )
        metrics = loop.run()

        # 4. التقييم والأنيميشن
        optimal_path = agent.get_best_path(env)
        success      = optimal_path[-1] == env.exit_pos

        if success:
            print(f"  ✅ {maze_name} Solved! Optimal path length: {len(optimal_path)-1} steps.")
            animate_agent(env, optimal_path, maze_name)
        else:
            print(f"  ⚠️ Agent failed to find the exit for {maze_name}.")

        # 5. حفظ الرسوم البيانية باسم المتاهة عشان ميمسحوش بعض
        print(f"  📊 Generating Visualisations for {maze_name}...")
        W = CONFIG["SMOOTH_WINDOW"]

        plot_training_dashboard(metrics.episode_rewards, metrics.episode_steps,
                                metrics.epsilon_per_episode, metrics.td_errors_mean,
                                W, _out(f"{maze_name}_01_dashboard.png"))

        if success:
            render_maze_path(env.get_maze_copy(), optimal_path, env.start_pos,
                             env.exit_pos, title=f"Optimal Path - {maze_name}",
                             save_path=_out(f"{maze_name}_05_path.png"))

        render_q_value_heatmap(agent.q_table, env.get_maze_copy(), env.n_cols,
                               env.start_pos, env.exit_pos, title=f"Q-Value Heatmap - {maze_name}",
                               save_path=_out(f"{maze_name}_06_heatmap.png"))

    banner("🎉 ALL MAZES COMPLETED SUCCESSFULLY!")

    # فتح كل الرسوم البيانية للخرائط كلها في النهاية
    print("\n  📊 Displaying all plots. Close the windows to exit the program...")
    plt.show()

if __name__ == "__main__":
    main()