import Helper

def Interaction(actor,influencer,diameter,influencer_effect_belief):
    #simulates the influencer interaction with an actor
    belief = 0
    if abs(actor.BeliefAxis - influencer.BeliefAxis) <= diameter: #if difference in belief is less than x
            belief += influencer_effect_belief

    #move belief "influencer_effect_belief" percent together
    if actor.BeliefAxis > influencer.BeliefAxis:
        actor.BeliefAxis -= belief * abs(actor.BeliefAxis - influencer.BeliefAxis)
    else:
        actor.BeliefAxis += belief * abs(actor.BeliefAxis - influencer.BeliefAxis)

    #run the helper function to push the result back to -1 or 1 if it went outside those bounds
    actor.BeliefAxis = Helper.Between01(actor.BeliefAxis)
