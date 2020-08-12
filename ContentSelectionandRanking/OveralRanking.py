import math

# OverallRanking class contains all functions used to calculate overall ranking using MF, UA and UI


class OverallRanking:

    # Default constructor used to initialize required data structures to calculate overall ranking of each topic
    def __init__(self, user_attention_in_each_cluster, media_focus_in_each_cluster, user_interaction_in_each_cluster):

        # list contains user attention of each topic cluster
        self.user_attention_in_each_cluster = user_attention_in_each_cluster

        # list contains media focus of each topic cluster
        self.media_focus_in_each_cluster = media_focus_in_each_cluster

        # list contains user interaction of each topic cluster
        self.user_interaction_in_each_cluster = user_interaction_in_each_cluster

        # list to store overall ranking of each cluster
        self.overall_ranking_in_each_cluster = {}

    # calculate_overall_ranking_for_each_cluster: used to calculate overall ranking using MF, UA and UI
    # Note: Overall ranking of TC: r(TC) = (MF(TC))^α x (UA(TC))^β x (UI(TC))^γ
    # Note: α = β = γ = 1/3
    def calculate_overall_ranking_for_each_cluster(self):
        for i in range(len(self.user_attention_in_each_cluster)):
            modified_user_attention = math.pow(self.user_attention_in_each_cluster[i], 1 / 3)
            modified_media_focus = math.pow(self.media_focus_in_each_cluster[i], 1 / 3)
            modified_user_interaction = math.pow(self.user_interaction_in_each_cluster[i], 1 / 3)
            self.overall_ranking_in_each_cluster[
                i] = modified_user_attention * modified_media_focus * modified_user_interaction
        return self.overall_ranking_in_each_cluster
