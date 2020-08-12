import matplotlib.pyplot as plt
import networkx as nx

# clustering class contains all functions needed to apply graph clustering using newman algorithm with improvement


class clustering:

    # Default constructor used to initialize required data structure used in clustering
    def __init__(self, co_occurrence_list):

        # list to store all topic clusters after clustering
        self.sub_graphs = list()

        # to store graph edges of key term graph in form (u,v,w)
        graph_edges = list()

        # Total Graph to store graph before clustering
        self.graph = nx.Graph()

        # loop to get each term
        for term1 in co_occurrence_list:
            # loop to get related terms of term1
            for term2 in co_occurrence_list[term1]:
                # add new edge in list (term1, term2, weight)
                graph_edges.append((term1, term2, co_occurrence_list[term1][term2]))

        # add graph edges in graph DS
        self.graph.add_weighted_edges_from(graph_edges)

        # save copy of graph before clustering is needed for next steps (in content selection and ranking)
        self.before_clustering = self.graph

    # get_betweenness_of_edges(): used to calculate betweenness of all edges in graph
    def get_betweenness_of_edges(self):

        # to store unique betweenness values of edges
        betweenness_values = set()

        # calculate betweenness of all edges in graph
        dict_with_centrality_values = nx.edge_betweenness_centrality(self.graph)

        # loop to get each edge with its betweenness value
        for edge, betweenness_value in dict_with_centrality_values.items():
            betweenness_values.add(betweenness_value)

        # retrieve betweenness values
        return betweenness_values

    # get_max_betweenness(): used to retrieve the edge with maximum betweeness
    def get_max_betweenness(self):

        # calculate betweenness of all edges in graph
        dict_with_centrality_values = nx.edge_betweenness_centrality(self.graph)

        # cast res as list
        list_of_tuples = list(dict_with_centrality_values.items())

        # sort list of tuples by betweenness in desc order
        list_of_tuples.sort(key=lambda t: t[1], reverse=True)

        # retrieve edge with max betweenness
        return list_of_tuples[0]

    # newman_algorithm_with_improvement(): used to apply newman algorithm with improvement
    def newman_algorithm_with_improvement(self):

        # to check is first iteration or not
        first_time = True

        # to store average betweenness
        average_betweenness = 0.0

        # to get unique betweenness values of edges
        edges_betweenness = list(self.get_betweenness_of_edges())

        # loop to to make clustering in graph
        while True:

            # if first iteration then calculate average betweenness
            if first_time:
                average_betweenness = sum(edges_betweenness) / len(edges_betweenness)
                first_time = False

            # get the edge with max betweenness
            tuple_with_max_betweenness = self.get_max_betweenness()

            # get max betweenness value from the tuple
            max_betweenness = tuple_with_max_betweenness[1]

            # calculate transitivity before removing edge with max betweenness
            previous_transitivity = nx.transitivity(self.graph)

            # remove edge with maximum betweenness from graph
            self.graph.remove_nodes_from(tuple_with_max_betweenness[0])

            # calculate transitivity after removing edge with max betweenness
            posterior_transitivity = nx.transitivity(self.graph)

            # check termination criteria
            if posterior_transitivity < previous_transitivity or max_betweenness < average_betweenness:
                break

        # add edge with maximum betweenness
        self.graph.add_weighted_edges_from(
            [[tuple_with_max_betweenness[0][0], tuple_with_max_betweenness[0][1], max_betweenness]])

    # draw_graph: is function used to draw graph
    def draw_graph(self):

        # set options
        options = {
            'node_color': 'yellow',
            'node_size': 50,
            'width': 1,
            'font_family': 'Monotype Corsiva',
            'edge_color': 'pink',
            'font_size': '12',
        }

        # draw and display graph
        nx.draw(self.graph, with_labels=True, **options)
        plt.draw()
        plt.show()

    # get_sub_graph_count(): is function to return number of sub graphs
    def get_sub_graph_count(self):
        sub_graphs = list(nx.connected_components(self.graph))
        return len(sub_graphs)

    # get_topic_clusters(): is function to set sub_graphs by list of clusters
    def get_topic_clusters(self):
        self.sub_graphs = list(nx.connected_components(self.graph))
