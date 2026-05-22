# CSE 326: Artificial Intelligence
# Markov Decision Processes

---

# Review: # Expectimax # Search
# ▪ # Uncertain outcomes controlled by chance, not an adversary
# ▪ # Why wouldn’t we know what the result of an action will be?
# ▪ # Explicit randomness: rolling dice
# ▪ # Unpredictable opponents: the ghosts respond randomly
# ▪ # Actions can fail: when moving a robot, wheels might slip
# ▪ # Values should now reflect average# -# case (# expectimax# )
# outcomes, not worst# -# case (# minimax# ) outcomes
# ▪ # Expectimax # search: # compute the average score under
# optimal play
# ▪ # Max nodes as in # minimax # search
# ▪ # Chance nodes are like min nodes but the outcome is uncertain
# ▪ # Calculate their # expected utilities
# ▪ # I.e. take weighted average (expectation) of children
# ▪ # Today, we’ll learn how to formalize the underlying uncertain# -
# result problems as # Markov Decision Processes
## 10 ## 4 ## 5 ## 7
## max
## chance
## 10 ## 10 ## 9 ## 100

---

# Non# -# Deterministic Search

---

# Reinforcement learning
# Atari (Minh et al, # Nature # 2015)

---

# Reinforcement learning

---

# Reinforcement learning
# Step 0
# Schulman, Wolski, Dhariwal, Radford, and Klimov, # 2017
# Schulman, Levine, Moritz, Jordan, and # Abbeel# , # 2015
# Video: Mukilan Krishnakumar

---

# Reinforcement learning
# Step 100

---

# Reinforcement learning
# Step 500

---

# Reinforcement learning
# Physical Intelligence, # 2024

---

# Reinforcement learning
# OpenAI, 2022

---

# Reinforcement learning
# DeGrave et al, # Nature# , 2022

---

# Example: Grid World
# ▪ # A maze# -# like problem
## ▪ ## The agent lives in a grid
## ▪ ## Walls block the agent’## s path
# ▪ # Noisy movement: # actions do not always go as planned
## ▪ ## 80% of the time, the action North takes the agent North
## (if there is no wall there)
## ▪ ## 10% of the time, North takes the agent West; 10% East
## ▪ ## If there is a wall in the direction the agent would have
## been taken, the agent stays put
# ▪ # The agent receives rewards each time step
## ▪ ## Small ## “living” reward each step (can be negative)
## ▪ ## Big rewards come at the end (good or bad)
# ▪ # Goal: maximize sum of rewards

---

# Grid World Actions
# Deterministic Grid World # Stochastic Grid World

---

# Markov Decision Processes
# ▪ # An MDP is defined by:
# ▪ # A # set of states s #  # S
# ▪ # A # set of actions a #  # A
# ▪ # A # transition function T(s, a, s# ’)
## ▪ ## Probability that a from s leads to s’, i.e., P(s## ’| s, a)
## ▪ ## Also called the model or the dynamics
# ▪ # A # reward function R(s, a, s# ’)
## ▪ ## Sometimes just R(s) or R(s## ’)
# ▪ # A # start state
# ▪ # Maybe a # terminal state
# ▪ # MDPs are non# -# deterministic search problems
# ▪ # One way to solve them is with # expectimax # search
# ▪ # We’# ll have a new tool soon

---

# What is Markov about MDPs?
# ▪ # “Markov” generally means that given the present state, the
# future and the past are independent
# ▪ # For Markov decision processes, # “Markov” means action
# outcomes depend only on the current state
# ▪ # This is just like search, where the successor function could only
# depend on the current state (not the history)
## Andrey ## Markov
## (1856## -## 1922)

---

# Policies
# Optimal policy when R(s, a, s# ’# ) = # -# 0.03
# for all non# -# terminals s
# ▪ # In deterministic single# -# agent search problems,
# we wanted an optimal # plan# , or sequence of
# actions, from start to a goal
# ▪ # For MDPs, we want an optimal # policy # # *: S → A
# ▪ # A policy #  # gives an action for each state
# ▪ # An optimal policy is one that maximizes
# expected utility if followed
# ▪ # An explicit policy defines a reflex agent
# ▪ # Expectimax # didn’t compute entire policies
# ▪ # It computed the action for a single state only

---

# Optimal Policies
## R(s) = ## -## 2.0## R(s) = 0.4
## R(s) = 0.03## R(s) = ## -## 0.01

---

# Example: Racing

---

# Example: Racing
# ▪ # A robot car wants to travel far, quickly
# ▪ # Three states: # Cool# , # Warm# , Overheated
# ▪ # Two actions: # Slow# , # Fast
# ▪ # Going faster gets double reward
# Cool
# Warm
# Overheated
## Fast
## Fast
## Slow
## Slow
## 0.5
## 0.5
## 0.5
## 0.5
## 1.0
## 1.0
## +1
## +## 1
## +1
## +2
## +2
## -## 10

---

# Example: Racing
## s ## a ## s' ## T(## s,a,s## ’) ## R(## s,a,s## ’)
## Slow ## 1.0 ## +1
## Fast ## 0.5 ## +2
## Fast ## 0.5 ## +2
## Slow ## 0.5 ## +1
## Slow ## 0.5 ## +1
## Fast ## 1.0 ## –## 10
## (end) ## 1.0 ## 0

---

# Racing Search Tree

---

# MDP Search Trees
# ▪ # Each MDP state projects an # expectimax# -# like search tree
## a
## s
## s## ’
## s, a
## (## s,a,s## ’## ) called a ## transition
## T(## s,a,s## ’## ) = P(s## ’## |## s,a## )
## R(## s,a,s## ’## )
## s,a,s## ’
## s is a ## state
## (s, a) is a
## q## -## state

---

# Utilities of Sequences

---

# Utilities of Sequences
# ▪ # What preferences should an agent have over reward sequences?
# ▪ # More or less?
# ▪ # Now or later?
# [1, 2, 2] # [2, 3, 4]# or
# [0, 0, 1] # [1, 0, 0]# or

---

# Discounting
# ▪ # It# ’# s reasonable to maximize the sum of rewards
# ▪ # It# ’# s also reasonable to prefer rewards now to rewards later
# ▪ # One solution: values of rewards decay exponentially
# Worth Now # Worth Next Step # Worth In Two Steps

---

# Discounting
# ▪ # How to discount?
# ▪ # Each time we descend a level, we
# multiply in the discount once
# ▪ # Why discount?
# ▪ # Sooner rewards probably do have
# higher utility than later rewards
# ▪ # Also helps our algorithms converge
# ▪ # Example: discount of 0.5
# ▪ # U([1,2,3]) = 1*1 + 0.5*2 + 0.25*3
# ▪ # U([3,2,1]) = 1*3 + 0.5*2 + 0.25*1
# ▪ # U([1,2,3]) < U([3,2,1])

---

# Stationary Preferences*
# ▪ # Theorem: if we assume # stationary preferences# :
# ▪ # Then: there are only two ways to define utilities
# ▪ # Additive utility:
# ▪ # Discounted utility:

---

# Infinite Utilities?!
# ▪ # Problem: What if the game lasts forever? Do we get infinite rewards?
# ▪ # Solutions:
# ▪ # Finite horizon: (similar to depth# -# limited search)
# ▪ # Terminate episodes after a fixed T steps (e.g. life)
# ▪ # Gives # nonstationary # policies (#  # depends on time left)
# ▪ # Discounting: use # 0 # < #  # < # 1
# ▪ # Smaller #  # means smaller # “# horizon# ” # – # shorter term focus
# ▪ # Absorbing state# : guarantee that for every policy, a terminal state will eventually
# be reached (like # “# overheated# ” # for racing)

---

# Recap: Defining MDPs
# ▪ # Markov decision processes:
# ▪ # Set of states S
# ▪ # Start state s
## 0
# ▪ # Set of actions A
# ▪ # Transitions P(# s# ’# |s,a# ) (or T(# s,a,s# ’# ))
# ▪ # Rewards R(# s,a,s# ’# ) (and discount # # )
# ▪ # MDP quantities so far:
# ▪ # Policy = Choice of action for each state
# ▪ # Utility = sum of (discounted) rewards
# a
# s
# s, a
# s,a,s# ’
# s# ’

---

# Solving MDPs

---

# Optimal Quantities
# ▪ # The value # (# utility) of a state s:
# V
## *
# (s) = expected utility starting in s and
# acting optimally
# ▪ # The value (utility) of a q# -# state (# s,a# ):
# Q
## *
# (# s,a# ) = expected utility starting out
# having taken action a from state s and
# (thereafter) acting optimally
# ▪ # The optimal policy:
# 
## *
# (s) = optimal action from state s
## a
## s
## s## ’
## s, a
# (s,a,s# ’# ) is a
# transition
## s,a,s## ’
# s is a
# state
# (s, a) is a
# q# -# state

---

# Snapshot of Demo # – # Gridworld # V Values
## Noise = ## 0
## Discount = ## 1
## Living reward = ## 0

---

# Snapshot of Demo # – # Gridworld # Q Values
## Noise = 0
## Discount = 1
## Living reward = 0

---

# Snapshot of Demo # – # Gridworld # V Values
## Noise = ## 0.2
## Discount = ## 1
## Living reward = ## 0

---

# Snapshot of Demo # – # Gridworld # Q Values
## Noise = ## 0.2
## Discount = ## 1
## Living reward = ## 0

---

# Snapshot of Demo # – # Gridworld # V Values
## Noise = ## 0.2
## Discount = ## 0.9
## Living reward = ## 0

---

# Snapshot of Demo # – # Gridworld # Q Values
## Noise = 0.2
## Discount = 0.9
## Living reward = 0

---

# Snapshot of Demo # – # Gridworld # V Values
## Noise = ## 0.2
## Discount = ## 0.9
## Living reward = ## -## 0.1

---

# Snapshot of Demo # – # Gridworld # Q Values
## Noise = ## 0.2
## Discount = ## 0.9
## Living reward = ## -## 0.1

---

# Values of States
# ▪ # Fundamental operation: compute the (# expectimax# ) value of a state
# ▪ # Expected utility under optimal action
# ▪ # Average sum of (discounted) rewards
# ▪ # This is just what # expectimax # computed!
# ▪ # Recursive definition of value:
# a
# s
# s, a
# s,a,s# ’
# s# ’

---

# Racing Search Tree

---

# Racing Search Tree

---

# Racing Search Tree
# ▪ # We# ’# re doing way too much
# work with # expectimax# !
# ▪ # Problem: States are repeated
# ▪ # Idea: Only compute needed
# quantities once
# ▪ # Problem: Tree goes on forever
# ▪ # Idea: Do a depth# -# limited
# computation, but with increasing
# depths until change is small
# ▪ # Note: deep parts of the tree
# eventually don# ’# t matter if # γ # < # 1

---

# Computing Time# -# Limited Values

---

# Time# -# Limited Values
# ▪ # Key idea: time# -# limited values
# ▪ # Define # V
### k
# (s) to be the optimal value of s if the game ends
# in k more time steps
# ▪ # Equivalently, it# ’# s what a depth# -# k # expectimax # would give from s

---

# k=# 0
## Noise = ## 0.2
## Discount = ## 0.9
## Living reward = ## 0

---

# k=1
## Noise = ## 0.2
## Discount = ## 0.9
## Living reward = ## 0

---

# k=# 2
## Noise = 0.2
## Discount = 0.9
## Living reward = 0

---

# k=# 3
## Noise = ## 0.2
## Discount = ## 0.9
## Living reward = ## 0

---

# k=# 4
## Noise = ## 0.2
## Discount = ## 0.9
## Living reward = ## 0

---

# k=5
## Noise = ## 0.2
## Discount = ## 0.9
## Living reward = ## 0

---

# k=# 6
## Noise = 0.2
## Discount = 0.9
## Living reward = 0

---

# k=# 7
## Noise = ## 0.2
## Discount = ## 0.9
## Living reward = ## 0

---

# k=# 8
## Noise = ## 0.2
## Discount = ## 0.9
## Living reward = ## 0

---

# k=9
## Noise = ## 0.2
## Discount = ## 0.9
## Living reward = ## 0

---

# k=# 10
## Noise = 0.2
## Discount = 0.9
## Living reward = 0

---

# k=# 11
## Noise = ## 0.2
## Discount = ## 0.9
## Living reward = ## 0

---

# k=# 12
## Noise = ## 0.2
## Discount = ## 0.9
## Living reward = ## 0

---

# k=100
## Noise = ## 0.2
## Discount = ## 0.9
## Living reward = ## 0

---

# Value Iteration

---

# Value Iteration
# ▪ # Start with V
### 0
# (s) = # 0# : no time steps left means an expected reward sum of zero
# ▪ # Given vector of # V
### k
# (s) values, do one ply of # expectimax # from each state:
# ▪ # Repeat until convergence
# ▪ # Complexity of each iteration: O(S
### 2
# A)
# ▪ # Theorem: will converge to unique optimal values
# ▪ # Basic idea: approximations get refined towards optimal values
# ▪ # Policy may converge long before values do
## a
## V
k+1
## (s)
## s, a
## s,a,s## ’
## V
k
## (## s## ’## )

---

# Example: Value Iteration
## Assume no discount!
## s ## a ## s' ## T(## s,a,s## ’) ## R(## s,a,s## ’)
## Slow ## 1.0 ## +1
## Fast ## 0.5 ## +2
## Fast ## 0.5 ## +2
## Slow ## 0.5 ## +1
## Slow ## 0.5 ## +1
## Fast ## 1.0 ## –## 10
## (end) ## 1.0 ## 0

---

# Example: Value Iteration
# 0 # 0 # 0
# 2 # 1 # 0
# 3.5 # 2.5 # 0
## Assume no discount!

---

# Next Time: Policy# -# Based Methods