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
    "Maze_1_Standard": np.array([
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

    "Maze_2_Tricky": np.array([
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    ]),

    "Maze_3_Expert": np.array([
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 1, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
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
from matplotlib.widgets import Button

def animate_agent(env, sample_paths, optimal_path, maze_name, initial_mode):
    """دالة لعمل أنيميشن مع زرار للتبديل بين التعلم والمسار النهائي"""
    print(f"\n  🎬 Starting Animation for {maze_name} (Mode: {initial_mode})...")
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.canvas.manager.set_window_title(f"{maze_name} - Agent Animation") # منع ظهور كلمة Figure 1
    plt.subplots_adjust(bottom=0.2) # مكان للزرار
    
    state = {'mode': initial_mode, 'running': True}
    ax_btn = plt.axes([0.3, 0.05, 0.4, 0.075])
    btn = Button(ax_btn, 'Skip to Final' if initial_mode == 'learning' else 'Show Learning')
    
    def on_click(event):
        state['mode'] = 'final' if state['mode'] == 'learning' else 'learning'
        btn.label.set_text('Skip to Final' if state['mode'] == 'learning' else 'Show Learning')
        state['running'] = False # يقطع اللوب الحالية ويبدأ التانية
    
    btn.on_clicked(on_click)

    while True:
        state['running'] = True
        if state['mode'] == 'final':
            for step, pos in enumerate(optimal_path):
                if not state['running'] or not plt.fignum_exists(fig.number): break
                ax.clear()
                maze_img = env.get_maze_copy().astype(float)
                maze_img[pos[0], pos[1]] = 0.5
                ax.imshow(maze_img, cmap='Set3', interpolation='nearest')
                ax.set_xticks([x - 0.5 for x in range(env.n_cols + 1)], minor=True)
                ax.set_yticks([y - 0.5 for y in range(env.n_rows + 1)], minor=True)
                ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.5)
                ax.text(env.start_pos[1], env.start_pos[0], 'S', ha="center", va="center", color="green", fontweight="bold", fontsize=14)
                ax.text(env.exit_pos[1], env.exit_pos[0], 'E', ha="center", va="center", color="red", fontweight="bold", fontsize=14)
                ax.set_title(f"[{maze_name}] Expert (Final Optimal Path)\nStep: {step}/{len(optimal_path)-1}", fontsize=13, fontweight="bold")
                ax.set_xticks([]); ax.set_yticks([])
                plt.pause(0.15)
            
            if state['running']: plt.pause(1.5) # خلص بنجاح
            
        else:
            for ep_num, path in sample_paths.items():
                if not state['running'] or not plt.fignum_exists(fig.number): break
                for step, pos in enumerate(path):
                    if not state['running'] or not plt.fignum_exists(fig.number): break
                    ax.clear()
                    maze_img = env.get_maze_copy().astype(float)
                    maze_img[pos[0], pos[1]] = 0.5
                    ax.imshow(maze_img, cmap='Set3', interpolation='nearest')
                    ax.set_xticks([x - 0.5 for x in range(env.n_cols + 1)], minor=True)
                    ax.set_yticks([y - 0.5 for y in range(env.n_rows + 1)], minor=True)
                    ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.5)
                    ax.text(env.start_pos[1], env.start_pos[0], 'S', ha="center", va="center", color="green", fontweight="bold", fontsize=14)
                    ax.text(env.exit_pos[1], env.exit_pos[0], 'E', ha="center", va="center", color="red", fontweight="bold", fontsize=14)
                    ax.set_title(f"[{maze_name}] Learning Progression (Episode {ep_num})\nStep: {step}/{len(path)-1}", fontsize=13, fontweight="bold")
                    ax.set_xticks([]); ax.set_yticks([])
                    plt.pause(0.02) # سريع جدا عشان الملل
                if state['running']: plt.pause(0.5)
            
            # لما يخلص التعلم أوتوماتيك يقلب على الفاينال
            if state['running']:
                state['mode'] = 'final'
                btn.label.set_text('Show Learning')
                continue
                
        if not plt.fignum_exists(fig.number): break

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

import tkinter as tk
from tkinter import messagebox

def get_user_config_gui():
    root = tk.Tk()
    root.title("🤖 Maze RL - Setup Configuration")
    window_width = 450
    window_height = 350
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.configure(bg="#f4f4f9")
    
    # Variables
    alpha_var = tk.StringVar(value=str(CONFIG["ALPHA"]))
    gamma_var = tk.StringVar(value=str(CONFIG["GAMMA"]))
    episodes_var = tk.StringVar(value=str(CONFIG["N_EPISODES"]))
    mode_var = tk.StringVar(value="final")
    
    tk.Label(root, text="Welcome to Maze RL Solver!", font=("Segoe UI", 16, "bold"), bg="#f4f4f9", fg="#2c3e50").pack(pady=15)
    
    frame = tk.Frame(root, bg="#f4f4f9")
    frame.pack(pady=10)
    
    tk.Label(frame, text="Alpha (Learning Rate):", bg="#f4f4f9", font=("Segoe UI", 10)).grid(row=0, column=0, sticky='e', pady=5, padx=5)
    tk.Entry(frame, textvariable=alpha_var, font=("Segoe UI", 10), width=10).grid(row=0, column=1, pady=5, sticky='w')
    
    tk.Label(frame, text="Gamma (Discount Factor):", bg="#f4f4f9", font=("Segoe UI", 10)).grid(row=1, column=0, sticky='e', pady=5, padx=5)
    tk.Entry(frame, textvariable=gamma_var, font=("Segoe UI", 10), width=10).grid(row=1, column=1, pady=5, sticky='w')
    
    tk.Label(frame, text="Total Episodes:", bg="#f4f4f9", font=("Segoe UI", 10)).grid(row=2, column=0, sticky='e', pady=5, padx=5)
    tk.Entry(frame, textvariable=episodes_var, font=("Segoe UI", 10), width=10).grid(row=2, column=1, pady=5, sticky='w')
    
    tk.Label(frame, text="Animation Mode:", bg="#f4f4f9", font=("Segoe UI", 10)).grid(row=3, column=0, sticky='e', pady=5, padx=5)
    modes_frame = tk.Frame(frame, bg="#f4f4f9")
    modes_frame.grid(row=3, column=1, sticky='w')
    tk.Radiobutton(modes_frame, text="Show Expert (Final Path)", variable=mode_var, value="final", bg="#f4f4f9").pack(anchor='w')
    tk.Radiobutton(modes_frame, text="Show Learning Progression", variable=mode_var, value="learning", bg="#f4f4f9").pack(anchor='w')
    
    user_choices = {}
    def on_start():
        try:
            user_choices['ALPHA'] = float(alpha_var.get())
            user_choices['GAMMA'] = float(gamma_var.get())
            user_choices['N_EPISODES'] = int(episodes_var.get())
            user_choices['mode'] = mode_var.get()
            root.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers!")
            
    tk.Button(root, text="🚀 Start Training", font=("Segoe UI", 12, "bold"), bg="#4CAF50", fg="white", command=on_start, cursor="hand2", padx=20).pack(pady=20)
    
    root.mainloop()
    
    if not user_choices:
        print("Setup cancelled by user.")
        exit()
        
    return user_choices

from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def show_tabbed_results(maze_name, fig_path, fig_heat, fig_dash):
    root = tk.Tk()
    root.title(f"{maze_name} - Comprehensive Analysis")
    
    # بما إننا عملنا الرسومات Responsive، مش محتاجين نفتحها Full Screen إجباري
    # هنفتحها بحجم مناسب (1300x800) ونسنترها في الشاشة بالظبط
    window_width = 1300
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    root.configure(bg="white")
    
    style = ttk.Style()
    style.theme_use('default')
    style.configure('TNotebook.Tab', padding=[20, 10], font=('Segoe UI', 12, 'bold'))
    style.configure('TNotebook', background='white')
    
    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, padx=10, expand=True, fill='both')
    
    # ── التاب الأول: Path & Heatmap ──
    tab1 = tk.Frame(notebook, bg="white")
    notebook.add(tab1, text="📍 1. Optimal Path & Heatmap")
    
    # استخدام grid لضمان المساواة 50/50 بين الرسمتين عند تغيير حجم النافذة (Responsive)
    tab1.columnconfigure(0, weight=1)
    tab1.columnconfigure(1, weight=1)
    tab1.rowconfigure(0, weight=1)
    
    f1 = tk.Frame(tab1, bg="white")
    f1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    canvas1 = FigureCanvasTkAgg(fig_path, master=f1)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    toolbar1 = NavigationToolbar2Tk(canvas1, f1)
    toolbar1.update()
    
    f2 = tk.Frame(tab1, bg="white")
    f2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    canvas2 = FigureCanvasTkAgg(fig_heat, master=f2)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    toolbar2 = NavigationToolbar2Tk(canvas2, f2)
    toolbar2.update()
    
    # ── التاب التاني: Dashboard ──
    tab2 = tk.Frame(notebook, bg="white")
    notebook.add(tab2, text="📈 2. Training Metrics Dashboard")
    
    canvas3 = FigureCanvasTkAgg(fig_dash, master=tab2)
    canvas3.draw()
    canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    toolbar3 = NavigationToolbar2Tk(canvas3, tab2)
    toolbar3.update()
    
    # لتأكيد قفل النافذة بالكامل والخروج من الـ mainloop عشان الكود يكمل للمتاهة اللي بعدها
    def on_closing():
        root.quit()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

def main() -> None:
    banner("Welcome to Maze RL Solver!")
    
    # ── واجهة تفاعلية GUI للمستخدم ──
    user_config = get_user_config_gui()
    
    # تحديث القيم
    CONFIG["ALPHA"] = user_config['ALPHA']
    CONFIG["GAMMA"] = user_config['GAMMA']
    CONFIG["N_EPISODES"] = user_config['N_EPISODES']
    initial_mode = user_config['mode']
    num_samples = 5

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
            verbose      = False, # خليناها False عشان الكونسول ميبقاش زحمة
            num_samples  = num_samples
        )
        metrics = loop.run()

        # 4. التقييم والأنيميشن
        optimal_path = agent.get_best_path(env)
        success      = optimal_path[-1] == env.exit_pos

        if success:
            print(f"  ✅ {maze_name} Solved! Optimal path length: {len(optimal_path)-1} steps.")
            # الأنيميشن التفاعلي بالزرار
            animate_agent(env, metrics.sample_paths, optimal_path, maze_name, initial_mode)
        else:
            print(f"  ⚠️ Agent failed to find the exit for {maze_name}.")

        # 5. حفظ الرسوم البيانية باسم المتاهة عشان ميمسحوش بعض
        print(f"  📊 Generating Visualisations for {maze_name}...")
        W = CONFIG["SMOOTH_WINDOW"]

        dash_img_path = _out(f"{maze_name}_01_dashboard.png")
        path_img_path = _out(f"{maze_name}_05_path.png")
        heat_img_path = _out(f"{maze_name}_06_heatmap.png")

        fig_dash = plot_training_dashboard(metrics.episode_rewards, metrics.episode_steps,
                                metrics.epsilon_per_episode, metrics.td_errors_mean,
                                W, dash_img_path)
        if success:
            fig_path = render_maze_path(env.get_maze_copy(), optimal_path, env.start_pos,
                             env.exit_pos, title=f"Optimal Path - {maze_name}",
                             save_path=path_img_path)

        fig_heat = render_q_value_heatmap(agent.q_table, env.get_maze_copy(), env.n_cols,
                               env.start_pos, env.exit_pos, title=f"Q-Value Heatmap - {maze_name}",
                               save_path=heat_img_path)

        # تنبيه للمستخدم عشان يقفل النافذة ويكمل للمتاهة اللي بعدها
        print(f"\n  📊 Displaying Analysis Tabs for {maze_name}.")
        print("  🛑 IMPORTANT: You MUST close the tabbed window to continue to the next maze...")

        # عرض نافذة بايثون أصلية (Tkinter) بتابات مدمج فيها الزوم
        show_tabbed_results(maze_name, fig_path, fig_heat, fig_dash)
        
        # بعد قفل النافذة، بنقفل الرسومات من الذاكرة
        plt.close(fig_dash)
        if success:
            plt.close(fig_path)
        plt.close(fig_heat)

        # 6. حفظ جدول الـ Q-Table في ملف Excel/CSV عشان نشوف الأرقام بعنينا
        csv_path = _out(f"{maze_name}_08_Q_Table.csv")
        if csv_path:
            np.savetxt(csv_path, agent.q_table, delimiter=",", fmt="%.4f", header="UP,DOWN,LEFT,RIGHT", comments="")
            print(f"  💾 Saved Q-Table to {csv_path}")

        # هنا خلاص شيلنا plt.show() لأن التابات قايمة بالواجب

    banner("🎉 ALL MAZES COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()