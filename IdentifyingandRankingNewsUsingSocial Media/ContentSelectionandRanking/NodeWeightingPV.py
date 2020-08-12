import networkx as nx
import math

"""
Node weighting is important task to determine the importance of each term in each topic cluster.

Node weighting equation is
foreach node in each cluster
    part1 = ((Number of edges connected to node)/(Number of edges in cluster))^0.5
    part2 = ((Summation of edges weight connected to node )/(Summation of edges weight in cluster))^0.5
    Node weight of node = part1 * part2

"""


class NodeWeighting:

    # Default constructor to get the graph before clustering and graph after clustering
    def __init__(self, total_graph, clusters_nodes):

        # total_graph: to store total graph before clustering
        self.total_graph = nx.Graph(total_graph)

        # clusters_nodes: to store each nodes list only for each cluster
        self.clusters_nodes = clusters_nodes

        # clusters: to store each cluster with each nodes and edges
        self.clusters = list()

        # nodes_weights: to store dict contains each node and its weight for each cluster
        self.nodes_weights = list()

    # get_each_cluster_from_total_graph: is function to get each cluster with its nodes and edges
    def get_each_cluster_from_total_graph(self):

        # loop to get each cluster nodes
        for cluster_nodes in self.clusters_nodes:
            # add each cluster with its nodes and edges by using subgraph()fn
            # subgraph()fn: input => cluster nodes list output => cluster with its nodes and edges
            self.clusters.append(self.total_graph.subgraph(cluster_nodes))

    # get_total_edges_weight_connected_to_node: is function to get the summation of edges weight connected to node
    def get_total_edges_weight_connected_to_node(self, node, topic_cluster):

        # get edges connected by node in specific topic cluster
        edges = topic_cluster.edges(node)

        # s: used to add add edge weight.
        s = 0

        # loop to get each edge connected to node
        for e in edges:
            # get edge weight by first and second nodes in edge in topic cluster
            s += topic_cluster[e[0]][e[1]]['weight']

        # return total edges weight connected to node
        return s

    # get_total_edges_weight_in_topic_cluster: is function to get Summation of edges weight in cluster
    def get_total_edges_weight_in_topic_cluster(self, topic_cluster):

        # s: used to add add edge weight.
        s = 0

        # loop to get each edge weight
        for (u, v, wt) in topic_cluster.edges.data('weight'):
            # add edge weight
            s += wt

        # return Summation of edges weight in cluster
        return s

    # calculate_nodes_weight: is function to calculate each node weight in each topic cluster
    def calculate_nodes_weight(self):

        # to get each cluster with its nodes and edges
        self.get_each_cluster_from_total_graph()

        # cluster_count: used to determine each topic cluster
        cluster_count = 0

        # loop to get nodes list for each cluster
        for cluster_nodes in self.clusters_nodes:

            # nodes_weights_dict: to store each node and its weight of specific cluster
            nodes_weights_dict = dict()

            # get first cluster that contains nodes and edges
            cluster = nx.Graph(self.clusters[cluster_count])

            # increase count by 1 to get next cluster for next iteration
            cluster_count += 1

            # total_edges_weight_in_cluster: get total edges weight in specific cluster
            total_edges_weight_in_cluster = self.get_total_edges_weight_in_topic_cluster(cluster)

            if total_edges_weight_in_cluster == 0:
                total_edges_weight_in_cluster = 1

            # loop to get each node in cluster nodes to calculate node weight
            for node in cluster_nodes:
                cluster_edges = cluster.number_of_edges()
                if cluster_edges == 0:
                    cluster_edges = 1
                # calculate ((Number of edges connected to node)/(Number of edges in cluster))^0.5
                part1 = math.pow(len(cluster.edges(node)) / cluster_edges, 0.5)

                # get total edges weight_connected to node
                total_edges_weight_connected_to_node = self.get_total_edges_weight_connected_to_node(node, cluster)

                # calculate ((Summation of edges weight connected to node )/(Summation of edges weight in cluster))^0.5
                part2 = math.pow((total_edges_weight_connected_to_node / total_edges_weight_in_cluster), 0.5)

                # calculate node weight
                node_weight = part1 * part2

                # add node and its weight in dict
                nodes_weights_dict[node] = node_weight

            # after finished all nodes in cluster add dict in nodes_weights
            self.nodes_weights.append(nodes_weights_dict)

        # return list that contains dicts of each node and its weight in topic clusters
        return self.nodes_weights
