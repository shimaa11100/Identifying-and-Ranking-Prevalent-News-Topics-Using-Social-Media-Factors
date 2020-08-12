from collections import defaultdict
from itertools import product
from enum import Enum
import math

"""
B-Key Term Graph Construction
-->a graph G is constructed, whose nodes represent the most prevalent news topics
in both news and social media.
The vertices of the graph are key terms that belong to set Itop and
the edges that connect them are defined as the co-occurrence of the terms in the tweet dataset.

-->The vertices in G are unique terms selected from N and T, and
the edges are represented by a relationship between these terms

Note: N is set of all keywords extracted from news
      T is set of all keywords extracted from Tweets
     |T| is total number of tweets
     |N| is total number of news
............................................................................
............................................................................

Key Term Graph Construction Processes
1.Term Document Frequency
2.Relevant Key Term Identification
3.Key Term Similarity Estimation
4.Outlier Detection

"""


class Similarity(Enum):
    """Different similarity that can be used ."""

    """
    -->Note:
      DICE_QS=0  or  jACC_QS=0 or COSINE_QS=0
    -->if co(i, j) ≤ ϑ where ϑ = 3 this value in a paper
    else
    DICE_QS = 2 * co(i,j) / df(top)[i] + df(top)[j]
    jACC_QS = co(i,j) / df(top)[i] + df(top)[j] - co(i,j)
    COSINE_QS = co(i,j) / sqrt (df(top)[i] * df(top)[j])
    """
    DICE_QS = 0
    JACC_QS = 1
    COSINE_QS = 2


class KeyTermGraphConstruction:

    # Default Constructor to initialize required data structure for Key term graph construction
    def __init__(self, tweets_keywords, news_keywords, tweets_terms_frequency, news_terms_frequency, total_tweets,
                 total_news, list_of_each_tweet_keywords):
        # (T)
        self.tweets_keywords = tweets_keywords
        # (N)
        self.news_keywords = news_keywords
        # df(t)
        self.tweets_terms_frequency = tweets_terms_frequency
        # df(n)
        self.news_terms_frequency = news_terms_frequency
        # |T|
        self.totaltweets = total_tweets
        # |N|
        self.totalnews = total_news
        # list of each tweet keywords
        self.list_of_each_tweet_keywords = list_of_each_tweet_keywords
        # similarity matrix  DICE_QS or jACC_QS or COSINE_QS
        self.Similarity_dict = defaultdict(lambda: defaultdict(lambda: 0.0))
        # co(i,j)
        self.co_occurrence_dict = defaultdict(lambda: defaultdict(lambda: 0))
        # I(top)
        self.Ranked_Prevalence_Terms = set()

        self.Not_Outliers_dict = defaultdict(lambda: defaultdict(lambda: 0.0))

    """
    1.Term Document Frequency
        -->First, the document frequency of each term in N and T is calculated accordingly.
        
        -->In the case of term set N: 
        The document frequency of each term n is equal to the number of news articles
        in which n has been selected as a keyword;it is represented as df(n).
        
        Note:
           The document frequency of each term t in set T is calculated in a similar fashion.
             
        -->In the case of term set T:     
        The document frequency of each term t is equal to the number of tweets 
        in which t appears it is represented as df(t).     
    """

    def get_term_document_frequency(self):
        return self.news_terms_frequency, self.tweets_terms_frequency

    """
    2.Relevant Key Term Identification (Vertices)
    -->We are primarily interested in the important news-related terms
       As these signal the presence of a news related topic.
       Additionally, part of our objective is to extract the topics that are prevalent
       in both news and social media.
       To achieve this, a new set I is formed I = N intersect T     Step(1)
    
    Note:This intersection of N and T eliminates terms from T 
         that are not relevant to the news and terms from N 
         that are not mentioned in the social media.
    
    -->Set I, however, still contains many potentially unimportant terms.
       So To solve this problem, terms in I are ranked based on
       their prevalence in both sources.                            Step (2)
    
    Notes:
    -prevalence is interpreted as the occurrence of a term, which in turn is 
     the term’s document frequency.
    
    -The prevalence of a term is thus a combination of its occurrence in both N and T.
    
    -Prevalence p of each term i in I is calculated such that half of its weight
     is based on the occurrence of the term in the news media, and
     the other half is based on its occurrence in social media
     
     So Prevalence Equation is 
     
     for each item in set I --> P(i) = ( df(n) * (|T|/|N| ) + df(t)) / 2*|T|
     
     -->The terms in set I are then ranked by their prevalence value,
     and only those in the top π th percentile are selected.
      Using a π value of 75 presented the best results in our experiments.
      We define the newly filtered set Itop using set-builder notation
      
      I(top)--> for each i in (I) if (Pi)/|T|

    """

    def relevant_key_term_identification(self):

        # Step(1)
        term_identification = self.news_keywords & self.tweets_keywords
        term_identification_count = len(term_identification)
        # total is variable = (|T|/|N|)
        total = self.totaltweets / self.totalnews

        prevalence_of_term = {}

        # Step(2)
        for term in term_identification:
            prevalence_of_term[term] = (self.news_terms_frequency[term] * total + self.tweets_terms_frequency[term]) / (
                    2 * self.totaltweets)

        # Step(3)
        for prevalent_term in prevalence_of_term:
            counter = 0
            for element in prevalence_of_term:
                if prevalent_term != element:
                    if prevalence_of_term[prevalent_term] > prevalence_of_term[element]:
                        counter += 1
            if (counter / term_identification_count) * 100 > 80:
                self.Ranked_Prevalence_Terms.add(prevalent_term)

    def key_term_similarity_estimation(self, similarity_metric=None, threshold=None):

        # Step(1)

        itop = list(self.Ranked_Prevalence_Terms)

        for prevalence_term1, prevalence_term2 in product(itop, itop):
            if prevalence_term1 != prevalence_term2:

                if not self.co_occurrence_dict.__contains__(
                        prevalence_term1) and not self.co_occurrence_dict.__contains__(prevalence_term2):
                    self.co_occurrence_dict[prevalence_term1][prevalence_term2] = 0

                for tweet_keywords in self.list_of_each_tweet_keywords:
                    keywords = list(tweet_keywords)

                    if keywords.__contains__(prevalence_term1) and keywords.__contains__(
                            prevalence_term2):

                        if self.co_occurrence_dict.__contains__(prevalence_term1):
                            self.co_occurrence_dict[prevalence_term1][prevalence_term2] += 1
                        elif self.co_occurrence_dict.__contains__(prevalence_term2):
                            self.co_occurrence_dict[prevalence_term2][prevalence_term1] += 1

        # Step (2)
        for key1 in self.co_occurrence_dict:
            for key2 in self.co_occurrence_dict[key1]:
                qs_value = self.calculate_similarity(key1, key2, similarity_metric, threshold)
                if qs_value > 0.03:
                    self.Similarity_dict[key1][key2] = qs_value

    def calculate_similarity(self, key1, key2, similarity_metric, threshold):
        if isinstance(similarity_metric, Similarity):
            metric = similarity_metric
        else:
            metric = Similarity.DICE_QS

        if threshold is None:
            self.threshold = 3
        else:
            self.threshold = threshold

        if self.co_occurrence_dict[key1][key2] <= self.threshold:
            return 0.0

        if metric == Similarity.DICE_QS:
            return 2 * self.co_occurrence_dict[key1][key2] / (
                    self.tweets_terms_frequency[key1] + self.tweets_terms_frequency[key2])

        elif metric == Similarity.COSINE_QS:
            return self.co_occurrence_dict[key1][key2] / math.sqrt(
                self.tweets_terms_frequency[key1] * self.tweets_terms_frequency[key2])

        elif metric == Similarity.JACC_QS:
            return self.co_occurrence_dict[key1][key2] / (
                    self.tweets_terms_frequency[key1] + self.tweets_terms_frequency[key2] -
                    self.co_occurrence_dict[key1][key2])

    # Need comments from Essra and Shaimaa
    def cal(self, listt):
        q1 = []
        q3 = []
        lenn = (len(listt) - 1)
        if (len(listt) % 2 != 0):
            middle = listt[(int)(lenn / 2)]

            for i in listt:
                if (i < middle):
                    q1.append((i))
                elif (i == middle):
                    continue;
                else:
                    q3.append(i)

        if (len(listt) % 2 == 0):
            middle1 = listt[(int)(len(listt) / 2)]
            middle2 = listt[(int)(len(listt) / 2) - 1]

            m = (middle2 + middle1) / 2
            for i in listt:
                if (i < middle1 and i < middle2):
                    q1.append((i))
                elif (i == middle1 or i == middle2):
                    continue
                else:
                    q3.append(i)

        return q1, q3

    def calc_Q(self, q1, q2):
        middle = m = 0
        len_q1 = (len(q1) - 1)
        len_q2 = (len(q2) - 1)
        if (len(q1) % 2 != 0):
            middle = q1[(int)(len_q1 / 2)]
        elif (len(q1) % 2 == 0):
            middle1 = q1[(int)(len(q1) / 2)]
            middle2 = q1[(int)(len(q1) / 2) - 1]
            middle = (middle2 + middle1) / 2

        if (len(q2) % 2 != 0):
            m = q2[(int)(len_q2 / 2)]
        elif (len(q2) % 2 == 0):
            middle1 = q2[(int)(len(q2) / 2)]
            middle2 = q2[(int)(len(q2) / 2) - 1]
            m = (middle2 + middle1) / 2

        return middle, m

    def Calculate_Outliers(self):

        Sorted_co_occurrence_dict = []

        for key1 in self.Similarity_dict:
            for key2 in self.Similarity_dict[key1]:
                Sorted_co_occurrence_dict.append(self.Similarity_dict[key1][key2])

        Sorted_co_occurrence_dict.sort()
        Quartiles1, Quartiles3 = self.cal(Sorted_co_occurrence_dict)
        Q1, Q3 = self.calc_Q(Quartiles1, Quartiles3)

        IQR = Q3 - Q1
        c = 4
        Smallest_outer = Q1 - (1.5 * c * IQR)
        Largest_outer = Q3 + (1.5 * c * IQR)

        outliers = []
        for value in Quartiles1:
            if value > Largest_outer:
                outliers.append(value)

        for value in Quartiles3:
            if value > Largest_outer:
                outliers.append(value)

        for k1 in self.Similarity_dict:
            for k2 in self.Similarity_dict[k1]:
                if outliers.__contains__(self.Similarity_dict[k1][k2]):
                    continue
                else:
                    if self.Similarity_dict[k1][k2] == 0:
                        continue
                    else:
                        self.Not_Outliers_dict[k1][k2] = self.Similarity_dict[k1][k2]

        return self.Not_Outliers_dict
