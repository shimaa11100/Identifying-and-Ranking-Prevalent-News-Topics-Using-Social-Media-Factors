from rake_nltk import Rake
from collections import Counter
from itertools import chain, product
import networkx as nx
import math
import nltk
import string


"""All Classes and function in this scope used to extract keywords from news articles using text rank algorithm"""


# Note: This class used to extract terms from news articles using text rank algorithm only
# news_pre_processing: class contains functions are used to extract main keywords from news articles
class news_pre_processing:

    # Default constructor used to initialize needed data structure to achieve our objective
    def __init__(self, stopwords=None, language="english"):

        # If user does not determine specific stopwords list
        # Then used the stopwords list of natural language tool kit
        # Otherwise we will use stopwords list defined by the user
        # Note: We use stopwords list of english language
        if stopwords is None:
            self.stopwords = nltk.corpus.stopwords.words(language)
        else:
            self.stopwords = stopwords

        # We used punctuation too
        self.punctuations = string.punctuation + '’'

        # to_ignore: is set of combination of stopwords list and punctuation
        self.to_ignore = set(chain(self.stopwords, self.punctuations))

        # used to store all relevant terms related to news article
        self.relevant_terms = None

    # extract_keywords_from_text_method: is function to get all relevant terms from news article
    def extract_keywords_from_text_method(self, text):

        # get sentences from news article text
        sentences = nltk.tokenize.sent_tokenize(text)

        # get_news_key_terms: if fn used to get relevant terms from sentences
        self.relevant_terms = self.get_news_key_terms(sentences)

        # retrieve terms
        return self.relevant_terms

    # get_news_key_terms: is function used to get relevant terms from sentences
    def get_news_key_terms(self, sentences):

        # used to store all relevant terms of news article
        event_key_terms = set()

        # loop to get each sentence
        for sentence in sentences:

            # wordpunct_tokenize will split pretty much at all special symbols and treat them as separate units.
            words_list = nltk.wordpunct_tokenize(sentence)

            # remove all stopwords and punctuation from list
            words_list = [w for w in words_list if w not in self.to_ignore and len(w) > 3]

            # add relevant terms of sentence in event_key_terms
            event_key_terms.update(words_list)

        # retrieve relevant terms of news article
        return event_key_terms


# word2vec : is used to make term as vector
def word2vec(word):

    # count the characters in word
    cw = Counter(word)

    # pre-computes a set of the different characters
    sw = set(cw)

    # pre-computes the "length" of the word vector
    lw = math.sqrt(sum(c * c for c in cw.values()))

    # return a tuple
    return cw, sw, lw


# cos_dis: is function to calculate cosine similarity between 2 vectors
def cos_dis(v1, v2):

    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])

    # by definition of cosine distance we have
    return sum(v1[0][ch] * v2[0][ch] for ch in common) / v1[2] / v2[2]


# get_required_data_using_text_rank: is function used to get required data(news articles keywords...) needed to construct graph
def get_required_data_using_text_rank(news_articles):

    # used to store all keywords of news articles
    # set(): to avoid duplication
    news_keywords = set()

    # list to store keywords list of each news article
    list_of_each_keyword_list = list()

    # to store each news article with its keywords
    news_articles_with_keywords = {}

    # used to lemmatize the word
    lemmatizer = nltk.WordNetLemmatizer()

    # object from news_pre_processing class to get main keywords of news article
    news_article_pre_processing = news_pre_processing()

    # to store each keyword and its term frequency of all news articles
    term_document_frequency = {}

    # loop to get each news article
    for news_article in news_articles:

        # used to construct graph of news article keywords
        graph = nx.Graph()

        # get terms from news article
        terms = news_article_pre_processing.extract_keywords_from_text_method(news_article)

        # to store pair terms (u,v) with cosine similarity (w) between two words
        graph_edges = list()

        # loop to get each term with other terms
        for term1, term2 in product(terms, terms):
            # if first term not like second term
            if term1 != term2:
                # add first word and second word and cosine similarity between them
                graph_edges.append((lemmatizer.lemmatize(term1), lemmatizer.lemmatize(term2),
                                    cos_dis(word2vec(term1), word2vec(term2))))
        # add edges in graph
        graph.add_weighted_edges_from(graph_edges)

        # apply text rank algorithms
        # text rank => is modified version from pagerank
        dic = nx.pagerank(graph)

        # sort keywords by weight
        res = sorted(dic.items(), key=lambda x: x[1], reverse=True)

        # to get 1/3 * len of keywords
        count = math.ceil((1 / 3) * len(res))

        # to store keywords of news article
        event_keywords = set()

        # loop to get the top K keywords
        for i in range(count):
            # add keyword in news_keywords
            news_keywords.add(res[i][0])
            # add keyword in event_keywords
            event_keywords.add(res[i][0])

            # store term frequency
            if res[i][0] in term_document_frequency:
                term_document_frequency[res[i][0]] += 1
            else:
                term_document_frequency[res[i][0]] = 1
        # add news article keywords in list
        list_of_each_keyword_list.append(event_keywords)

        # add news article with its top keywords
        news_articles_with_keywords[news_article] = list(event_keywords)

    # retrieve required data
    return news_articles_with_keywords, news_keywords, term_document_frequency, list_of_each_keyword_list, len(
        news_articles)


"""#########################################End of Scope#########################################"""


"""All Classes and function in this scope used to extract keywords from news articles using rake algorithm"""


def get_required_data_using_rake(news_articles):

    # used to store all keywords of news articles
    # set(): to avoid duplication
    news_keywords = set()

    # list to store keywords list of each news article
    list_of_each_keyword_list = list()

    # to store each news article with its keywords
    news_articles_with_keywords = {}

    # used to lemmatize the word
    lemmatizer = nltk.WordNetLemmatizer()

    # to store each keyword and its term frequency of all news articles
    term_document_frequency = {}

    # object from class Rake contains functions for keywords extraction
    rake_algorithm = Rake()

    # loop to get each news article
    for news_article in news_articles:

        # used to extract keywords from text
        rake_algorithm.extract_keywords_from_text(news_article)

        # get top keywords after ranking
        key_words_list = rake_algorithm.get_ranked_phrases()

        # event_key_terms: used to store keywords of news article
        event_key_terms = set()

        # loop to get each ranked phrase
        for keyword in key_words_list:

            # split each phrase into words
            key_list = str(keyword).split(' ')

            # loop to get each keyword
            for word in key_list:

                # apply lemmatization
                w = lemmatizer.lemmatize(word)

                # add keyword in news_keywords and event_key_terms
                news_keywords.add(w)
                event_key_terms.add(w)

                # store word with it's document frequency
                if w in term_document_frequency:
                    term_document_frequency[w] += 1
                else:
                    term_document_frequency[w] = 1

        # add news article keywords in list
        list_of_each_keyword_list.append(event_key_terms)

        # add news article with its keywords
        news_articles_with_keywords[news_article] = list(event_key_terms)

    # retrieve required data
    return news_articles_with_keywords, news_keywords, term_document_frequency, list_of_each_keyword_list, len(
        news_articles)


"""################################### End of Scope ###################################"""


# Methods to call functions explained before

# for text rank algorithm
def news_key_term_extraction_method_using_text_rank(news_articles):

    news_articles_with_keywords, news_keywords, term_document_frequency, list_each_event_keys_topic, number_of_articles = get_required_data_using_text_rank(news_articles)

    return news_articles_with_keywords, news_keywords, term_document_frequency, list_each_event_keys_topic, number_of_articles


# for rake algorithm
def news_key_term_extraction_method_using_rake(news_articles):

    news_articles_with_keywords, news_keywords, term_document_frequency, list_each_event_keys_topic, number_of_articles = get_required_data_using_rake(
        news_articles)

    return news_articles_with_keywords, news_keywords, term_document_frequency, list_each_event_keys_topic, number_of_articles
