import networkx as nx
import matplotlib.pyplot as plt
import statistics

#function to calculate statisitcs about the current state of the network which are stored in the data_dict
def Calculate_Statistics(Actor_List,graph,data_dict):
    data_dict['AverageDegree'].append(len(graph.edges()) / len(graph.nodes()))
    data_dict['GraphDensity'].append(len(graph.edges()) / int(len(Actor_List) * (len(Actor_List)-1) /2 ))

    for i in range(len(Actor_List)):
        data_dict['Belief'][i].append(Actor_List[i].BeliefAxis)

    BeliefValueList = []
    for actor in Actor_List:
        BeliefValueList.append(actor.BeliefAxis)
    data_dict['AverageBelief'].append(sum(BeliefValueList)/len(Actor_List))
    data_dict['StandardDeviationBelief'].append(statistics.stdev(BeliefValueList))

    data_dict['FriendBBLink'].append(0)
    data_dict['FriendBWLink'].append(0)
    data_dict['FriendWWLink'].append(0)
    data_dict['FriendRWLink'].append(0)
    data_dict['FriendRRLink'].append(0)
    data_dict['FriendBRLink'].append(0)

    for edge in graph.edges():
        if Actor_List[edge[0]].BeliefAxis < -.333:
            if Actor_List[edge[1]].BeliefAxis < -.333:
                data_dict['FriendBBLink'][-1] += 1  # b-b
            elif Actor_List[edge[1]].BeliefAxis > .333:
                data_dict['FriendBRLink'][-1] += 1  # b-r
            else:
                data_dict['FriendBWLink'][-1] += 1  # b-w
        elif Actor_List[edge[0]].BeliefAxis > .333:
            if Actor_List[edge[1]].BeliefAxis < -.333:
                data_dict['FriendBRLink'][-1] += 1  # r-b
            elif Actor_List[edge[1]].BeliefAxis > .333:
                data_dict['FriendRRLink'][-1] += 1  # r-r
            else:
                data_dict['FriendRWLink'][-1] += 1  # r-w
        else:
            if Actor_List[edge[1]].BeliefAxis < -.333:
                data_dict['FriendBWLink'][-1] += 1  # w-b
            elif Actor_List[edge[1]].BeliefAxis > .333:
                data_dict['FriendRWLink'][-1] += 1  # w-r
            else:
                data_dict['FriendWWLink'][-1] += 1  # w-w


    data_dict['ClusteringCoefficient'].append(nx.algorithms.cluster.average_clustering(graph))
    components = list(graph.subgraph(c) for c in nx.algorithms.connected_components(graph))
    data_dict['NumberOfComponents'].append(len(components))
    largest_component = max(components, key=len)
    data_dict['SizeOfLargestComponent'].append(len(largest_component.nodes()))
    data_dict['DiameterGraph'].append(nx.algorithms.distance_measures.diameter(largest_component))
    data_dict['NumberOfEdgesNew'].append(len(graph.edges() - data_dict['PreviousGraph'].edges()))
    data_dict['NumberOfEdgesGone'].append(len(data_dict['PreviousGraph'].edges() - graph.edges()))
    data_dict['PreviousGraph'] = graph

#function to turn the data_dict into a varity of charts
def Make_Charts(data_dict,NumberOfDays,NumberOfDaysBetweenImage,folder_name):
    plt.close('all')
    #function to graph a simple xy line graph with one or more lines
    def GraphFactory(list_of_things_to_plot, labels_of_things_to_plot, chart_title, xlabel, ylabel, figfilename,
                     Number_of_Days, Number_of_Days_Between_Image):
        fig, ax = plt.subplots(1)
        x = range(0, Number_of_Days, Number_of_Days_Between_Image)
        for i in range(len(list_of_things_to_plot)):
            plt.plot(x, list_of_things_to_plot[i], label=labels_of_things_to_plot[i])
        plt.legend()
        plt.title(chart_title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(folder_name + '/Output_Graph/' + figfilename + '.png', format='PNG')
        plt.close(fig)

    # applying the graph factory function over a variety of different data_dict
    GraphFactory(list_of_things_to_plot = [data_dict['AverageDegree']],
                 labels_of_things_to_plot = ['Average Degree'],
                 chart_title = 'Average Degree of a Node (Number of Friends An Actor Has)',
                 xlabel = 'Day', ylabel = 'Average Degree',
                 figfilename = 'averageDegree',
                 Number_of_Days = NumberOfDays,Number_of_Days_Between_Image = NumberOfDaysBetweenImage)

    GraphFactory(list_of_things_to_plot=[data_dict['AverageBelief']],
                 labels_of_things_to_plot=['Average Belief'],
                 chart_title='Average Belief of Actors',
                 xlabel='Day', ylabel='Average Belief of Actors',
                 figfilename='averageBelief',
                 Number_of_Days=NumberOfDays, Number_of_Days_Between_Image=NumberOfDaysBetweenImage)

    GraphFactory(list_of_things_to_plot=[data_dict['StandardDeviationBelief']],
                 labels_of_things_to_plot=['Standard Deviation of Belief'],
                 chart_title='Standard Deviation of an Personal Belief',
                 xlabel='Day', ylabel='Standard Deviation',
                 figfilename='sdBelief',
                 Number_of_Days=NumberOfDays, Number_of_Days_Between_Image=NumberOfDaysBetweenImage)

    GraphFactory(list_of_things_to_plot=[data_dict['GraphDensity']],
                 labels_of_things_to_plot=['Density'],
                 chart_title='Density of Graph',
                 xlabel='Day', ylabel='Density',
                 figfilename='Density',
                 Number_of_Days=NumberOfDays, Number_of_Days_Between_Image=NumberOfDaysBetweenImage)

    GraphFactory(list_of_things_to_plot=[data_dict['FriendBBLink'],data_dict['FriendBWLink'],data_dict['FriendWWLink'],data_dict['FriendRWLink'],data_dict['FriendRRLink'],data_dict['FriendBRLink']],
                 labels_of_things_to_plot=['Blue-Blue','Blue-White','White-White','Red-White','Red-Red','Blue-Red'],
                 chart_title='Friendship Types',
                 xlabel='Day', ylabel='Amount of Type of Connection',
                 figfilename='FriendType',
                 Number_of_Days=NumberOfDays, Number_of_Days_Between_Image=NumberOfDaysBetweenImage)

    GraphFactory(list_of_things_to_plot=[data_dict['ClusteringCoefficient']],
                 labels_of_things_to_plot=['Average Clustering Coefficient'],
                 chart_title='Average Clustering Coefficient',
                 xlabel='Day', ylabel='Average Clustering Coefficient',
                 figfilename='ClusteringCoefficient',
                 Number_of_Days=NumberOfDays, Number_of_Days_Between_Image=NumberOfDaysBetweenImage)

    GraphFactory(list_of_things_to_plot = [data_dict['NumberOfComponents']],
                 labels_of_things_to_plot = ['Number Of Components'],
                 chart_title = 'Number Of Components',
                 xlabel = 'Day', ylabel = 'Amount',
                 figfilename = 'numberComponents',
                 Number_of_Days = NumberOfDays,Number_of_Days_Between_Image = NumberOfDaysBetweenImage)

    GraphFactory(list_of_things_to_plot = [data_dict['SizeOfLargestComponent']],
                 labels_of_things_to_plot = ['Size Of Largest Components'],
                 chart_title = 'Size Of Largest Components',
                 xlabel = 'Day', ylabel = 'Amount of Nodes',
                 figfilename = 'sizeLargestComponents',
                 Number_of_Days = NumberOfDays,Number_of_Days_Between_Image = NumberOfDaysBetweenImage)

    GraphFactory(list_of_things_to_plot = [data_dict['DiameterGraph']],
                 labels_of_things_to_plot = ['Diameter Of Graph'],
                 chart_title = 'Diameter of the Graphs largest connected component',
                 xlabel = 'Day', ylabel = 'Diameter',
                 figfilename = 'diameter',
                 Number_of_Days = NumberOfDays,Number_of_Days_Between_Image = NumberOfDaysBetweenImage)

    GraphFactory(list_of_things_to_plot = [data_dict['NumberOfEdgesNew'],data_dict['NumberOfEdgesGone']],
                 labels_of_things_to_plot = ['Number of New Edges','Number of Lost Edges'],
                 chart_title = 'Difference In Amounts Of Edges Since The Previous Graph State',
                 xlabel = 'Day', ylabel = 'Amount',
                 figfilename = 'newOldEdges',
                 Number_of_Days = NumberOfDays,Number_of_Days_Between_Image = NumberOfDaysBetweenImage)

    #Creating chart to display the belief of each actor over time
    fig = plt.figure()
    ax = plt.axes()
    x = range(0,NumberOfDays,NumberOfDaysBetweenImage)
    for i in range(len(data_dict['Belief'])):
        plt.plot(x,data_dict['Belief'][i])

    plt.title('Belief of Actors over time')
    plt.xlabel('Day')
    plt.ylabel('Belief')
    plt.savefig(folder_name + '/' + 'belief'+'.png',format = 'PNG', dpi = 200)
    plt.close('all')



