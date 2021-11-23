def decay(Time_Since_Last_Interaction,Opinion_List,random,chance,amount):
    #applies on each relationship, a "chance" percent of the time move the relationship closer to 0 by "amount"
    for i in range(len(Opinion_List)):
        for j in range(i + 1, len(Opinion_List[0])):
            if random.next() <= chance and abs(Opinion_List[i][j]) >= amount:
                if Opinion_List[i][j] > 0:
                    Opinion_List[i][j] -= amount
                elif Opinion_List[i][j] < 0:
                    Opinion_List[i][j] += amount

