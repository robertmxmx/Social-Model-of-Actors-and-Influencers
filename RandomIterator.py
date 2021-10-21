import random
class RandomIterator:
    Initial_Seed = None
    Last_Number = None
    def __init__(self,initial_seed):
        self.Initial_Seed = initial_seed
        random.seed(initial_seed)
        self.Last_Number = random.random()

    def next(self):
        random.seed(self.Last_Number)
        self.Last_Number = random.random()
        return self.Last_Number