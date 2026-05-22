# Artificial # Intelligence
# Reinforcement # Learning # I

---

# Reinforcement # Learning

---

# Example: Samuel’s checker player (1956# -# 67)

---

# Example: Learning to Walk
# Initial
## [Kohl and Stone, ICRA 2004]

---

# Example: Learning to Walk
# Finished
## [Kohl and Stone, ICRA 2004]

---

# Example: # Sidewinding
## [Andrew Ng] ## [Video: SNAKE ## – ## climbStep+sidewinding## ]

---

# Example: Breakout (DeepMind)
## [© ## TwoMinuteLectures## ]

---

# Example: AlphaGo (2016)

---

# The # Crawler!

---

# Video # of # Demo # Crawler # Bot

---

# Quadruped # Robot # Learning # in # Berkeley Hills
## [Smith ## et ## al, ## 2022]

---

# Reinforcement # Learning: # An # Overview
# ▪ # Passive # Reinforcement # Learning: # how # to # learn # from # already # given # experiences
# ▪ # Model# -# based: # learn # the # MDP model # from # experiences, # then # solve # the # MDP
# ▪ # Model# -# free: # forego # learning the # MDP model, # directly # learn # V # or # Q
# ▪ # Value # learning: # learns # value of # a # fixed policy
# ▪ # 2 # approaches: # Direct # Evaluation # & # Temporal Difference (# TD# ) # Learning
# ▪ # Q # learning: # learns # Q # values of # the # optimal policy # (Q version # of # TD # Learning)
# ▪ # Active # Reinforcement # Learning: # how # to # collect # new # experiences
# ▪ # Approximate # Reinforcement # Learning: # to # handle # large # state # spaces
# ▪ # Case # studies: # game playing, # robotics, # language # assistants

---

# Reinforcement # Learning
# ▪ # Still assume a Markov decision process (MDP):
# ▪ # A set of states # s #  # S
# ▪ # A set of actions (per state) # A# (# s# )
# ▪ # A transition model # T# (# s# ,# a# ,# s# ’# )
# ▪ # A reward function # R# (# s# ,# a# ,# s# ’# )
# ▪ # Still looking for a policy # # (# s# )

---

# Reinforcement # Learning
# ▪ # Still assume a Markov decision process (MDP):
# ▪ # A set of states # s #  # S
# ▪ # A set of actions (per state) # A# (# s# )
# ▪ # A transition model # T# (# s# ,# a# ,# s# ’# )
# ▪ # A reward function # R# (# s# ,# a# ,# s# ’# )
# ▪ # Still looking for a policy # # (# s# )
# ▪ # New twist: # don# ’t know # T # or # R
# ▪ # I.e. # we # don’t know # which # states # are # good # or what the # actions # do
# ▪ # Must # actually try out # actions # and # states # to # learn

---

# Reinforcement # Learning
# ▪ # Still assume a Markov decision process (MDP):
# ▪ # A set of states # s #  # S
# ▪ # A set of actions (per state) # A# (# s# )
# ▪ # A transition model # T# (# s# ,# a# ,# s# ’# )
# ▪ # A reward function # R# (# s# ,# a# ,# s# ’# )
# ▪ # Still looking for a policy # # (# s# )
# ▪ # New twist: # don# ’t know # T # or # R
# ▪ # I.e. # we # don’t know # which # states # are # good # or what the # actions # do
# ▪ # Must # actually try out # actions # and # states # to # learn
# Actions: # a
# State: # s
# Reward: # r
# A# g# e# n# t
# Environment

---

# Offline # (MDPs) # vs. # Online # (RL)
# Offline # Solution:
# Compute # policy # ahead
# of # time
# Online # Learning:
# Compute # policy # as
# experience # comes # in

---

# Passive Reinforcement Learning
# ▪ # Simplified task: policy evaluation
# ▪ # Input: a fixed policy # # (# s# )
# ▪ # You don’t know # T # and # R
# ▪ # Goal: learn the state values # V
### 
# (# s# )

---

# Passive # Reinforcement # Learning
# ▪ # Simplified # task: policy # evaluation
# ▪ # Input: # a # fixed # policy # # (s)
# ▪ # You # don’t # know # the # transitions # T(s,a,s’)
# ▪ # You # don’t # know # the # rewards # R(s,a,s’)
# ▪ # Goal: # learn # the # state # values
# ▪ # In # this # case:
# ▪ # Learner # is # “along # for # the # ride”
# ▪ # No # choice # about # what # actions # to # take
# ▪ # Just # execute the policy # and # learn # from # experience
# ▪ # This # is # NOT # offline # planning! # You # actually # take actions # in # the # world.

---

# Model# -# Based # Learning

---

# Model# -# Based # Learning
# ▪ # Model# -# Based # Idea:
# ▪ # Learn # an # approximate # model # based # on # experiences
# ▪ # Solve # for # values as if # the # learned # model # were # correct
# ▪ # Step # 1: # Learn # empirical # MDP # model
# ▪ # Count # outcomes # s’ # for # each # s, # a
# ▪ # Normalize to # give # an # estimate # of
# ▪ # Discover # each # when # we # experience (s, # a, # s’)
# ▪ # Step # 2: # Solve # the # learned # MDP
# ▪ # For # example, # use # value # iteration, # as # before

---

# Example: # Model# -# Based # Learning
# Input # Policy #  # Observed # (s, # a, # s’, # R) # Transitions # Learned # Model
## Assume: ##  ## = ## 1
# A
# B # C # D
# E
# Episode # 1
# B, # east, # C, # -# 1
# C, east, # D, # -# 1
# D, # exit, # x, # +10
# Episode # 4
# E, # north, # C, # -# 1
# C, # east, # A, # -# 1
# A, # exit, # x, # -# 10
# Episode # 2
# B, # east, # C, # -# 1
# C, east, # D, # -# 1
# D, # exit, # x, # +10
# Episode # 3
# E, # north, # C, # -# 1
# C, # east, # D, # -# 1
# D, # exit, # x, # +10
# T(B, # east, # C) # = # 1.00
# T(C, # east, # D) # = # 0.75
# T(C, # east, # A) # = # 0.25
# …
# R(B, # east, # C) # = # -# 1
# R(C, # east, # D) # = # -# 1
# R(D, # exit, # x) # = # +10
# …

---

# Analogy: # Expected # Age
# Goal: # Compute # expected age # of # cs# e326 # students
# Known # P(A)
# Without # P(A), # instead # collect # samples # [a
### 1
# , a
### 2
# , # … # a
### N
# ]
# Unknown # P(A): # “Model # Based” # Unknown # P(A): # “Model # Free”
# Why # does # this
# work? # Because
# samples # appear
# with the # right
# frequencies.
# Why # does # this
# work? # Because
# eventually # you
# learn the # right
# model.

---

# Model# -# Free # Learning

---

# Basic idea of model# -# free methods
# ▪ # To approximate expectations with respect to a distribution, you
# can either
# ▪ # Estimate the distribution from samples, compute an expectation
# ▪ # Or, bypass the distribution and estimate the expectation from samples
# directly

---

# Direct evaluation
# ▪ # Goal: Estimate # V
## 
# (# s# )# , i.e., expected total discounted
# reward from # s # onwards
# ▪ # Idea:
# ▪ # Use # returns# , the # actual # sums of discounted rewards from # s
# ▪ # Average over multiple trials and visits to # s
# ▪ # This is called # direct evaluation # (or direct utility
# estimation)

---

# Direct # Evaluation
# ▪ # This # is # called # direct # or # Monte# -# Carlo # evaluation
# 𝑁 
## i
# 𝑉 𝑠 # ← 
# 1 
# 𝑠𝑎𝑚𝑝𝑙𝑒 # (# 𝑠# )
# ▪ # Goal: Compute # values # for # each # state # under # 
# ▪ # Idea: Average # together # observed # sample # values
# ▪ # Act # according # to # 
# ▪ # Every # time you visit # a # state, write down what the
# sum of discounted # rewards turned # out to # be from
# that # state # until the # end # of # the # episode:
# 𝑠𝑎𝑚𝑝𝑙𝑒
## i 
# 𝑠 # = # 𝑅 𝑠 # + # 𝛾𝑅 𝑠
## " 
# + # 𝛾
## 2
# 𝑅 𝑠
## "" 
# + # …
# ▪ # Average # those # samples:

---

# Example: Direct Estimation
# Input Policy # 
## Assume: ##  ## = 1
# Observed Episodes (Training) # Output Values
# A
# B # C # D
# E
# B# , # east# , # C# , # -# 1
# C# , # east# , # D# , # -# 1
# D# , # exit# , # x# , +10
# B# , # east# , # C# , # -# 1
# C# , # east# , # D# , # -# 1
# D# , # exit# , # x# , +10
# E# , # north# , # C# , # -# 1
# C# , # east# , # A# , # -# 1
# A# , # exit# , # x# , # -# 10
# Episode 1 # Episode 2
# Episode 3 # Episode 4
# E# , # north# , # C# , # -# 1
# C# , # east# , # D# , # -# 1
# D# , # exit# , # x# , +10
# A
# B # C # D
# E
# +8 # +4 # +10
# -# 10
# -# 2

---

# Example: # Direct # Evaluation
# Input # Policy # 
## Assume: ##  ## = ## 1
# Observed # (s, # a, # s’, # R) # Transitions # Output # Values
# A
# B # C # D
# E
# Episode # 1
# B, # east, # C, # -# 1
# C, east, # D, # -# 1
# D, # exit, # x, # +10
# Episode # 4
# E, # north, # C, # -# 1
# C, # east, # A, # -# 1
# A, # exit, # x, # -# 10
# Episode # 2
# B, # east, # C, # -# 1
# C, east, # D, # -# 1
# D, # exit, # x, # +10
# Episode # 3
# E, # north, # C, # -# 1
# C, # east, # D, # -# 1
# D, # exit, # x, # +10
# -# 10
# A
# +8
# B 
# +4
# C 
# +10
# D
# -# 2
# E
# V(s) # is sum of # discounted # rewards # from # s # until # the # end, # averaged # over # all # encounters # of # s

---

# Problems # with # Direct # Evaluation
# ▪ # What’s # good about # direct # evaluation?
# ▪ # It’s # easy # to # understand
# ▪ # It # doesn’t # require # any # knowledge of # T, # R
# ▪ # It eventually # computes the # correct # average # values,
# using # just # sample # transitions
# ▪ # What # bad # about # it?
# ▪ # It # wastes # information # about # state # connections
# ▪ # Need # to # have # all # episodes ahead of # time # (cannot
# “stream” # in transitions)
# Output # Values
# -# 10
# A
# 0
# B 
# 0
# C 
# +10
# D
# 0
# E
# If # B # and # E # both go # to # C
# under # this # policy, # how # can
# their # values # be # different?

---

# Temporal difference (TD) learning

---

# Why # Not # Use # Policy # Evaluation?
# ▪ # Simplified # Bellman # updates # calculate # V # for # a # fixed # policy:
# ▪ # Each round, # replace # V # with # a # one# -# step# -# look# -# ahead # layer over V
# s
# # (s)
# s, # # (s)
# s, # # (s),s’
# s’
# ▪ # This # approach # fully # exploited # the # connections # between # the # states
# ▪ # Unfortunately, # we # need # T # and # R # to # do # it!
# ▪ # Key # question: # how # can # we # do # this # update # to # V # without # knowing # T # and # R?
# ▪ # In other # words, # how to we # take # a # weighted # average # without knowing # the # weights?

---

# Sample# -# Based # Policy # Evaluation?
# ▪ # We want # to # improve our # estimate # of # V by # computing these averages:
# ▪ # Idea: # Take # samples # of # outcomes # s’ # (by # doing # the # action!) # and # average
## Known ## P(A):
## Unknown P(A): ## “Model ## Free”

---

# Sample# -# Based # Policy # Evaluation?
## s
2
## ' ## s
3
## '
# ▪ # We want # to # improve our # estimate # of # V by # computing these averages:
# ▪ # Idea: # Take # samples # of # outcomes # s’ # (by # doing # the # action!) # and # average
## s
## ## (s)
## s, ## ## (s)
## s, ## ## (s),s’
## s'
1
## '
# Almost! # But we can’t
# rewind # time # to # get # sample
# after # sample # from # state # s.

---

# Temporal # Difference # Learning
# ▪ # Big # idea: # learn # from # every # experience!
# ▪ # Update # V(s) each # time # we # experience # a transition # (s, # a, # s’, # r)
# ▪ # Likely # outcomes # s’ # will # contribute # updates # more # often
# ▪ # Temporal # difference # learning # of # values
# ▪ # Policy # still # fixed, # still # doing # evaluation!
# ▪ # Move # values # toward # value # of # whatever # successor # occurs: # running # average
# # (s)
# s
# s, # # (s)
# s’
# Sample # of # V(s):
# Update # to # V(s):
# Same # update:
# 0 # < # ⍺ # < # 1

---

# Exponential # Moving # Average
# ▪ # Traditional # Average:
# ▪ # Need # to # have # all # N # samples # at # once # (cannot “stream” in samples)
# ▪ # Exponential # moving # average
# ▪ # The # running # interpolation # update:
# ▪ # Makes # recent # samples # more # important:
# ▪ # Forgets # about the # past # samples (how quickly # depends # on # ⍺# )
# ▪ # Decreasing # learning # rate # ⍺ # can # give converging # averages
# 0 # < # ⍺ # < # 1

---

# Example: Temporal Difference Learning
## Assume: ##  ## = 1, ## α ## = 1/2
# Observed Transitions
# B# , # east# , # C# , # -# 2
# 0
# 0 # 0 # 8
# 0
# 0
# -# 1 # 0 # 8
# 0
# 0
# -# 1 # 3 # 8
# 0
# C# , # east# , # D# , # -# 2
# A
# B # C # D
# E
# States
# B# , # east# , # C# , # -# 2
# C# , # east# , # D# , # -# 2
## V(S=B)=0, V(S’=C)=0, ## ½ *0 + ½ * [ ## -## 2 + 1*0] = ## -## 1
## V(S=C)=0, V(S’=D)=8, ## ½ *0 + ½ * [ ## -## 2 + 1*8] = 3

---

# Problems # with # TD # Value # Learning
# ▪ # What # can # we # do?
# ▪ # Learn # Q# -# values, # not # values
# ▪ # Makes # action selection model# -# free # too!
# ▪ # TD # value # leaning # is # a # model# -# free # way # to # do # policy # evaluation
# ▪ # However, # if # we want # to turn # values # into # a # (new) # policy, # we’re # stuck:
# s
# a
# s, # a
# s# ,a,# s# ’
# s# ’

---

# Q# -# Value # Iteration
# ▪ # Value # iteration: # find # successive # (depth# -# limited) # values
# ▪ # Start # with # V
0
# (s) # = # 0, # which # we know # is # right
# ▪ # Given # V
k
# , # calculate the # depth # k+1 # values # for # all states:
# ▪ # But # Q# -# values # are # more # useful, # so # compute # them # instead
# ▪ # Start # with # Q
0
# (s,a) = # 0, which we # know # is # right
# ▪ # Given # Q
k
# , # calculate the # depth # k+1 # q# -# values # for # all q# -# states:

---

# Q# -# L# e# a# rn# i# ng
## [Demo: ## Q## -## learning ## – ## gridworld ## (L10D2)]
## [Demo: ## Q## -## learning ## – ## crawler ## (L10D3)]
# ▪ # Q# -# Learning: sample# -# based # Q# -# value # iteration
# ▪ # Learn # Q(s,a) # values as you go
# ▪ # Receive # a # sample # (s,a,s’,r)
# ▪ # Consider # your # old # estimate:
# ▪ # Consider # your # new # sample # estimate:
## no ## longer ## policy
## evaluation!
# ▪ # Incorporate # the # new # estimate # into # a # running # average:

---

# Video of Demo Q# -# Learning # -- # Gridworld

---

# Video of Demo Q# -# Learning # -- # Crawler

---

# Q# -# Learning # Properties
# ▪ # Amazing result: # Q# -# learning converges # to # optimal # policy # -- # even
# if you’re acting suboptimally!
# ▪ # This is # called # off# -# policy # learning
# ▪ # Caveats:
# ▪ # You # have # to # explore # enough
# ▪ # You # have # to # eventually # make # the # learning # rate
# small # enough
# ▪ # … # but # not # decrease # it # too # quickly
# ▪ # Basically, in # the # limit, # it doesn’t # matter # how you # select actions # (!)

---

# Active # Reinforcement # Learning

---

# Active # Reinforcement # Learning
# ▪ # Full # reinforcement # learning: # optimal # policies # (like value iteration)
# ▪ # You # don’t # know # the # transitions # T(s,a,s’)
# ▪ # You # don’t # know # the # rewards # R(s,a,s’)
# ▪ # You # choose # the # actions # now
# ▪ # Goal: # learn # the # optimal # policy # / # values
# ▪ # In # this # case:
# ▪ # Learner # makes # choices!
# ▪ # Fundamental # tradeoff: # exploration vs. # exploitation
# ▪ # This # is # NOT # offline # planning! # You # actually take actions in the world # and
# find # out # what # happens…

---

# What # we # did # today # (a # lot!)
# + # 𝛾
### 2
# 𝑅 𝑠
### "" 
# + # …
# ▪ # Focused # on # Passive # Reinforcement # Learning # problem
# ▪ # How # to # learn # from # already # given # experiences # when # we # don# ’# t # know # T # and # R
# ▪ # Saw # distinction # between # model# -# based # and # model# -# free # approaches # to # RL
# ▪ # Model# -# Based: # Learn # a # model # of # T # and # R # from # experiences, # then # solve # MDP
# ▪ # Model# -# Free: # Learn # from # experience # samples # without # building # a # model
# ▪ # Direct # evaluation # was our # first attempt # at # model# -# free # value # learning
# ▪ # Estimate # values # from # samples # of # discounted # sums # of # rewards: # sample # = # 𝑅 𝑠 # + # 𝛾𝑅 𝑠
### "
# ▪ # Issue # 1# : # Does # not # take # advantage # of # state # connections
# ▪ # Issue # 2# : # Needs # to # see # all # transitions # at # once
# ▪ # Introduced # TD # Learning # as # a # way to # address # two # issues # above
# ▪ # Solution # 1# : # Use # V(s) # when # calculating value # samples: # sample # = # 𝑅 𝑠 # + # 𝛾𝑉
### 𝜋
# (# 𝑠
### "
# )
# ▪ # Solution 2: # Use # Exponential # Moving # Average # to # build up # averages # one # transition at a time
# ▪ # New # issue: # TD # Learning only learns # state # values # – # can’t # use # it # to # pick # optimal # actions!
# ▪ # Solution is # Q# -# Learning: # learn Q # values # instead # of # V # with # TD# -# like # update
# ▪ # Now # can # pick # optimal # actions, # so # get # an # optimal # model# -# free # policy

---

# Next # Time: # Active # & # Approximate # RL!