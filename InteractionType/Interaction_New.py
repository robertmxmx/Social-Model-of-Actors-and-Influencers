import Helper

def Interaction(actor_one,actor_two,actor_list,opinion_list,Time_Since_Last_Interaction,Number_Of_Previous_Interaction,diameter,effect_opinion,effect_belief):

    #extract belief from actors
    ActorOneBelief = actor_list[actor_one].BeliefAxis
    ActorTwoBelief = actor_list[actor_two].BeliefAxis

    belief,opinion = 0,0

    if abs(ActorOneBelief - ActorTwoBelief) <= diameter: #if difference in belief is less than diameter
        opinion += effect_opinion
        if opinion_list[actor_one][actor_two] >= 0.20: #if there is a positive bond between 2 actors
            belief += (effect_belief * (1+opinion_list[actor_one][actor_two]))*2

    else: #if difference in belief is greater than diameter
        opinion -= effect_opinion
        if opinion_list[actor_one][actor_two] <= -0.20: #if there is a negative bond (disagreement) between 2 actors
            belief -= effect_belief

    #move actor's relationship "opinion" percent together/apart
    opinion_list[actor_one][actor_two] += (1-abs(opinion_list[actor_one][actor_two])) * opinion

    #move actor's belief "belief" percent together/apart
    if ActorOneBelief > ActorTwoBelief:
        actor_list[actor_one].BeliefAxis -= belief * abs(ActorOneBelief - ActorTwoBelief)
        actor_list[actor_two].BeliefAxis += belief * abs(ActorOneBelief - ActorTwoBelief)
    else:
        actor_list[actor_one].BeliefAxis += belief * abs(ActorOneBelief - ActorTwoBelief)
        actor_list[actor_two].BeliefAxis -= belief * abs(ActorOneBelief - ActorTwoBelief)

    #run the helper function to push the result back to -1 or 1 if it went outside those bounds
    actor_list[actor_one].BeliefAxis = Helper.Between01(actor_list[actor_one].BeliefAxis)
    actor_list[actor_two].BeliefAxis = Helper.Between01(actor_list[actor_two].BeliefAxis)
