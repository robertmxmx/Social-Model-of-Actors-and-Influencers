import random
def Picker(Actor_List,Opinion_List,Time_Since_Last_Interaction,Number_Of_Previous_Interaction,random_iterator):
    #applies a weight to each actor so that actors will prefer to interact with those they have a bond with and prefer not to interact with actors they have a negative bond with
    random.seed(random_iterator.next())
    actor_one_index = random.sample(range(len(Actor_List)),1)[0]
    opinion_line = Opinion_List[actor_one_index][:]

    for i in range(len(opinion_line)):
        if i != actor_one_index:
            opinion_line[i] += 1
    random_value =  random_iterator.next()*sum(opinion_line)

    for i in range(1,len(opinion_line)):
            opinion_line[i] += opinion_line[i-1]

    for i in range(1,len(opinion_line)):
        if random_value < opinion_line[i]:
            actor_two_index = i-1
            break

    return actor_one_index,actor_two_index

