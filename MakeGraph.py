import networkx as nx
import matplotlib.pyplot as plt
import random
def make_graph(save_graph_image_bool,Number_of_Actors,Actor_List,Opinion_List,Show_Relation_Above,iteration_number,Influencer_List,folder_name):
    #This is the function which will produce a visual graph of the system and does not need to be changed with runs
    graph = nx.Graph()
    node_colour_list = []
    edge_colour_list = []
    node_border_list = []
    node_size_list = []
    
    #adds nodes to graph and colour list for nodes
    for i in range(Number_of_Actors):
        graph.add_node(i)
        node_border_list.append('black')
        node_size_list.append(50)
        if Actor_List[i].BeliefAxis < 0:
            node_colour_list.append((1 - abs(Actor_List[i].BeliefAxis), 1 - abs(Actor_List[i].BeliefAxis), 1))
        else:
            node_colour_list.append((1, 1 - abs(Actor_List[i].BeliefAxis), 1 - abs(Actor_List[i].BeliefAxis)))
    
    #adds edges to graph
    for i in range(Number_of_Actors):
        for j in range(i, Number_of_Actors):
            if Opinion_List[i][j] >= Show_Relation_Above:

                graph.add_edge(i, j, weight=Opinion_List[i][j] + 1)

                if Opinion_List[i][j] < 0:
                    pass
                    edge_colour_list.append((1, 0,0, 1))
                else:
                    edge_colour_list.append((0, 1, 0,1))

    #adds influencers as larger nodes to the list
    for i in range(len(Influencer_List)):
        graph.add_node(i+Number_of_Actors)
        node_border_list.append('purple')
        node_size_list.append(250)
        if Influencer_List[i].BeliefAxis < 0:
            node_colour_list.append((1 - abs(Influencer_List[i].BeliefAxis), 1 - abs(Influencer_List[i].BeliefAxis), 1))
        else:
            node_colour_list.append((1, 1 - abs(Influencer_List[i].BeliefAxis), 1 - abs(Influencer_List[i].BeliefAxis)))

    plt.close('all')
    #draw graph in the spring form
    nx.draw_spring(graph, node_color=node_colour_list, node_size=node_size_list, edge_color=edge_colour_list, edgecolors=node_border_list,width=1)
    if save_graph_image_bool:
        plt.savefig(folder_name +'/'+str(iteration_number) + "spring.png", format="png", bbox_inches='tight',dpi = 200)
    plt.close('all')

    return graph
