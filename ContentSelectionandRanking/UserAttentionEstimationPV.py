# User Attention class contains all functions used to calculate user attention of each cluster


class USerAttention:
    # constructor to initialize required data
    def __init__(self, list_of_each_tweet_keywords, list_of_tweet_user, nodes_weight):
        # list contains each tweet keywords
        self.list_of_each_tweet_keywords = list_of_each_tweet_keywords
        # list contains all users made tweets
        self.list_of_tweet_user = list_of_tweet_user
        # list contains nodes weight of each cluster
        self.nodes_weight = nodes_weight
        # list to store tweets related to each cluster
        self.tweets_related_to_each_cluster = list()
        # list to store unique users related to each cluster
        self.unique_users_related_to_each_cluster = list()
        # list to store user attention for each cluster
        self.user_attention_in_each_cluster = list()

    # function used to calculate threshold used to filter nodes
    def get_threshold(self):
        pass

    # get_tweets_related_to_each_topic is function used to get tweets related to each cluster
    def get_tweets_related_to_each_topic(self):

        # loop to get each cluster nodes weight
        for node_weight_dict in self.nodes_weight:

            # to store the ids of tweets related to nodes
            tweets_related_to_topic_cluster = set()

            # loop to get each node and its weight
            for key in node_weight_dict:

                # get nodes with high weight.
                # must be greater than threshold
                if node_weight_dict[key] > 0.001:

                    # loop to get each tweet keywords to check is node in this tweet or not
                    for i in range(len(self.list_of_each_tweet_keywords)):

                        # check node in this tweet
                        if list(self.list_of_each_tweet_keywords[i]).__contains__(key):
                            tweets_related_to_topic_cluster.add(i)

            # add tweets related to topic cluster in tweets_related_to_each_cluster
            self.tweets_related_to_each_cluster.append(tweets_related_to_topic_cluster)

    # get_unique_users_related_to_tweets: is function to get all unique users related to each topic cluster
    def get_unique_users_related_to_tweets(self):

        # loop to get each tweets related to topic cluster
        for tweets_related_to_cluster in self.tweets_related_to_each_cluster:

            # to store unique users in topic cluster
            unique_users = set()

            # loop to get each tweet from tweets_related_to_cluster
            for tweet in tweets_related_to_cluster:
                # add user in set
                unique_users.add(self.list_of_tweet_user[tweet])

            # add unique users of topic cluster
            self.unique_users_related_to_each_cluster.append(unique_users)

    # get_total_unique_users_in_clusters(): is function to get the total unique users in clusters
    def get_total_unique_users_in_clusters(self):
        # to store summation of number of unique users of each topic cluster
        s = 0

        # loop to get each unique users in each cluster
        for unique_users_related_to_cluster in self.unique_users_related_to_each_cluster:
            # add number of unique users
            s += len(unique_users_related_to_cluster)

        # return total unique users in clusters
        return s

    # calculate_user_attention_estimation_for_each_cluster: is function to calculate user attention in each cluster
    def calculate_user_attention_estimation_for_each_cluster(self):

        # get total unique users in clusters
        total_unique_users_in_clusters = self.get_total_unique_users_in_clusters()

        # loop to get each unique users in each cluster
        for unique_users_related_to_cluster in self.unique_users_related_to_each_cluster:
            # calculate user attention and add in user_attention_in_each_cluster
            self.user_attention_in_each_cluster.append(
                len(unique_users_related_to_cluster) / total_unique_users_in_clusters)

        # return user attention for each cluster
        return self.user_attention_in_each_cluster
