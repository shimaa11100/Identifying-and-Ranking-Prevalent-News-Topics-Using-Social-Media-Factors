from nltk import WordNetLemmatizer, wordpunct_tokenize
from itertools import chain
import string
import nltk
import xlrd


# tweets_pre_processing: class contains functions are used to extract relevant from tweets

class tweets_pre_processing:

    # Default constructor used to initialize needed data structure to achieve our objective

    def __init__(self, stopwords=None, language="english", post_tags=None):
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

        # If user does not determine specific post tags list
        # Then used the post_tags list defined by developer
        # Otherwise we will use post tags list defined by the user
        if post_tags is None:
            self.post_tags = ['NN', 'JJ', 'JJR', 'JJS', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP']
        else:
            self.post_tags = post_tags

        # to_ignore: is set of combination of stopwords list and punctuation
        self.to_ignore = set(chain(self.stopwords, self.punctuations))

        # used to store all relevant terms related to tweet
        self.relevant_terms = None

        # to store each relevant term and its term frequency of all news articles
        self.term_document_frequency = {}

    # extract_keywords_from_text_method: is function used to get relevant terms from tweet
    def extract_relevant_terms_from_text_method(self, text):

        # get sentences from text
        sentences = nltk.tokenize.sent_tokenize(text)

        # to get all words in sentences after applying part of speech tagging and stopwords removal...
        phrase_list = self.apply_part_of_speech_method(sentences)

        # get relevant terms
        self.relevant_terms = self.get_tweets_keywords(phrase_list)

        # retrieve relevant terms
        return self.relevant_terms

    # apply_part_of_speech_method: is function used to apply part of speech on sentences
    def apply_part_of_speech_method(self, sentences):

        # contains all words after removing stopwords, punctuation and applying part of speech tagging
        phrase_list = set()

        # loop to get each sentence
        for sentence in sentences:

            # to store all
            cleaning_sentences = []

            # wordpunct_tokenize will split pretty much at all special symbols and treat them as separate units.
            words_list = wordpunct_tokenize(sentence)

            # remove stop words from sentence
            words_list = [w for w in words_list if w not in self.stopwords]

            # apply part of speech tagging for each word in list
            tagged = nltk.pos_tag(words_list)

            # loop to get each word and its tag
            for pos_tuple in tagged:
                hash_tag_check = 0

                # check is word contains # in first word
                if pos_tuple[0][0] == '#':
                    hash_tag_check = 1

                # if word contains # and its tag in post_tags then app word in list without #
                if hash_tag_check == 1 and pos_tuple[1] in self.post_tags:

                    cleaning_sentences.append(str(pos_tuple[0][1:]))
                # otherwise tag in  post_tags and length of word > 3 and word not in  to_ignore
                elif pos_tuple[1] in self.post_tags and pos_tuple[0] not in self.to_ignore and len(pos_tuple[0]) > 3:

                    # used to check word contains any punctuation in word
                    punctuation_check = 0

                    # check every character in word contains any punctuation inside word
                    for char in self.punctuations:

                        if str(pos_tuple[0]).__contains__(char):
                            punctuation_check = 1
                            break

                    # if word not contains any punctuation then add in list
                    if punctuation_check == 0:
                        cleaning_sentences.append(str(pos_tuple[0]))

            # add cleaning_sentences list in phrase_list
            phrase_list.update(cleaning_sentences)

        # retrieve phrase list
        return phrase_list

    # get_tweets_keywords: is function used to get relevant terms
    def get_tweets_keywords(self, phrase_list):

        final_result = set()

        # to lemmatize word
        lemmatizer = WordNetLemmatizer()

        # loop to get each word
        for word in phrase_list:

            # if word contains _
            if str(word).__contains__('_'):

                # split hash tag by _ to get words
                words_in_hash_tag = str.split(str(word), '_')

                # loop to get each word in hash tag
                for wx in words_in_hash_tag:

                    # apply lemmatization
                    w = lemmatizer.lemmatize(wx)

                    # add word in relevant terms set
                    final_result.add(str(w).lower())

                    # calculate term frequency
                    self.tweet_term_document_frequency(str(w).lower())
            else:
                # apply lemmatization
                w = lemmatizer.lemmatize(word)

                # add word in relevant terms set
                final_result.add(str(w).lower())
                # calculate term frequency
                self.tweet_term_document_frequency(str(w).lower())

        # retrieve relevant terms of tweet
        return final_result

    # to calculate term frequency of term
    def tweet_term_document_frequency(self, word):

        if word in self.term_document_frequency:
            self.term_document_frequency[word] += 1
        else:
            self.term_document_frequency[word] = 1


# get_required_data(): is function to get required data to construct key term graph
# Note: tweets_topics: is list contains topics names related to the user

def get_required_data(tweets_topics):

    # to store all relevant terms of all tweets
    tweets_keywords = set()

    # list to store each tweet relevant terms list for each tweet
    list_of_each_tweet_keywords = list()

    # to store each user and its tweets
    users_with_their_tweets = {}

    # to store users
    list_of_tweet_user = list()

    # object from tweets_pre_processing class to get main relevant terms of tweets
    tp = tweets_pre_processing()

    # open data set
    wb = xlrd.open_workbook(
        r'C:\Users\Ahmed AbdElhamed\Desktop\IdentifyingandRankingNewsUsingSocial Media\Tweets\tweetsdata.xlsx')

    # get first sheet
    sheet = wb.sheet_by_index(0)

    # loop to get each row in excel sheet
    for i in range(sheet.nrows):

        # check data row is related to topic name
        if list(tweets_topics).__contains__(sheet.cell_value(i, 1)):

            # get relevant terms of tweet
            relevant_terms = tp.extract_relevant_terms_from_text_method(sheet.cell_value(i, 2))

            # add in list of each tweet relevant terms
            list_of_each_tweet_keywords.append(list(relevant_terms))

            # add in tweets_keywords
            tweets_keywords.update(relevant_terms)

            # to handle problem @ in some names and other not
            # if contains @ then add name without @
            if str(sheet.cell_value(i, 4)).__contains__('@'):
                user = str(sheet.cell_value(i, 4))[1:]
                if user in users_with_their_tweets:
                    users_with_their_tweets[user].update(relevant_terms)
                else:
                    users_with_their_tweets[user] = relevant_terms
                # add user in list
                list_of_tweet_user.append(user)

            else:
                user = str(sheet.cell_value(i, 4))
                if user in users_with_their_tweets:
                    users_with_their_tweets[user].update(tp.relevant_terms)
                else:
                    users_with_their_tweets[user] = tp.relevant_terms
                # add user in list
                list_of_tweet_user.append(user)

    return tweets_keywords, tp.term_document_frequency, list_of_each_tweet_keywords, sheet.nrows, list_of_tweet_user, users_with_their_tweets


def tweets_key_term_extraction_method(tweets_topics):
    tweets_keywords, term_document_frequency, final_list_of_each_tweet_keywords, tweets_count, list_of_tweet_user, users_with_their_tweets = get_required_data(
        tweets_topics)
    return tweets_keywords, term_document_frequency, final_list_of_each_tweet_keywords, tweets_count, list_of_tweet_user, users_with_their_tweets
