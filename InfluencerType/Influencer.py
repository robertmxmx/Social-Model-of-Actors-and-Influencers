import random

class Influencer():
    #Factory for an influencer, will use the function given to generate a value which is expected to be between -1 and 1
    id = None
    BeliefAxis = 0

    def __init__(self,ID,Function,random,override):
        self.id = ID
        self.BeliefAxis = Function.picker(random,override)

