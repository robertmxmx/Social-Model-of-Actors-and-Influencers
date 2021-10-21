import random
def Picker(Actor_List,Opinion_List,Time_Since_Last_Interaction,Number_Of_Previous_Interaction,random_iterator):
    #picks 2 actors randomly without replacment from the list of actors
    random.seed(random_iterator.next())
    return random.sample(range(len(Actor_List)),2)