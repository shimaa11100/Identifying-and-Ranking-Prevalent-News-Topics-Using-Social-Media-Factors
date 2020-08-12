from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from rake_nltk import Rake

import UserDataManagement.MainData
from UserDataManagement.models import User, Topic
from NewsTopicsManagement.models import Article, History, Feedback
import datetime
import time
# Core of our project

from Preprocessing import Tweets_Keyterm_ExtractionPV
from Preprocessing import News_Keywords_ExtractionPV
from KeyTermGraphConstruction import Key_Term_Graph_ConstructionPV
from GraphClustering import ClusteringUsingNewmanAlgoPV
from ContentSelectionandRanking import NodeWeightingPV
from ContentSelectionandRanking import UserAttentionEstimationPV
from ContentSelectionandRanking import MediaFocusEstimationPV
from ContentSelectionandRanking import UserInteractionEstimationPV
from ContentSelectionandRanking import OveralRanking

Current = "Hello"


# Create your views here.
def load_news_page(request):
    if UserDataManagement.MainData.EnteredUser.UserEmail == '':
        return HttpResponseNotFound("Please You Should Sign in First")
    else:
        user = User.objects.get(pk=UserDataManagement.MainData.EnteredUser.UserEmail)
        return render(request, 'news.html', {'UserName': UserDataManagement.MainData.EnteredUser.UserName,
                                             'UserTopics': user.topic_set.all()})


def load_search_page(request):
    return render(request, 'Search.html', {"UserName": UserDataManagement.MainData.EnteredUser.UserName})


def load_recommended_topics_page(request):
    if UserDataManagement.MainData.EnteredUser.UserEmail == '':
        return HttpResponseNotFound("Please You Should Sign in First")
    else:
        user = User.objects.get(pk=UserDataManagement.MainData.EnteredUser.UserEmail)
        InterestedTopics = user.topic_set.all()
        alltopics = Topic.objects.all()
        history = History.objects.filter(UserEmailFK=UserDataManagement.MainData.EnteredUser.UserEmail)
        words = set()
        recommendtopics = set()
        for i in history:
            text = str(i).split('-')
            a = text[0][:len(text[0]) - 1]
            words.add(a)

        checktopic = 0
        searchbytopic = set()
        searchbykeword = set()
        for x in words:
            for topic in alltopics:
                if str(x).lower() == str(topic.TopicName).lower():
                    checktopic = 1
                    break
            if checktopic == 1:
                searchbytopic.add(x.capitalize())
            else:
                searchbykeword.add(x.lower())
            checktopic = 0

        checkinterstornot = 0

        for s in searchbytopic:
            for i in InterestedTopics:
                if str(i.TopicName).__eq__(s):
                    checkinterstornot = 1
                    break
            if checkinterstornot == 0:
                recommendtopics.add(s)
            checkinterstornot = 0
    for x in searchbykeword:
        RakeAlgoritm = Rake()
        RakeAlgoritm.extract_keywords_from_text(x)
        KeyWordsList1 = RakeAlgoritm.get_ranked_phrases()
        for topic in alltopics:
            for article in topic.article_set.all():
                RakeAlgoritm.extract_keywords_from_text(article.ArticleDescription)
                KeyWordsList = RakeAlgoritm.get_ranked_phrases()
                intersection = set(KeyWordsList) & set(KeyWordsList1)
                if intersection == set():
                    continue
                else:
                    w = 0
                    for a in InterestedTopics:
                        if str(article.TopicNameFK).__eq__(a):
                            w = 1
                            break
                    if w == 0:
                        recommendtopics.add(article.TopicNameFK)
                    w = 0
        return render(request, 'recommend.html', {"topics": recommendtopics})


def save_topics(request):
    if request.method == 'POST':
        topics = request.POST.getlist('checks[]')
        if len(topics) == 0:
            return redirect('NewsTopicsManagement:LoadRecommendedTopics')
        else:
            new_user = User.objects.get(pk=UserDataManagement.MainData.EnteredUser.UserEmail)
            for i in topics:
                a = Topic.objects.get(pk=i)
                a.TopicMembers.add(new_user)
            return redirect('NewsTopicsManagement:NewsPage')


def load_user_history_page(request):
    if UserDataManagement.MainData.EnteredUser.UserEmail == '':
        return HttpResponseNotFound("Please You Should Sign in First")
    else:
        user_history = History.objects.filter(UserEmailFK=UserDataManagement.MainData.EnteredUser.UserEmail)
        return render(request, 'history.html', {"histories": user_history})


def load_entertainment_news_page(request):
    if UserDataManagement.MainData.EnteredUser.UserEmail == '':
        return HttpResponseNotFound("Please You Should Sign in First")
    else:
        topic = Topic.objects.get(pk="Entertainment")
        return render(request, 'NewsTopic.html',
                      {"Topic": "Entertainment", "UserName": UserDataManagement.MainData.EnteredUser.UserName,
                       "articles": topic.article_set.all()})


def load_health_news_page(request):
    if UserDataManagement.MainData.EnteredUser.UserEmail == '':
        return HttpResponseNotFound("Please You Should Sign in First")
    else:
        topic = Topic.objects.get(pk="Health")
        return render(request, 'NewsTopic.html',
                      {"Topic": "Health", "UserName": UserDataManagement.MainData.EnteredUser.UserName,
                       "articles": topic.article_set.all()})


def load_sports_news_page(request):
    if UserDataManagement.MainData.EnteredUser.UserEmail == '':
        return HttpResponseNotFound("Please You Should Sign in First")
    else:
        topic = Topic.objects.get(pk="Sports")
        return render(request, 'NewsTopic.html',
                      {"Topic": "Sports", "UserName": UserDataManagement.MainData.EnteredUser.UserName,
                       "articles": topic.article_set.all()})


def load_science_news_page(request):
    if UserDataManagement.MainData.EnteredUser.UserEmail == '':
        return HttpResponseNotFound("Please You Should Sign in First")
    else:
        topic = Topic.objects.get(pk="Science")
        return render(request, 'NewsTopic.html',
                      {"Topic": "Science", "UserName": UserDataManagement.MainData.EnteredUser.UserName,
                       "articles": topic.article_set.all()})


def load_world_news_page(request):
    if UserDataManagement.MainData.EnteredUser.UserEmail == '':
        return HttpResponseNotFound("Please You Should Sign in First")
    else:
        topic = Topic.objects.get(pk="World")
        return render(request, 'NewsTopic.html',
                      {"Topic": "World", "UserName": UserDataManagement.MainData.EnteredUser.UserName,
                       "articles": topic.article_set.all()})


def load_nation_news_page(request):
    if UserDataManagement.MainData.EnteredUser.UserEmail == '':
        return HttpResponseNotFound("Please You Should Sign in First")
    else:
        topic = Topic.objects.get(pk="Nation")
        return render(request, 'NewsTopic.html',
                      {"Topic": "Nation", 'UserName': UserDataManagement.MainData.EnteredUser.UserName,
                       "articles": topic.article_set.all()})


def load_business_news_page(request):
    if UserDataManagement.MainData.EnteredUser.UserEmail == '':
        return HttpResponseNotFound("Please You Should Sign in First")
    else:
        topic = Topic.objects.get(pk="Business")
        return render(request, 'NewsTopic.html',
                      {"Topic": "Business", "UserName": UserDataManagement.MainData.EnteredUser.UserName,
                       "articles": topic.article_set.all()})


def search_keyword(request):
    if request.method == "POST":
        search_title = request.POST["search_title"]
        if search_title is None:
            return HttpResponse("found")
        user = User.objects.get(pk=UserDataManagement.MainData.EnteredUser.UserEmail)
        history = History()
        history.Date_Time = datetime.datetime.now()
        history.SearchTitle = search_title
        history.UserEmailFK = user
        history.save()
        topics = Topic.objects.all()
        for topic in topics:
            if (str(topic.TopicName).lower()) == (str(search_title).lower()):
                return render(request, "Search.html", {"articles": topic.article_set.all(),
                                                       "UserName": UserDataManagement.MainData.EnteredUser.UserName,
                                                       "check": "1"})

        Newslist = []
        RakeAlgoritm = Rake()
        RakeAlgoritm.extract_keywords_from_text(search_title)
        KeyWordsList1 = RakeAlgoritm.get_ranked_phrases()
        for topic in topics:
            for article in topic.article_set.all():
                RakeAlgoritm.extract_keywords_from_text(article.ArticleDescription)
                KeyWordsList = RakeAlgoritm.get_ranked_phrases()
                intersection = set(KeyWordsList) & set(KeyWordsList1)
                if intersection == set():
                    continue
                else:
                    Newslist.append(article.ArticleDescription)
        if len(Newslist) != 0:
            return render(request, "Search.html", {"articles": Newslist,
                                                   "UserName": UserDataManagement.MainData.EnteredUser.UserName,
                                                   "check": "2"})

    return HttpResponse("Notfound")


def load_send_feedback_page(request, event):
    UserDataManagement.MainData.feedback.Current = event
    UserDataManagement.MainData.feedback.Topic = str(request.path).split('/')[3]
    return render(request, 'SendFeedback.html')


def add_feedback(request):
    topic = Topic.objects.get(pk=UserDataManagement.MainData.feedback.Topic)
    for t in topic.article_set.all():
        if (str(t.ArticleDescription[0:len(t.ArticleDescription) - 1]).lower()) == (
                str(UserDataManagement.MainData.feedback.Current).lower()):
            article = Article.objects.get(ArticleDescription=t.ArticleDescription)
            user = User.objects.get(pk=UserDataManagement.MainData.EnteredUser.UserEmail)
            feedback_title = request.POST["Feedback"]
            new_feedback = Feedback.objects.create(FeedbackTitle=feedback_title, UserEmailFK=user, ArticleFK=article)
            new_feedback.save()
            break
    if UserDataManagement.MainData.feedback.Topic == "Health":
        return redirect('NewsTopicsManagement:HealthNewsPage')
    elif UserDataManagement.MainData.feedback.Topic == "Entertainment":
        return redirect('NewsTopicsManagement:EntertainmentNewsPage')
    elif UserDataManagement.MainData.feedback.Topic == "Science":
        return redirect('NewsTopicsManagement:ScienceNewsPage')
    elif UserDataManagement.MainData.feedback.Topic == "World":
        return redirect('NewsTopicsManagement:WorldNewsPage')
    elif UserDataManagement.MainData.feedback.Topic == "Business":
        return redirect('NewsTopicsManagement:BusinessNewsPage')
    elif UserDataManagement.MainData.feedback.Topic == "Nation":
        return redirect('NewsTopicsManagement:NationNewsPage')
    elif UserDataManagement.MainData.feedback.Topic == "Sports":
        return redirect('NewsTopicsManagement:SportsNewsPage')


def load_view_feedback_page(request, event):
    l = []
    topic = Topic.objects.get(pk="Health")
    for t in topic.article_set.all():
        if t.ArticleDescription[0:len(t.ArticleDescription) - 1] == event:
            article = Article.objects.get(ArticleDescription=t.ArticleDescription)
            feedback = Feedback.objects.all()

            for i in feedback:
                if i.ArticleFK == article:
                    l.append(i)
            break
    return render(request, 'ViewFeedback.html', {'feedback_of_event': l})


def get_top_news(request):

    # get current user
    user = User.objects.get(pk=UserDataManagement.MainData.EnteredUser.UserEmail)
    # get all topics related to the user
    news_topics_related_to_user = list(user.topic_set.all())
    # news_articles_of_topics: to store all articles of news topics related to the user
    news_articles_of_topics = list()
    # news_topics_name_related_to_user: to store topics name related by user
    news_topics_name_related_to_user = list()
    # get news articles for each topic
    for news_topic in news_topics_related_to_user:
        news_topics_name_related_to_user.append(str(news_topic.TopicName))
        for news_article in list(news_topic.article_set.all()):
            news_articles_of_topics.append(str(news_article))

    start_time = time.time()
    # Tweets and News Pre-processing
    T, tweets_terms_frequency, list_of_each_tweet_keywords, total_tweets, list_of_tweet_user, list_of_users_with_tweets = Tweets_Keyterm_ExtractionPV.tweets_key_term_extraction_method(news_topics_name_related_to_user)
    news_articles, N, news_terms_frequency, list_of_each_news_keywords, total_news = News_Keywords_ExtractionPV.news_key_term_extraction_method_using_text_rank(news_articles_of_topics)

    # Key term Graph Construction
    graph = Key_Term_Graph_ConstructionPV.KeyTermGraphConstruction(T, N, tweets_terms_frequency, news_terms_frequency,
                                                                   total_tweets, total_news,
                                                                   list_of_each_tweet_keywords)
    graph.relevant_key_term_identification()
    graph.key_term_similarity_estimation(0)
    edges_weights = graph.Calculate_Outliers()

    # Graph Clustering
    clusters = ClusteringUsingNewmanAlgoPV.clustering(edges_weights)
    clusters.newman_algorithm_with_improvement()
    clusters.get_topic_clusters()
    total_graph, clusters_nodes = clusters.before_clustering, clusters.sub_graphs

    # Node Weighting Process
    nodes_weights = NodeWeightingPV.NodeWeighting(total_graph, clusters_nodes)
    nodes_weight = nodes_weights.calculate_nodes_weight()
    sorted_nodes_weight = list()
    for i in nodes_weight:
        ress = sorted(i.items(), key=lambda x: x[1], reverse=True)
        print(ress)
        sorted_nodes_weight.append(dict(ress))

    # User Attention Estimation
    UserAttentionEst = UserAttentionEstimationPV.USerAttention(list_of_each_tweet_keywords, list_of_tweet_user,
                                                               sorted_nodes_weight)
    UserAttentionEst.get_tweets_related_to_each_topic()
    UserAttentionEst.get_unique_users_related_to_tweets()
    user_attention_for_each_cluster = UserAttentionEst.calculate_user_attention_estimation_for_each_cluster()

    # Media Focus
    MediaFocusEst = MediaFocusEstimationPV.MediaFocus(list_of_each_news_keywords, sorted_nodes_weight)
    MediaFocusEst.get_news_related_to_each_topic()
    media_focus_for_each_cluster = MediaFocusEst.calculate_media_focus_estimation_for_each_cluster()

    # User Interaction
    UserInteractionEst = UserInteractionEstimationPV.UserInteraction()
    UserInteractionEst.get_users_related_topic_clusters(list_of_users_with_tweets,
                                                        clusters_nodes)
    UserInteractionEst.generate_social_graph_topic_clusters_with_improvement()
    UserInteractionEst.calculate_reciprocity_topic_clusters()
    user_interaction_for_each_cluster = UserInteractionEst.get_user_interaction_topic_cluster()

    # Overall ranking
    overall_ranking = OveralRanking.OverallRanking(user_attention_for_each_cluster, media_focus_for_each_cluster,
                                                   user_interaction_for_each_cluster)
    overall_ranking_for_each_cluster = overall_ranking.calculate_overall_ranking_for_each_cluster()
    res = sorted(overall_ranking_for_each_cluster.items(), key=lambda x: x[1], reverse=True)
    print("--- %s seconds ---" % (time.time() - start_time))
    # Display News
    final_news = list()

    for topic in res:

        topic_keywords = sorted_nodes_weight[topic[0]]
        news_articles_of_topic = list()
        for keyword in topic_keywords.keys():
            for news_article, news_keywords in news_articles.items():
                if news_keywords.__contains__(keyword):
                    if not(news_articles_of_topic.__contains__(news_article)):
                        news_articles_of_topic.append(news_article)
        final_news.append(list(news_articles_of_topic))

    return render(request, 'TopNews.html', {'UserName': UserDataManagement.MainData.EnteredUser.UserName, 'final_news': final_news})


def sign_out(request):
    UserDataManagement.MainData.EnteredUser.UserEmail = ''
    return redirect('UserDataManagement:HomePage')
