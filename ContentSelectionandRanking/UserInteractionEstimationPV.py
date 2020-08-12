import networkx as nx
import xlrd


# User Interaction class contains all functions used to calculate user interaction of each cluster


class UserInteraction:

    # Default constructor to initialize required data
    def __init__(self):

        # list to store unique users related to each topic cluster
        self.users_related_topic_clusters = list()

        # list to store each social graph for each topic cluster
        self.social_graph_of_topic_clusters = list()

        # list to store reciprocity of each topic cluster
        self.reciprocity_of_graph_clusters = list()

        # list to store user interaction of each topic cluster
        self.user_interaction_topic_clusters = list()

        # dict to store each user with list of all followers
        self.users_with_followers = {}

    # get_users_with_followers(): is function used to get each user and their followers
    def get_users_with_followers(self):

        # open excel file
        wb = xlrd.open_workbook(
            r'C:\Users\Ahmed AbdElhamed\Desktop\IdentifyingandRankingNewsUsingSocial Media\Tweets\users_followers.xlsx')

        # get first sheet
        sheet = wb.sheet_by_index(0)

        # loop to get each row in excel sheet
        for i in range(sheet.nrows):

            # if user in dict then add follower in list of their followers
            # otherwise add new item in dict with new user
            if sheet.cell_value(i, 0) in self.users_with_followers:
                self.users_with_followers[sheet.cell_value(i, 0)].append(sheet.cell_value(i, 1))
            else:
                self.users_with_followers[sheet.cell_value(i, 0)] = [sheet.cell_value(i, 1)]

    # get_users_related_topic_clusters(): get users related to each topic cluster
    def get_users_related_topic_clusters(self, users_with_thier_tweetss, topic_clusterss):

        # users_with_thier_tweets: dict contains users and list of tweets
        users_with_thier_tweets = users_with_thier_tweetss

        # topic_clusters: contains list of nodes of each cluster
        topic_clusters = topic_clusterss

        # loop to get each topic cluster
        for topic_cluster in topic_clusters:

            # to store users related to topic cluster
            users_related_topic_cluster = set()

            # cast set to list
            tc = list(topic_cluster)

            # loop to get each node (keyword) in cluster
            for keyword in tc:

                # get users related to topic cluster
                for user, tweet_keywords in users_with_thier_tweets.items():
                    if list(tweet_keywords).__contains__(keyword):
                        # add user in set
                        users_related_topic_cluster.add(user)

            # add users related to cluster in list
            self.users_related_topic_clusters.append(list(users_related_topic_cluster))

    # generate_social_graph_topic_clusters_with_improvement(): used to generate social graph for each cluster
    def generate_social_graph_topic_clusters_with_improvement(self):

        # generate dict of users and their followers
        self.get_users_with_followers()

        # loop to get each cluster users
        for topic_cluster_users in self.users_related_topic_clusters:

            # graph to add users and their followers of topic cluster
            social_graph = nx.Graph()

            # loop to get each user in cluster users
            for user in topic_cluster_users:

                # if user has followers then add user and list followers
                # otherwise add user as node
                if user in self.users_with_followers:

                    # loop to get each follower in follower list of current user
                    for follower in self.users_with_followers[user]:
                        # add user and follower in graph (u,v)
                        social_graph.add_edge(user, follower)

                else:
                    # add user as node in graph
                    social_graph.add_node(user)

            # add social graph in list
            self.social_graph_of_topic_clusters.append(social_graph)

    # calculate_reciprocity_topic_clusters(): used to calculate reciprocity of social graph of topic cluster
    def calculate_reciprocity_topic_clusters(self):

        # loop to get each social graph
        for social_graph_of_cluster in self.social_graph_of_topic_clusters:
            # calculate reciprocity of social graph
            reciprocity = (2 * nx.Graph(social_graph_of_cluster).number_of_edges()) / (
                    nx.Graph(social_graph_of_cluster).number_of_nodes() - 1)

            # add reciprocity of social graph in list
            self.reciprocity_of_graph_clusters.append(reciprocity)

    # get_user_interaction_topic_cluster(): used to calculate user interaction of each topic
    def get_user_interaction_topic_cluster(self):

        # loop to get reciprocity of each social graph
        for reciprocity in self.reciprocity_of_graph_clusters:
            # calculate user interaction of topic cluster and add in list
            if sum(self.reciprocity_of_graph_clusters) == 0:
                self.user_interaction_topic_clusters.append(0)
            else:
                self.user_interaction_topic_clusters.append(reciprocity / sum(self.reciprocity_of_graph_clusters))

        # retrieve user interaction list
        return self.user_interaction_topic_clusters
