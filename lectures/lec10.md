# Artificial # Intelligence
# Reinforcement # Learning # II

---

# Reinforcement # Learning: # Overview # of # this # week
# Last # Lecture:
# ▪ # Passive # Reinforcement # Learning: # how # to # learn # from # already # given # experiences
# This # Lecture:
# ▪ # Active # Reinforcement # Learning: # how # to # collect # new # experiences
# ▪ # Approximate # Reinforcement # Learning: # to # handle # large # state # spaces
# ▪ # Case # studies: # game # playing, # robot # locomotion, language assistants

---

# Reinforcement # Learning
# ▪ # We # still # assume # an # MDP:
# ▪ # A # set # of # states # s #  # S
# ▪ # A # set # of actions # (per # state) # A
# ▪ # A # model # T(s,a,s’)
# ▪ # A # reward # function # R(s,a,s’)
# ▪ # Still # looking # for # a # policy # # (s)
# ▪ # New # twist: # don’t # know # T # or # R# , # so must # try out # actions
# ▪ # Big # idea: # Compute # all # averages # over # T # using sample # outcomes

---

# The # Story # So # Far: # MDPs # and # RL
# Go# al
# Known # MDP: # Offline # Solution
# Technique
## Compute ## V*, ## Q*, ## ## * ## Value ## / ## policy iteration
## Evaluate ## a ## fixed ## policy ##  ## Policy ## evaluation
# Unknown # MDP: # Model# -# Based # Unknown # MDP: # Model# -# Free
# Technique
## VI/PI ## on ## approx. ## MDP
# Goal
## Compute ## V*, Q*, ## ## *
## Evaluate ## a ## fixed policy ##  
## PE ## on ## approx. ## MDP
# T# e# c# hnique
## Q## -## learning
# Goal
## Compute ## V*, Q*, ## ## *
## Evaluate ## a ## fixed policy ##  
## Value ## Learning

---

# Model# -# Free # Learning
# ▪ # Model# -# free # (temporal # difference) # learning
# ▪ # Receive # stream of # experiences from the # world:
# ▪ # Update # estimates # each # transition
# a
# s
# s, # a
# r
# s’
# a’
# s# ’# , # a’
# s’’

---

# Model# -# Free # Learning
# ▪ # Model# -# free # (temporal # difference) # learning
# ▪ # Receive # stream of # experiences from the # world:
# ▪ # Update # estimates # each # transition
# a
# s
# s, # a
# r
# s’
# a’
# s# ’# , # a’
# s’’

---

# Model# -# Free # Learning
# ▪ # Model# -# free # (temporal # difference) # learning
# ▪ # Receive # stream of # experiences from the # world:
# ▪ # Update # estimates # each # transition
# a
# s
# s, # a
# r
# s’
# a’
# s# ’# , # a’
# s’’

---

# Model# -# Free # Learning
# ▪ # Model# -# free # (temporal # difference) # learning
# ▪ # Receive # stream of # experiences from the # world:
# ▪ # Update # estimates # each # transition
# a
# s
# s, # a
# r
# s’
# a’
# s# ’# , # a’
# s’’

---

# Model# -# Free # Learning
# ▪ # Model# -# free # (temporal # difference) # learning
# ▪ # Receive # stream of # experiences from the # world:
# ▪ # Update # estimates each # transition
# ▪ # Over # time, # updates # will # mimic # Bellman # updates
# a
# s
# s, # a
# r
# s’
# a’
# s# ’# , # a’
# s# ’’

---

# Q# -# L# e# a# rn# i# ng
# ▪ # Q# -# Iteration: # do # Q# -# value # updates # to # each # Q# -# state:
# ▪ # Initialize # Q
0
# (s,a) # = # 0, # then # iterate:
# ▪ # But can’t # compute # this # update # without # knowing # T, # R
# ▪ # Q# -# Learning: # Instead, # compute # average # as # we # go
# ▪ # Receive # a # sample # transition # (s,a,r,s’)
# ▪ # This # sample # suggests:
# ▪ # But we # want # to # average over # results # from # (s,a)
# ▪ # So # keep # a # running # average:

---

# Q# -# Learning # Properties
# ▪ # Amazing result: # Q# -# learning converges # to # optimal # policy # -- # even
# if you’re acting suboptimally!
# ▪ # Gives # us # optimal # way # to act! # # *(s) # = # argmax # Q(s,a)
## a
# ▪ # This is # called # off# -# policy # learning
# ▪ # Caveats:
# ▪ # You # have # to # explore # enough
# ▪ # You # have # to # eventually # make # the # learning # rate
# small # enough (but # not # decrease # it # too # quickly)
# ▪ # Basically, in # the # limit, # it doesn’t # matter # how you # select actions # (!)
## [Demo: ## Q## -## learning ## – ## auto ## – ## cliff ## grid ## (L11D1)]

---

# Video of Demo Q# -# Learning # -- # Gridworld

---

# Active # Reinforcement # Learning
## Acting according to policy ## # *(s) # = # argmax # Q(s,a)
## a

---

# Exploration # vs. # Exploitation

---

# Exploration # vs # exploitation
# ▪ # Exploration# : try new things
# ▪ # Exploitation# : do what’s best given what you’ve learned so far
# ▪ # Key point: pure exploitation often gets # stuck in a rut # and never
# finds an optimal policy!
### 15

---

# How # to # Explore?
# ▪ # Several # schemes for forcing # exploration
# ▪ # Simplest: # random # actions (# # -# greedy)
# ▪ # Every # time # step, # flip # a # coin
# ▪ # With # (small) # probability # # , # act # randomly
# ▪ # With # (large) # probability 1# -# # , act # on # current # policy
# ▪ # Problems # with # random actions?
# ▪ # You do # eventually explore the space, # but keep
# thrashing # around once # learning # is done
# ▪ # One # solution: # lower #  # over # time
# ▪ # Another solution: # exploration functions
## [Demo: ## Q## -## learning ## – ## manual ## exploration ## – ## bridge ## grid ## (L11D2)]
## [Demo: ## Q## -## learning ## – ## epsilon## -## greedy ## -- ## crawler ## (L11D3)]

---

# Demo Q# -# learning # – # Epsilon# -# Greedy # – # Crawler

---

# Exploration # Functions
# ▪ # When # to # explore?
# ▪ # Random # actions: # explore # a # fixed # amount
# ▪ # Better # idea: # explore # areas # whose # badness # is not
# (yet) # established, # eventually # stop # exploring
# ▪ # Exploration # function
# ▪ # Takes a # value estimate # u and a # visit count # n, and
# returns # an # optimistic # utility, e.g.
# Regular Q# -# Update:
# Modified # Q# -# Update:
# 𝑥 # ←
### 𝛼 
# 𝑣 # is # shorthand # for # 𝑥 # ← # 1 # − # 𝛼 𝑥 # + # 𝛼𝑣
## [Demo: ## exploration ## – ## Q## -## learning ## – ## crawler ## – ## exploration ## function ## (L11D4)]

---

# Demo Q# -# learning # – # Exploration Function # – # Crawler

---

# How # Can # we # Evaluate # Exploration # Methods?

---

# Re# gret
# !
# ▪ # Even if # you # learn the optimal policy,
# you # still make # mistakes # along the # way
# ▪ # Regret # is # a # measure # of # your total
# mistake # cost:
## ▪ ## Difference ## between ## all ## your ## (expected)
## rewards, ## including ## youthful ## suboptimality,
## and ## optimal ## (expected) ## rewards
# ▪ # Minimizing regret # goes # beyond
# learning # to # be # optimal # – # it requires
# optimally learning # to # be # optimal
# ▪ # For # example: # random exploration # and
# exploration functions both # end # up
# optimal, # but # random exploration has
# higher regret

---

# Are # We # Done?
# ▪ # Large # and # complex # state # spaces # are # still # a # problem!

---

# Approximate # Q# -# Learning

---

# Generalizing # Across # States
# ▪ # Basic # Q# -# Learning # keeps # a # table # of # all q# -# values
# ▪ # In realistic situations, we cannot possibly # learn
# about # every # single # state!
# ▪ # Too # many # states to # visit them # all in # training
# ▪ # Too # many # states # to # hold # the q# -# tables in # memory
# ▪ # Instead, # we # want # to # generalize:
# ▪ # Learn about # some # small # number # of # training # states # from
# experience
# ▪ # Generalize # that # experience # to # new, # similar # situations
# ▪ # This # is # a # fundamental # idea # in # machine # learning, # and # we’ll
# see # it # over # and over # again
### [demo ### – ### RL ### pacman]

---

# Recall # Lecture # 2: # State # Space # Sizes
# ▪ # World # state:
# ▪ # Agent # positions: # 120
# ▪ # Food # count: # 30
# ▪ # Ghost # positions: # 12
# ▪ # Agent # facing: # NSEW
# ▪ # How # many
# ▪ # World # states?
# 120x# (# 2
30
# )# x# (# 12
2
# )# x# 4
# ▪ # States # for # pathing?
# 120
# ▪ # States # for # eat# -# all# -# dots?
# 120x(2
30
# )

---

# Example: # Pacman
[Demo: Q-learning – pacman – tiny – watch all (L11D5)],[Demo: Q-learning – pacman – tiny – silent train (L11D6)], [Demo: Q-learning – pacman – tricky – watch all (L11D7)]
# Let’s # say # we # discover
# through # experience
# that # this # state # is # bad# :
# In # naïve # q# -# learning,
# we # know nothing
# about # this # state:
# Or # even # this # one!

---

# Demo Q# -# Learning # Pacman # – # Tiny # – # Watch All

---

# Demo Q# -# Learning # Pacman # – # Tiny # – # Silent Train

---

# Demo Q# -# Learning # Pacman # – # Tricky # – # Watch All

---

# Feature# -# Based # Representations
# ▪ # Solution: describe # a # state using # a # vector of
# features # (properties) # f
### 1
# , # f
### 2
# , # …
# ▪ # Features are # functions from # states to real # numbers
# (often # 0/1) # that # capture # important # properties # of # the
# state
# ▪ # Example # features:
## ▪ ## Distance ## to ## closest ## ghost
## ▪ ## Distance to closest ## dot
## ▪ ## Number ## of ## ghosts
## ▪ ## 1 ## / ## (dist ## to ## dot)
2
## ▪ ## Is ## Pacman in ## a ## tunnel? ## (0/1)
## ▪ ## …… ## etc.
## ▪ ## Is it ## the ## exact state ## on ## this slide?
# ▪ # Can # also # describe # a q# -# state (s, a) with features # (e.g.
# action # moves # closer to # food)

---

# Linear # Value # Functions
# ▪ # Using # a feature # representation # f
### 1
# , f
### 2
# , # … # we # can # write # a # q # function # (or # value # function)
# for # any # state # using # a # few # weights # w
### 1
# , w
### 2
# , # … :
# ▪ # Advantage: # our # experience # is # summed # up # in # a # few # powerful # numbers # w
### 1
# , w
### 2
# , # …
# ▪ # Disadvantage: # states may # share # features # but # actually # be # very different # in # value!
# ▪ # Ex: # these # two # states # would # have # the # same # value # if # we # don’t # include # ghost # positions # as a # feature:

---

# Approximate # Q# -# Learning
# ▪ # Q# -# learning # with linear Q# -# functions:
## Exact ## Q’s
## Approximate ## Q’s
# ▪ # Intuitive # interpretation:
# ▪ # Adjust # weights # of # active # features
# ▪ # E.g., # if # something unexpectedly bad # happens, # blame # the features # that # were # on:
# disprefer # all states with # that state’s features
# ▪ # Formal justification: online # least squares, # gradient # descent

---

# Example: # Q# -# Pacman
### [Demo: ### approximate ### Q### -
### learning ### pacman ### (L11D10)]

---

# Demo Approximate Q# -# Learning # -- # Pacman

---

# Policy # Search

---

# Policy # Search
# ▪ # Problem: # often # the # feature# -# based # policies # that work well (win # games, maximize
# utilities) # aren’t # the # ones # that # approximate # V # / # Q # best
# ▪ # Q# -# learning’s # priority: # get # Q# -# values # close # (modeling)
# ▪ # Action selection # priority: # get # ordering of # Q# -# values # right # (prediction)
# ▪ # We’ll see # this # distinction # between # modeling and # prediction # again # later in the # course
# ▪ # Solution: # learn # policies #  # that # maximize # rewards, # not the # Q # values # that predict # them
# ▪ # Policy # search: start with # an # ok solution # (e.g. Q# -# learning) # then # fine# -# tune # by # hill # climbing
# on # feature # weights

---

# Policy # Search
# ▪ # Simplest # policy # search:
# ▪ # Start # with # an # initial # linear # value # function # or Q# -# function
# ▪ # Nudge # each # feature # weight # up # and # down # and see # if # your policy is # better # than # before
# ▪ # Problems:
# ▪ # How # do # we # tell # the # policy # got # better?
# ▪ # Need # to # run # many # sample episodes!
# ▪ # If # there # are a # lot # of # features, # this # can # be # impractical
# ▪ # Better # methods # exploit # lookahead # structure, # sample wisely, # change
# multiple # parameters…
# ▪ # Policy # Gradient# , # Proximal # Policy # Optimization # (PPO) # are # examples

---

# Case # Studies # of # Reinforcement Learning!
# ▪ # Atari # game # playing
# ▪ # Robot # Locomotion
# ▪ # Language # assistants

---

# Case # Studies: # Atari # Game # Playing

---

# Case # Studies: # Atari # Game # Playing
# ▪ # MDP:
# ▪ # State: # image # of # game # screen
# ▪ # 256
84*84 
# possible # states
# ▪ # Processed with # hand# -# designed # feature # vectors or
# neural networks
# ▪ # Action: # combination # of # arrow # keys # + # button # (18)
# ▪ # Transition # T: # game # code # (don’t # have # access)
# ▪ # Reward R: # game score # (don’t # have # access)
# ▪ # Very # similar to # our # pacman # MDP
# ▪ # Use # approximate # Q # learning with neural
# networks and # ε# -# greedy # exploration to # solve
### [Human### -### level ### control ### through deep ### reinforcement ### learning,
### Mnih ### et ### al, ### 2015]

---

# Case # Studies: # Robot # Locomotion
# ▪ # MDP:
# ▪ # State: # image # of # robot camera # + N # joint angles # + # accelerometer # + …
# ▪ # Angles # are # N# -# dimensional # continuous # vector!
# ▪ # Processed # with # hand# -# designed # feature # vectors # or # neural # networks
# ▪ # Action: # N # motor commands # (continuous # vector!)
# ▪ # C# a# n’# t ea# s# ily # c# o# m# pu# te # ma# x # 𝑄# (# 𝑠# ′# , # 𝑎# ) # wh# en # 𝑎 # is c# on# ti# nuous
### 𝑎
# ▪ # Use # policy # search # methods # or # adapt # Q # learning # to # continuous # actions
# ▪ # Transition # T: # real # world (don’t # have # access)
# ▪ # Reward # R: # hand# -# designed # rewards
# ▪ # Stay # upright, # keep # forward # velocity, # etc
# ▪ # Learning # in # the real # world # may # be # slow and # unsafe
# ▪ # Build # a # simulator # and # learn # there # first, # then # deploy # in # real # world

---

# Case # Studies: Language # Assistants
### [### O### p### e### nAI### ]

---

# Case # Studies: Language # Assistants
# ▪ # Step # 1: # train # large # language # model # to mimic # human# -# written # text
# ▪ # Query: # “What # is # population # of # Berkeley?”
# ▪ # Human# -# like # completion: # “This # question # always # fascinated # me!”
# ▪ # Step # 2: # fine# -# tune # model # to # generate # helpful # text
# ▪ # Query: # “What # is # population # of # Berkeley?”
# ▪ # Helpful completion: # “It # is # 117,145 # as # of # 2021 # census”
# ▪ # Use # Reinforcement # Learning in # Step # 2

---

# Case # Studies: Language # Assistants
# ▪ # MDP:
# ▪ # State: # sequence # of # words # seen # so # far # (ex. ## “What ## is ## population ## of ## Berkeley? ## ”# )
# ▪ # 100,000
1,000 
# possible # states
# ▪ # Huge, but # can # be # processed # with # feature # vectors # or # neural # networks
# ▪ # Action: # next # word (ex. ## “## It”, ## “chair”, “purple”## , # …) # (so # 100,000 # actions)
# ▪ # Hard # to # compute # max
### 𝑎 
# 𝑄# (# 𝑠# ′, # 𝑎# ) # when # max # is # over # 100K actions!
# ▪ # Transition # T: # easy, # just # append # action word to # state # words
# ▪ # s: ## “My ## name“ # a: ## “is“ # s’: ## “My ## name ## is“
# ▪ # Reward # R: # ???
# ▪ # Humans # rate # model # completions # (ex. ### “What ### is ### population ### of ### Berkeley? ### ”# )
### ▪ ### “It ### is ### 117,145“: ### +1 ### “It ### is ### 5“: ### -### 1 ### “Destroy ### all ### humans“: ### -### 1
# ▪ # L# earn # a re# w# ard # m# od# el # 𝑅 # a# n# d # u# se # t# h# at # (# m# od# e# l# -# b# a# s# ed # R# L# )
# ▪ # Commonly # use # policy # search # (### Proximal ### Policy ### Optimization# ) # but # looking # into # Q # Learning

---

# Conclusion
# ▪ # We’re # done # with Part # I: # Search # and # Planning!
# ▪ # We’ve seen # how AI methods can solve
# problems # in:
# ▪ # Search
# ▪ # Constraint # Satisfaction # Problems
# ▪ # Games
# ▪ # Markov # Decision # Problems
# ▪ # Reinforcement # Learning
# ▪ # Next # up: # Part # II: # Uncertainty # and # Learning!