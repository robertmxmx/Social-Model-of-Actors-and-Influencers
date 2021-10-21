#import statements are used to make sure of functions in other files, new modular functions need to be imported here
import InfluencerType.Influencer
import InteractionType.Interaction_New
import InteractionPickerType.PickerWeighted
import InteractionPickerType.PickerRandom
import BeliefPickerType.BeliefRandom
import BeliefPickerType.BeliefSame
import ActorType.Actor
import MakeGraph
import matplotlib.pyplot as plt
import statistics
import RandomIterator
import random
import DecayType.DecayUniform
import DecayType.NoDecay
import CalculateStatistics
import networkx as nx
import InteractionType.Influencer_Interaction
from os import makedirs

#Parameters
Number_of_Days_Between_Image = 500
Number_of_Actors = 100
Number_of_Influencers = 1
Average_Daily_Interactions = 12 #https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6113687/
Average_Daily_Influencer_Events = 12
Number_of_Days = 2001 #for best results make sure the number of days to run ends in 1 e.g. 2001 days , 1501 days, 5001 days etc.
effect_opinion = 0.005
effect_belief = 0.005
influencer_effect_belief = 0.005
diameter = 0.5
influencer_diameter = 0.5
decay_chance = 0.01
decay_amount = 0.05

#setting which files logic is used for each of these actions, these are modular and can be replaced with other functions
InfluencerType = InfluencerType.Influencer
ActorType = ActorType.Actor
ActorBeliefPickerType = BeliefPickerType.BeliefRandom
ActorBeliefOverride = 0 #if BeliefPickerType.BeliefSame is used it will make use of the override value
InfluencerBeliefPickerType = BeliefPickerType.BeliefSame
InfluencerBeliefOverride = 0 #if BeliefPickerType.BeliefSame is used it will make use of the override value
ActorPickerType = InteractionPickerType.PickerRandom #another option produced is InteractionPickerType.PickerWeighted
InfluencerInteractionType = InteractionType.Influencer_Interaction
InteractionType = InteractionType.Interaction_New
DecayType = DecayType.DecayUniform #another option produced is OpinionDailyChange.NoDecay which has the same effect as disabling the opinion decay

Make_Graph = True #create the visual graph networks
Make_Charts = False #create the charts for graph and statistics

for k in range(1):  # used to automate tests over a variety of 1 or 2 parameters, how many times to run each parameter set
    diameter = 0
    for i in range(1): #used to automate tests over a variety of 1 or 2 parameters, varying how many times to adjust first parameter
        diameter += 0.5
        influencer_diameter = 0
        for j in range(1): #used to automate tests over a variety of 1 or 2 parameters, varying how many times to adjust second parameter ,
            influencer_diameter += 0.5

            #to use a custom seed, you can uncomment the next two lines and comment out the following 2 lines as they set the seed to be a random number
            #seed = 11
            #Random = RandomIterator.RandomIterator(seed)

            seed = random.randrange(1,1000000000000) #to use a manual seed comment this line and uncomment the previous two lines
            Random = RandomIterator.RandomIterator(seed)

            folder_prefix = "My First Test" # what the output folder of files should be called
            folder_name = folder_prefix + "/ diameter=" + str(round(diameter,5)) + " and influencer_diameter =" + str(round(influencer_diameter,5)) + " and seed =" + str(seed) #can be redone depending on what parameters are being tested

            try: #making folder to put other graph iamges in
                makedirs(folder_name+"\Output_Graph")
            except:
                pass
            #data_dict holds the statistics for the various charts produced
            data_dict = {
                'PreviousGraph': nx.empty_graph(Number_of_Actors),
                'AverageBelief': [],
                'StandardDeviationBelief': [],
                'AverageDegree': [],
                'GraphDensity': [],
                'NumberOfEdgesNew': [],
                'NumberOfEdgesGone': [],
                'FriendBBLink': [],
                'FriendBWLink': [],
                'FriendWWLink': [],
                'FriendRWLink': [],
                'FriendRRLink': [],
                'FriendBRLink': [],
                'DiameterGraph': [],
                'ClusteringCoefficient': [],
                'Centrality': [],
                'NumberOfComponents': [],
                'SizeOfLargestComponent': [],
                'Belief' : []
            }
            for i in range(Number_of_Actors):
                data_dict["Belief"].append([])

            #initialising the lists to hold the state of the world, its actors, and relationship tracking
            Actor_List = [ActorType.Actor(i,ActorBeliefPickerType,Random,ActorBeliefOverride) for i in range(Number_of_Actors)]
            Influencer_List = [InfluencerType.Influencer(i,InfluencerBeliefPickerType,Random,InfluencerBeliefOverride) for i in range(Number_of_Influencers)]
            Opinion_List = [[0 for i in range(Number_of_Actors)] for j in range(Number_of_Actors)]
            Time_Since_Last_Interaction = [[0 for i in range(Number_of_Actors)] for j in range(Number_of_Actors)] #currently unused but is tracked and transmited to functions for potential future use
            Number_Of_Previous_Interaction = [[0 for i in range(Number_of_Actors)] for j in range(Number_of_Actors)] #currently unused but is tracked and transmited to functions for potential future use

            for iteration_number in range(Number_of_Days): #main loop to repeat the days

                if iteration_number % Number_of_Days_Between_Image == 0:  #code to call the function to make network images
                    graph = MakeGraph.make_graph(Make_Graph,Number_of_Actors,Actor_List,Opinion_List,0.2,iteration_number,Influencer_List,folder_name)
                    if Make_Charts:
                        CalculateStatistics.Calculate_Statistics(Actor_List,graph,data_dict)

                for interaction_number in range(int(Number_of_Actors*Average_Daily_Interactions/2)): # actor-actor iteration loop

                    actor_one,actor_two = ActorPickerType.Picker(Actor_List,Opinion_List,Time_Since_Last_Interaction,Number_Of_Previous_Interaction,Random) #Use ActorPickerType to choose 2 actors
                    if actor_one > actor_two:
                        actor_one,actor_two = actor_two,actor_one
                    InteractionType.Interaction(actor_one,actor_two,Actor_List,Opinion_List,Time_Since_Last_Interaction,Number_Of_Previous_Interaction,diameter,effect_opinion,effect_belief) #Use InteractionType to simulate an interaction between the 2 actors
                    Time_Since_Last_Interaction[actor_one][actor_two] = 0 #currently unused but is tracked and transmited to functions for potential future use
                    Number_Of_Previous_Interaction[actor_one][actor_two] += 1 #currently unused but is tracked and transmited to functions for potential future use

                for interaction_number in range(int(Number_of_Actors*Average_Daily_Influencer_Events/2)): # actor-influencer iteration loop
                    if Number_of_Influencers >= 1:
                        actor = Actor_List[int(Random.next()*len(Actor_List))]
                        influencer = Influencer_List[int(Random.next()*len(Influencer_List))]
                        InfluencerInteractionType.Interaction(actor,influencer,influencer_diameter, influencer_effect_belief) #Use InteractionType to simulate an interaction between a randomly selected actor and influencer

                DecayType.decay(Time_Since_Last_Interaction, Opinion_List, Random, decay_chance, decay_amount) #actor-relationship decay

            if Make_Charts:
                CalculateStatistics.Make_Charts(data_dict,Number_of_Days,Number_of_Days_Between_Image,folder_name)
