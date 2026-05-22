# Artificial Intelligence
# Expectimax

---

# Resource Limits
# ▪ # Problem: In realistic games, cannot search to leaves!
# ▪ # Solution: Depth# -# limited search
# ▪ # Instead, search only to a limited depth in the tree
# ▪ # Replace terminal utilities with an evaluation function for
# non# -# terminal positions
# ▪ # Example:
# ▪ # Suppose we have # 100 # seconds, can explore # 10# K nodes / sec
# ▪ # So can check # 1# M nodes per move
# ▪ # # -#  # reaches about depth # 8 # – # decent chess program
# ▪ # Guarantee of optimal play is gone
# ▪ # More plies makes a BIG difference
# ▪ # Use iterative deepening for an anytime algorithm 
## ? ## ? ## ? ## ?
## -## 1 ## -## 2 ## 4 ## 9
## 4
## min
## max
## -## 2 ## 4

---

# Evaluation Functions
# ▪ # Evaluation functions score non# -# terminals in depth# -# limited search
# ▪ # Ideal function: returns the actual # minimax # value of the position
# ▪ # In practice: typically weighted linear sum of features:
# ▪ # e.g. # f
### 1
# (# s# ) = (num white queens # – # num black queens)# , etc.

---

# Synergies between Evaluation Function and Alpha# -# Beta?
# ▪ # Alpha# -# Beta: amount of pruning depends on expansion ordering
# ▪ # Evaluation function can provide guidance to expand most promising nodes first
# (which later makes it more likely there is already a good alternative on the path to
# the root)
# ▪ # (somewhat similar to role of A* heuristic, CSPs filtering)
# ▪ # Alpha# -# Beta: (similar for roles of min# -# max swapped)
# ▪ # Value at a min# -# node will only keep going down
# ▪ # Once value of min# -# node lower than better option for max along path to root, can
# prune
# ▪ # Hence: IF evaluation function provides upper# -# bound on value at min# -# node, and
# upper# -# bound already lower than better option for max along path to root
# THEN can prune

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
5
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
5
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # -# ∞
# β # = # +# ∞

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
5
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # -# ∞
# β # = # 3

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # -# ∞
# β # = # 3
# α # < # β # => # continue
5

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
5
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # -# ∞
# β # = # 3

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # -# ∞
# β # = # 3
# α # < # β # => # continue
5

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
5
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # -# ∞
# β # = # 3

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # -# ∞
# β # = # 3
# α # < # β # => # continue
5

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
5
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # -# ∞
# β # = # 3

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # 3
# β # = # 3
5

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
5
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # 3
# β # = # +# ∞

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
5
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # 3
# β # = # 2

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # 3
# β # = # 2
# α # ≥ # β # => # prune # I, # J
5

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # 3
## pruned
5

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # 3
## pruned
5
# β # = # +# ∞

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # 3
## pruned
5
# β # = # 14

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # 3
## pruned
# β # = # 14
# α # < # β # => # continue
5

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # 3
## pruned
5
# β # = # 14

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # 3
## pruned
5
# β # = # 5

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # 3
## pruned
# β # = # 5
# α # < # β # => # continue
5

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # 3
## pruned
5
# β # = # 5

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # 3
## pruned
5
# β # = # 2

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Apply # α# -# β # pruning to calculate minimax # value # for # node # A.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # 3
## pruned
5

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Reverse # the # order of # the # utility # values # for # K, # L, # and # M.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## K
### 14
## L
### 5
## M
### 2
# α # = # 3
## pruned
6

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Reverse # the # order of # the # utility # values # for # K, # L, # and # M.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## M
### 2
## L
### 5
## K
### 14
# α # = # 3
## pruned
6

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Reverse # the # order of # the # utility # values # for # K, # L, # and # M.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## M
### 2
## L
### 5
## K
### 14
# α # = # 3
## pruned
6
# β # = # ∞

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Reverse # the # order of # the # utility # values # for # K, # L, # and # M.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## M
### 2
## L
### 5
## K
### 14
# α # = # 3
## pruned
6
# β # = # 2

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Reverse # the # order of # the # utility # values # for # K, # L, # and # M.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## M
### 2
## L
### 5
## K
### 14
# α # = # 3
## pruned
# β # = # 2
# α # ≥ # β # => # prune # L, # K
6

---

# Adversarial # search
# Example: # Effect # of # move # ordering # on # α# -# β # pruning
# Reverse # the # order of # the # utility # values # for # K, # L, # and # M.
## A
## B ## C ## D
## E
### 3
## F
### 12
## G
### 8
## H
### 2
## I
### 4
## J
### 6
## M
### 2
## L
### 5
## K
### 14
# α # = # 3
## pruned ## pruned
6

---

# Adversarial # search
# Effect # of # move # ordering on # α# -# β # pruning
## In ## the ## previous ## example, ## changing ## the ## order ## of ## nodes ## increases ## the ## efficiency ## of ## α## -## β
## pruning.
## Efficiency ## dependant ## on ## the ## ordering ## of ## children:
## Checks ## each ## of ## MAX## ’## s ## children ## until ## finding ## one with ## a ## value ## higher
## than ## β## .
## Checks ## each ## of ## MIN## ’## s ## children ## until ## finding ## one ## with ## a ## value lower
## than ## α## .
## Can use heuristics ## to order ## the nodes ## to check:
## Check ## the highest## -## value ## children first ## for ## MAX## .
## Check ## the ## lowest## -## value ## children ## first ## for ## MIN## .
## Good ordering can reduce time complexity to ## O## (## b
m/2
## )## , ## random ## ordering ## gives
## roughly ## O## (## b
3m/4
## )## , ## remember ## that ## Minimax ## is ## O## (## b
m
## )## .

---

# Uncertain Outcomes
# ▪ # Why do we care about uncertainty and randomness?
# ▪ # Want to model random events happening in the world
# ▪ # Build efficient algorithms with random sampling (Monte Carlo Tree
# Search)

---

# Worst# -# Case vs. Average Case
## 10 ## 10 ## 9 ## 100
## max
## min
# Idea: Uncertain outcomes controlled by chance, not an adversary!

---

# Expectimax # Search
# ▪ # Why wouldn# ’# t we know what the result of an action will be?
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
# ▪ # Later, we# ’# ll learn how to formalize the underlying uncertain# -
# result problems as # Markov Decision Processes
## 10 ## 4 ## 5 ## 7
## max
## chance
## 10 ## 10 ## 9 ## 100
## [Demo: min ## vs ## exp ## (L7D1,2)]

---

# Expectimax # Pseudocode
# def value(state):
# if the state is a terminal state: return the state’s utility
# if the next agent is # MAX# : return # max# -# value(state)
# if the next agent is # EXP# : return # exp# -# value(state)
# def exp# -# value(state):
# initialize v = # 0
# for each successor of state:
# p = probability(successor)
# v += p * # value(successor)
# return v
# def max# -# value(state):
# initialize v = # -# ∞
# for each successor of state:
# v = max(v, # value(successor)# )
# return v

---

# Expectimax # Pseudocode
# def exp# -# value(state):
# initialize v = # 0
# for each successor of state:
# p = probability(successor)
# v += p * # value(successor)
# return v # 5 # 7# 8 # 24 # -# 12
# 1# /# 2 
# 1# /# 3 
# 1# /# 6
# v = (# 1# /# 2# ) (# 8# ) + (# 1# /# 3# ) (# 24# ) + (# 1# /# 6# ) (# -# 12# ) = # 10

---

# Expectimax Example
## 12 ## 9 ## 6 ## 0## 3 ## 2 ## 15## 4 ## 6

---

# Expectimax Pruning?
## 12 ## 9## 3 ## 2

---

# Depth# -# Limited Expectimax
## …
## …
## 492 ## 362 
## …
## 400 ## 300
## Estimate of true
## expectimax ## value
## (which would
## require a lot of
## work to compute)

---

# Probabilities

---

# Reminder: Probabilities
# ▪ # A # random variable # represents an event whose outcome is unknown
# ▪ # A # probability distribution # is an assignment of weights to outcomes
# ▪ # Example: Traffic on freeway
## ▪ ## Random variable: T = whether there’s traffic
## ▪ ## Outcomes: T in {none, light, heavy}
## ▪ ## Distribution: P(T=none) = 0.25, P(T=light) = 0.50, P(T=heavy) = 0.25
# ▪ # Some laws of probability (more later):
## ▪ ## Probabilities are always non## -## negative
## ▪ ## Probabilities over all possible outcomes sum to one
# ▪ # As we get more evidence, probabilities may change:
## ▪ ## P(T=heavy) = 0.25, P(T=heavy | Hour=8am) = 0.60
## ▪ ## We’ll talk about methods for reasoning and updating probabilities later
# 0.25
# 0.50
# 0.25

---

# ▪ # The expected value of a function of a random variable is the
# average, weighted by the probability distribution over
# outcomes
# ▪ # Example: How long to get to the airport?
# Reminder: Expectations
# 0.25 # 0.50 # 0.25# Probability:
# 20 # min # 30 # min # 60 # min# Time:
# 35 min
## x ## x ## x
# + # +

---

# ▪ # In # expectimax # search, we have a probabilistic model
# of how the opponent (or environment) will behave in
# any state
# ▪ # Model could be a simple uniform distribution (roll a die)
# ▪ # Model could be sophisticated and require a great deal of
# computation
# ▪ # We have a chance node for any outcome out of our control:
# opponent or environment
# ▪ # The model might say that adversarial actions are likely!
# ▪ # For now, assume each chance node magically comes
# along with probabilities that specify the distribution
# over its outcomes
# What Probabilities to Use?
## Having a probabilistic belief about
## another agent’s action does not mean
## that the agent is flipping any coins!

---

# Quiz: Informed Probabilities
# ▪ # Let’s say you know that your opponent is actually running a depth 2 # minimax# , using the
# result 80% of the time, and moving randomly otherwise
# ▪ # Question: What tree search should you use?
## 0.1 ## 0.9
# ▪ # Answer: # Expectimax# !
# ▪ # To figure out EACH chance node# ’# s probabilities,
# you have to run a simulation of your opponent
# ▪ # This # kind of thing gets very slow very quickly
# ▪ # Even worse if you have to simulate your
# opponent simulating you# …
# ▪ # … # except for # minimax# , which # has the nice
# property that it all collapses into one game tree

---

# Modeling Assumptions

---

# The Dangers of Optimism and Pessimism
# Dangerous Optimism
## Assuming chance when the world is adversarial
# Dangerous Pessimism
## Assuming the worst case when it’s not likely

---

# Assumptions vs. Reality
## Adversarial ## Ghost ## Random ## Ghost
## Minimax
## Pacman
## Won 5/5
## Avg. ## Score: 483
## Won 5/5
## Avg. ## Score: 493
## Expectimax
## Pacman
## Won 1/5
## Avg. ## Score: ## -## 303
## Won 5/5
## Avg. ## Score: 503
## [Demos: world assumptions (L7D3,4,5,6)]
## Results from playing ## 5 ## games
## Pacman ## used depth ## 4 ## search with an ## eval ## function that avoids trouble
## Ghost used depth ## 2 ## search with an ## eval ## function that seeks ## Pacman

---

# Assumptions vs. Reality
## Adversarial ## Ghost ## Random ## Ghost
## Minimax
## Pacman
## Won 5/5
## Avg. ## Score: 483
## Won 5/5
## Avg. ## Score: 493
## Expectimax
## Pacman
## Won 1/5
## Avg. ## Score: ## -## 303
## Won 5/5
## Avg. ## Score: 503
## [Demos: world assumptions (L## 7## D## 3,4,5,6## )]
## Results from playing 5 games
## Pacman ## used depth 4 search with an ## eval ## function that avoids trouble
## Ghost used depth 2 search with an ## eval ## function that seeks ## Pacman

---

# Other Game Types

---

# Mixed Layer Types
# ▪ # E.g. Backgammon
# ▪ # Expectiminimax
# ▪ # Environment is an
# extra # “# random
# agent# ” # player that
# moves after each
# min/max agent
# ▪ # Each node
# computes the
# appropriate
# combination of its
# children

---

# Example: Backgammon
# ▪ # Dice rolls increase # b# : 21 possible rolls with 2 dice
# ▪ # Backgammon #  # 20 legal moves
# ▪ # Depth 2 = 20 x (21 x 20)
3 
# = 1.2 x 10
9
# ▪ # As depth increases, probability of reaching a given
# search node shrinks
# ▪ # So usefulness of search is diminished
# ▪ # So limiting depth is less damaging
# ▪ # But pruning is trickier…
# ▪ # Historic AI: # TDGammon # uses depth# -# 2 search + very
# good evaluation function + reinforcement learning:
# world# -# champion level play
# ▪ # 1
### st 
# AI world champion in any game!
### Image: Wikipedia

---

# Multi# -# Agent Utilities
# ▪ # What if the game is not zero# -# sum, or has multiple players?
# ▪ # Generalization of # minimax# :
# ▪ # Terminals have utility # tuples
# ▪ # Node values are also utility # tuples
# ▪ # Each player maximizes its own component
# ▪ # Can give rise to cooperation and
# competition dynamically…
## 1## ,## 6## ,## 6 ## 7## ,## 1## ,## 2 ## 6## ,## 1## ,## 2 ## 7## ,## 2## ,## 1 ## 5## ,## 1## ,## 7 ## 1## ,## 5## ,## 2 ## 7## ,## 7## ,## 1 ## 5## ,## 2## ,## 5
## 1## ,## 6## ,## 6 
## 6## ,## 1## ,## 2 
## 5## ,## 1## ,## 7 
## 5## ,## 2## ,## 5
## 1## ,## 6## ,## 6 ## 5## ,## 2## ,## 5
## 5## ,## 2## ,## 5

---

# Summary
# ▪ # Games require decisions when optimality is impossible
# ▪ # Bounded# -# depth search and approximate evaluation functions
# ▪ # Games force efficient use of computation
# ▪ # Alpha# -# beta pruning, MCTS
# ▪ # Game playing has produced important research ideas
# ▪ # Reinforcement learning (checkers)
# ▪ # Iterative deepening (chess)
# ▪ # Rational metareasoning (Othello)
# ▪ # Monte Carlo tree search (chess, Go)
# ▪ # Solution methods for partial# -# information games in economics (poker)
# ▪ # Video games present much greater challenges # – # lots to do!
# ▪ # b # = 10
### 500
# , # |# S# | = 10
### 4000
# , # m # = 10,000# , partially observable, often > 2 players

---

# Next Time: MDPs!
# Search # &
# Planning
# R# e# i# n# f# o# r# c# e# m# e# n# t
# Learning
# Probability # &
# Inference
# Sup# e# r# vi# s# e# d
# Learning
# How # can # I # find # rules # (# policy) # to # make # best
# decisions # for # any # situation?