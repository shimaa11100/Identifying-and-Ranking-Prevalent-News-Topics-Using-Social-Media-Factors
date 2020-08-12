# Media Focus class contains all functions used to calculate media focus of each cluster
class MediaFocus:

    # Default constructor used to initialize required data structures
    def __init__(self, list_of_each_news_keywords, nodes_weight):

        # list contains each news article keywords
        self.list_of_each_news_keywords = list_of_each_news_keywords

        # list contains nodes weight of each cluster
        self.nodes_weight = nodes_weight

        # list to store news articles related to each cluster
        self.news_related_to_each_cluster = list()

        # list to store media focus for each cluster
        self.media_focus_in_each_cluster = list()

    # function used to calculate threshold used to filter nodes
    def get_threshold(self):
        pass

    # get_news_related_to_each_topic: is function to get news articles related to each topic cluster
    def get_news_related_to_each_topic(self):

        # loop to get each dict of nodes weight of cluster
        for node_weight_dict in self.nodes_weight:

            # news_related_to_topic_cluster: to add news articles related to topic cluster
            news_related_to_topic_cluster = set()

            # loop to get each node
            for key in node_weight_dict:

                # compare weight with threshold
                if node_weight_dict[key] > 0.001:
                    # get news articles related by topic cluster
                    for i in range(len(self.list_of_each_news_keywords)):
                        if list(self.list_of_each_news_keywords[i]).__contains__(key):
                            news_related_to_topic_cluster.add(i)

            # add news articles set in list.
            self.news_related_to_each_cluster.append(news_related_to_topic_cluster)

    # get_total_news_in_clusters: get total number of news articles related to all topic clusters
    def get_total_news_in_clusters(self):

        # to store summation of number of news articles of each topic cluster
        s = 0

        # loop to get number of news articles in each topic
        for news_related_to_cluster in self.news_related_to_each_cluster:
            # add number of news articles related to topic cluster
            s += len(news_related_to_cluster)

        # retrieve result
        return s

    # calculate_media_focus_estimation_for_each_cluster: to calculate MF for each topic cluster
    def calculate_media_focus_estimation_for_each_cluster(self):

        # get news articles related to each topic cluster
        total_news_in_clusters = self.get_total_news_in_clusters()

        # loop to get news articles related to each cluster
        for news_related_to_cluster in self.news_related_to_each_cluster:
            # calculate MF and add it in list
            self.media_focus_in_each_cluster.append(
                len(news_related_to_cluster) / total_news_in_clusters)

        # retrieve MF of each cluster
        return self.media_focus_in_each_cluster
