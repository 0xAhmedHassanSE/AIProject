# Artificial # Intelligence
# Markov # Decision # Processes # II

---

# To# day
# ▪ # Review # MDPs, # Bellman # equation, # value # iteration
# ▪ # Policy # extraction, # policy # evaluation, # policy # iteration
# ▪ # All # based # on the Bellman # equation

---

# Example: # Grid # World
# ▪ # A # maze# -# like # problem
## ▪ ## The ## agent ## lives ## in ## a ## grid
## ▪ ## Walls ## block ## the ## agent’s ## path
# ▪ # Noisy movement: # actions # do # not # always # go # as # planned
## ▪ ## 80% ## of ## the ## time, ## the ## action ## North ## takes ## the ## agent ## North
## ▪ ## 10% of ## the ## time, ## North ## takes ## the ## agent ## West; ## 10% ## East
## ▪ ## If ## there ## is ## a ## wall ## in ## the ## direction ## the ## agent ## would ## have
## been ## taken, ## the ## agent ## stays ## put
# ▪ # The # agent # receives # rewards # each # time # step
## ▪ ## Small ## “living” ## reward ## each ## step ## (can ## be ## negative)
## ▪ ## Big ## rewards ## come ## at ## the ## end ## (good or ## bad)
# ▪ # Goal: # maximize # sum # of # (discounted) # rewards

---

# Recap: # MDPs
# ▪ # Markov # decision # processes:
# ▪ # States # S
# ▪ # Actions # A
# ▪ # Transitions # P(s’|s,a) # (or # T(s,a,s’))
# ▪ # Rewards # R(s,a,s’) # (and # discount # # )
# ▪ # Start # state # s
### 0
# s
# a
# s, # a
# T(s,a,s# ’# )
# s# ’

---

# Recap: # MDPs
# s
# a
# s, # a
# T(s,a,s’)
# s# ’
# ▪ # Markov decision processes:
# ▪ # States S
# ▪ # Actions A
# ▪ # Transitions P(s’|s,a) (or T(s,a,s’))
# ▪ # Rewards R(s,a,s’) (and discount # # )
# ▪ # Start state s
### 0
# ▪ # Quantities:
# ▪ # Policy = map of states to actions
# ▪ # Utility = sum of discounted rewards
# ▪ # Values = expected future utility from a state (max node)
# ▪ # Q# -# Values = expected future utility from a q# -# state (chance node)

---

# Solving # MDPs

---

# Optimal # Quantities
# ▪ # The # value # (utility) # of # a # state # s:
# V
## *
# (s) # = # expected utility starting in # s # and
# acting # optimally
# ▪ # The # value # (utility) of # a # q# -# state # (s,a):
# Q
## *
# (s,a) # = # expected # utility # starting # out
# having taken action # a # from state # s # and
# (thereafter) acting # optimally
# ▪ # The # optimal # policy:
# 
## *
# (s) # = # optimal action from # state # s
## a
## s
## s’
## s, ## a
# (s,a,s’) # is # a
# transition
## T(s,a,s)## ’
# s # is # a # state
# (s, # a) # is # a # q# -
# state
# V
### *
# (s)
# Q
### *
# (s,a)

---

# Optimal # Quantities
# ▪ # The # value # (utility) # of # a # state # s:
# V
## *
# (s) # = # expected utility starting in # s # and
# acting optimally
# ▪ # The # value # (utility) of # a # q# -# state # (s,a):
# Q
## *
# (s,a) # = # expected # utility # starting # out
# having taken action # a # from state # s # and
# (thereafter) acting # optimally
# ▪ # The # optimal # policy:
# 
## *
# (s) # = # optimal # action # from # state # s
## Here ## V*(s) ## is ## a ## lookup ## table ## with ## 11 ## entries

---

# Optimal # Quantities
# ▪ # The # value # (utility) # of # a # state # s:
# V
## *
# (s) # = # expected utility starting in # s # and
# acting # optimally
# ▪ # The # value # (utility) of # a # q# -# state # (s,a):
# Q
## *
# (s,a) # = # expected # utility # starting # out
# having taken action # a # from state # s # and
# (thereafter) acting # optimally
# ▪ # The # optimal # policy:
# 
## *
# (s) # = # optimal # action # from # state # s
## Here ## Q*(s,a) ## is a ## lookup ## table ## with ## 9*4+2 ## entries

---

# Optimal # Quantities
# ▪ # The # value # (utility) # of # a # state # s:
# V
## *
# (s) # = # expected utility starting in # s # and
# acting # optimally
# ▪ # The # value # (utility) of # a # q# -# state # (s,a):
# Q
## *
# (s,a) # = # expected # utility # starting # out
# having taken action # a # from state # s # and
# (thereafter) acting # optimally
# ▪ # The # optimal # policy:
# 
## *
# (s) # = # optimal action from # state # s
## Here ## 
*
## (s) ## is ## a ## lookup ## table ## with ## 11 ## entries

---

# The # Bellman # Equations
# How # to # be # optimal:
# Step # 1: # Take # correct # first # action
# Step # 2: # Keep # being # optimal

---

# The # Bellman # Equations
# ▪ # Definition # of # “optimal # utility” # via # expectimax
# recurrence # gives # a # simple one# -# step # lookahead
# relationship # amongst # optimal utility values
# ▪ # These are the Bellman # equations, # and # they # characterize
# optimal # values # in # a # way # we’ll # use # over and # over
# s
# a
# s, # a
# T(s,a,s# ’# )
# s# ’
# V
### *
# (s)
# Q
### *
# (s,a)

---

# Value Iteration
# ▪ # Bellman equations # characterize # the optimal values:
# ▪ # Value iteration # computes # them:
# ▪ # Value iteration is just a fixed point solution method
# ▪ # … though the # V
k 
# vectors are also interpretable as time# -# limited values
## a
## V(s)
## s, a
## s,a,s## ’
## V(## s## ’## )

---

# Value # Iteration
# ▪ # Start # with V
### 0
# (s) # = # 0: # no # time # steps # left # means # an # expected # reward # sum # of # zero
# ▪ # Given vector # of # V
### k
# (s) values, # do # one # step # of # expectimax # from # each # state:
# ▪ # Repeat # until # convergence, # which yields # V*
# ▪ # Complexity # of # each # iteration: # O(S
### 2
# A)
# ▪ # Theorem: # will # converge to # unique # optimal # values
# ▪ # Basic # idea: # approximations # get # refined # towards # optimal # values
# ▪ # Policy # may # converge # long # before # values # do
## V
k+1
## (s)
## a
## s, ## a
## s## ,a,## s## ’
## V
k
## (s## ’## )

---

# k=# 0
## Noise ## = ## 0.2
## Discount ## = ## 0.9
## Living ## reward ## = ## 0

---

# k=1

---

# k=1
## V
1
## ( ## )
## V
1
## (s) ## is value ## of ## depth## -## 1
## expectimax from ## s

---

# k=# 1
## V
1
## ( ## )
## V
1
## (s) ## is value ## of ## depth## -## 1
## expectimax from ## s

---

# k=2
## V
2
## ( ## )
## V
2
## (s) ## is value ## of ## depth## -## 2
## expectimax from ## s

---

# k=# 3
## Noise ## = ## 0.2
## Discount ## = ## 0.9
## Living ## reward ## = ## 0

---

# k=4
## Noise ## = ## 0.2
## Discount ## = ## 0.9
## Living ## reward ## = ## 0

---

# k=5
## Noise ## = ## 0.2
## Discount ## = ## 0.9
## Living ## reward ## = ## 0

---

# k=6
## Noise ## = ## 0.2
## Discount ## = ## 0.9
## Living ## reward ## = ## 0

---

# k=# 7
## Noise ## = ## 0.2
## Discount ## = ## 0.9
## Living ## reward ## = ## 0

---

# k=8
## Noise ## = ## 0.2
## Discount ## = ## 0.9
## Living ## reward ## = ## 0

---

# k=9
## Noise ## = ## 0.2
## Discount ## = ## 0.9
## Living ## reward ## = ## 0

---

# k=1# 0
## Noise ## = ## 0.2
## Discount ## = ## 0.9
## Living ## reward ## = ## 0

---

# k=# 1# 1
## Noise ## = ## 0.2
## Discount ## = ## 0.9
## Living ## reward ## = ## 0

---

# k=1# 2
## Noise ## = ## 0.2
## Discount ## = ## 0.9
## Living ## reward ## = ## 0

---

# k=1# 0# 0
## Noise ## = ## 0.2
## Discount ## = ## 0.9
## Living ## reward ## = ## 0

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
# ▪ # A robot car wants to travel far, quickly
# ▪ # Three states: # Cool# , # Warm# , Overheated
# ▪ # Two actions: # Slow# , # Fast
# ▪ # Going faster gets double reward

---

# Example: # Value # Iteration
# 0 # 0 # 0
## Assume ## no ## discount!

---

# Example: # Value # Iteration
# 0 # 0 # 0
## Assume ## no ## discount!
# a# =# sl# o# w# : # 1(1 # + # 0) # = # 1
# a=fast: # 0.5(2 # + # 0) # + # 0.5(2 # + # 0) # = # 2
# ?

---

# Example: # Value # Iteration
# 0 # 0 # 0
## Assume ## no ## discount!
# a# =# sl# o# w# : # 0.5(1 # + # 0) # + # 0.5(1 # + # 0) # = # 1
# a=fast: # 1(# -# 10 # + # 0) # = # -# 10
# 2 # ?

---

# Example: # Value # Iteration
# 0 # 0 # 0
# 2 # 1 # 0
# ?
## Assume ## no ## discount!
# a# =# sl# o# w# : # 1(1 # + # 2) # = # 3
# a=fast: # 0.5(2 # + # 2) # + # 0.5(2 # + # 1) # = # 3.5

---

# Example: # Value # Iteration
# 0 # 0 # 0
# 2 # 1 # 0
# 3.# 5 # ? # 0
## Assume ## no ## discount!
# a# =# sl# o# w# : # 0.5(1 # + # 2) # + # 0.5(1 # + # 1) # = # 2.5
# a=fast: # 1(# -# 10 # + # 0) # = # -# 10

---

# Example: # Value # Iteration
# 0 # 0 # 0
# 2 # 1 # 0
# 3.# 5 # 2.# 5 # 0
## Assume ## no ## discount!

---

# Value # Iteration
# ▪ # Bellman # equations # characterize # the # optimal # values:
# ▪ # Value # iteration # computes # them:
# ▪ # Value # iteration # is # just # a # fixed # point solution # method
# ▪ # … # though # the V
k 
# vectors # are # also # interpretable # as # time# -# limited # values
# ▪ # There # may # be # other # methods # to # solve # this # Bellman # equation
## a
## s, ## a
## V(## s## )
## T(s,a,s’)
## V(## s## ’)

---

# Quiz: # Bellman # equation # for # Q # values?
# ▪ # We # saw # Bellman # equation # that characterized # optimal # V*(s)
# s
# a
# s, # a
# ▪ # Can # we write down # Bellman # equation # for # Q*(s,a)# ?
# T(s,a,s’)
# s’
# a’
# s# ’# , # a’
# Q*(s, # a)
# Q*(s’, # a’)
## (don’t ## look ## at ## the ## next ## slide ## if ## you’re
## following ## along ## with ## the ## notes ## please ## :)

---

# Quiz: # Bellman # equation # for # Q # values?
# a
# s, # a
# ▪ # Can # we write down # Bellman # equation # for # Q*(s,a)# ?
# T(s,a,s’)
# s’
# a’
# s# ’# , # a’
# Q*(s, # a)
# Q*(s’, # a’)
# ▪ # Leads # to # Q# -# Value # iteration # algorithm # we’ll see next week
# ▪ # We # saw # Bellman # equation # that characterized # optimal # V*(s)
# s

---

# Policy # Extraction

---

# Computing Actions from Values
# ▪ # Let’s imagine we have the optimal values V*(s)
# ▪ # How should we act?
# ▪ # It’s not obvious!
# ▪ # We need to do a mini# -# expectimax # (one step)
# ▪ # This is called # policy extraction# , since it gets the policy implied by the values
## ex:
## max ## [0.5, ## 1.7, ## 1.2] ## = ## 1.7
## argmax ## [0.5, ## 1.7, ## 1.2] ## = ## 1
## argmax return index
"argmax" returns the index or argument corresponding to the maximum value in a sequence.

---

# Computing Actions from Q# -# Values
# ▪ # Let’s imagine we have the optimal q# -# values:
# ▪ # How should we act?
# ▪ # Completely trivial to decide!
# ▪ # Important lesson: actions are easier to select from q# -# values than values!

---

# Problems # with # Value # Iteration
# ▪ # Value # iteration repeats the # Bellman updates:
# ▪ # Problem # 1: # It’s # slow # – # O(S
## 2
# A) # per # iteration
# ▪ # Problem # 2: # The “max” # at # each # state rarely # changes
# ▪ # Problem # 3: # The # policy often # converges # long # before # the # values
# s
# a
# s, # a
# s# ,a,# s# ’
# s# ’

---

# k=1# 2
## Noise ## = ## 0.2
## Discount ## = ## 0.9
## Living ## reward ## = ## 0

---

# k=1# 0# 0
## Noise ## = ## 0.2
## Discount ## = ## 0.9
## Living ## reward ## = ## 0

---

# Policy # Methods

---

# Policy # Evaluation

---

# Fixed # Policies
# s# ,a,# s# ’ 
# s, # # (s),s’
# s’ # s’
# ▪ # Expectimax # trees # max # over # all # actions to # compute # the # optimal # values
# ▪ # If we # fixed # some # policy # # (s), # then # the # tree # would # be # simpler # – # only one # action # per # state
# ▪ # … # though # the tree’s # value # would depend # on which policy we # fixed
# Do # the # optimal # action
# s
# a
# s, # a
# Do # what #  # says # to # do
# s
# # (s)
# s, # # (s)

---

# Utilities for # a # Fixed # Policy
# ▪ # Another basic operation: compute the utility of a state s under a fixed
# (generally non# -# optimal) policy
# ▪ # Define # the utility of # a # state # s, # under # a # fixed # policy # # :
# V

# (s) # = # expected # total # discounted # rewards # starting # in s # and # following # 
# ▪ # What # is the # recursive # relation # (one# -# step # look# -# ahead # / # Bellman
# equation)?
# ▪ # Hint: # recall # Bellman # equation # for # optimal # policy:
# s
# # (s)
# s, # # (s)
# s, # # (s),s’
# s# ’

---

# Utilities for # a # Fixed # Policy
# ▪ # Define # the utility of # a # state # s, # under # a # fixed # policy # # :
# V

# (s) # = # expected # total # discounted # rewards # starting # in s # and # following # 
# ▪ # What # is the # recursive # relation # (one# -# step # look# -# ahead # / # Bellman
# equation)?
# ▪ # Hint: # recall # Bellman # equation # for # optimal # policy:
# ▪ # Answer:
# s
# # (s)
# s, # # (s)
# s, # # (s),s’
# s# ’

---

# Policy # Evaluation
# ▪ # How # do # we calculate the # V’s # for # a # fixed # policy # # ?
# ▪ # Idea # 1: # Turn # recursive Bellman equations into # updates
# (like value # iteration)
# s
# # (s)
# s, # # (s)
# s, # # (s),s’
# s’
# ▪ # Efficiency: # O(S
### 2
# ) # per # iteration
# ▪ # Idea # 2: # Without the # maxes, # the # Bellman # equations # are # just # a # linear # system
# ▪ # Solve # with # your favorite # linear # system # solver 
## V
 
## (s
1
## )
## V
 
## (s
2
## )
## …
# x # =

---

# Example: # Policy # Evaluation
# Always # Go # Right # Always # Go # Forward

---

# Example: # Policy # Evaluation
# Always # Go # Right # Always # Go # Forward

---

# Policy # Iteration

---

# Policy Iteration
# ▪ # Alternative approach for optimal values:
# ▪ # Step 1: Policy evaluation: # calculate utilities for some fixed policy (not optimal
# utilities!) until convergence
# ▪ # Step 2: Policy improvement: # update policy using one# -# step look# -# ahead with resulting
# converged (but not optimal!) utilities as future values
# ▪ # Repeat steps until policy converges
# ▪ # This is # policy iteration
# ▪ # It’s still optimal!
# ▪ # Can converge (much) faster under some conditions

---

# Policy # Iteration
# ▪ # Evaluation: # For # fixed # current # policy # # , # find # values # with policy evaluation:
# ▪ # Iterate # until values # converge:
# ▪ # End # up # with # value # function
# ▪ # Improvement: # For # fixed # values, # get # a better # policy # using # policy # extraction
# ▪ # One# -# step # look# -# ahead:
# ▪ # Repeat # steps # until # policy converges

---

# Comparison
# ▪ # Both # value # iteration # and # policy # iteration # compute # the # same # thing (all # optimal values)
# ▪ # In # value # iteration:
# ▪ # Every # iteration updates both the # values # and # (implicitly) the # policy
# ▪ # We # don’t # track # the # policy, # but # taking # the # max # over actions # implicitly # recomputes # it
# ▪ # In # policy # iteration:
# ▪ # We # do # several # passes # that # update # utilities # with # fixed # policy # (each # pass # is # fast # because # we
# consider # only # one # action, # not # all # of # them)
# ▪ # After # the # policy # is # evaluated, # a # new # policy # is # chosen (slow # like # a # value # iteration # pass)
# ▪ # The new # policy # will # be # better # (or # we’re # done)
# ▪ # Both # are # dynamic # programs # for # solving # MDPs

---

# Summary: # MDP # Algorithms
# ▪ # So # you # want # to….
# ▪ # Compute # optimal values: use # value # iteration # or # policy # iteration
# ▪ # Compute # values # for a # particular policy: use # policy evaluation
# ▪ # Turn # your # values # into # a # policy: use # policy # extraction # (one# -# step lookahead)
## Value ## Iteration # V* ## Policy ## Iteration # V*## or
## Policy ## Evaluation # V
π
# π
## Policy ## Extraction # π
V
# V

---

# Summary: # MDP # Algorithms
# ▪ # So # you # want # to….
# ▪ # Compute # optimal values: use # value # iteration # or # policy # iteration
# ▪ # Compute # values # for # a # particular policy: # use # policy evaluation
# ▪ # Turn # your # values # into # a # policy: use # policy extraction # (one# -# step # lookahead)
# ▪ # These # all # look the # same!
# ▪ # They # basically # are # – # they # are # all # variations # of # Bellman # updates
# ▪ # They # all # use # one# -# step # lookahead # expectimax fragments
# ▪ # They # differ # only in # whether # we # plug # in # a # fixed # policy or max # over # actions

---

# Summary: Bellman # Equation # Zoo!

---

# How # to # be # optimal:
# Step # 1: # Take # correct # first # action
# Step # 2: # Keep # being # optimal
# The # Bellman # Equations
# “# J# o# u# r# n# ey# o# f # a# t# h# o# u# s# a# n# d # o# p# t# i# m# al # s# t# e# p# s # be# g# i# n# s # w# i# t# h # a# f# i# r# s# t # o# p# t# i# m# al # s# t# e# p# ”

---

# Double Bandits

---

# Double# -# Bandit MDP
# ▪ # Actions: # Blue# , # Red
# ▪ # States: # Win# , Lose
# W # L
# $1
# 1.0
# $1
# 1.0
# 0.25 # $0
# 0.75
# $2
# 0.75 # $2
# 0.25
# $0
# No discount
# 100 time steps
# Both states have
# the same value

---

# Offline Planning
# ▪ # Solving MDPs is offline planning
# ▪ # You determine all quantities through computation
# ▪ # You need to know the details of the MDP
# ▪ # You do not actually play the game!
# Play Red
# Play Blue
# Value
# No discount
# 100 time steps
# Both states have
# the same value
# 150
# 100
# W # L
# $1
# 1.0
# $1
# 1.0
# 0.25 # $0
# 0.75
# $2
# 0.75 # $2
# 0.25
# $0

---

# Let’s Play!
# $2 # $2 # $0 # $2 # $2
# $2 # $2 # $0 # $0 # $0

---

# Online Planning
# ▪ # Rules changed! Red’s win chance is different.
# W # L
# $1
# 1.0
# $1
# 1.0
# ?? # $0
# ??
# $2
# ?? # $2
# ??
# $0

---

# Let’s Play!
# $0 # $0 # $0 # $2 # $0
# $2 # $0 # $0 # $0 # $0

---

# What Just Happened?
# ▪ # That wasn’t planning, it was learning!
# ▪ # Specifically, reinforcement learning
# ▪ # There was an MDP, but you couldn’t solve it with just computation
# ▪ # You needed to actually act to figure it out
# ▪ # Important ideas in reinforcement learning that came up
# ▪ # Exploration: you have to try unknown actions to get information
# ▪ # Exploitation: eventually, you have to use what you know
# ▪ # Regret: even if you learn intelligently, you make mistakes
# ▪ # Sampling: because of chance, you have to try things repeatedly
# ▪ # Difficulty: learning can be much harder than solving a known MDP

---

# Next # Time: Reinforcement # Learning!