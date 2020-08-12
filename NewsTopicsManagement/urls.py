from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'NewsTopicsManagement'

urlpatterns = [

    # /SociRank/UserHistory
    url(r'^UserHistory/$', views.load_user_history_page, name="UserHistoryPage"),

    # /SociRank/Signout
    url(r'^Signout/$', views.sign_out, name="SignOut"),

    # /SociRank/NewsPage
    url(r'^NewsPage/$', views.load_news_page, name="NewsPage"),

    # /SociRank/NewsPage/Business
    url(r'^NewsPage/Business/$', views.load_business_news_page, name="BusinessNewsPage"),

    # /SociRank/NewsPage/Science
    url(r'^NewsPage/Science/$', views.load_science_news_page, name="ScienceNewsPage"),

    # /SociRank/NewsPage/Health
    url(r'^NewsPage/Health/$', views.load_health_news_page, name="HealthNewsPage"),

    # /SociRank/NewsPage/Sports
    url(r'^NewsPage/Sports/$', views.load_sports_news_page, name="SportsNewsPage"),

    # /SociRank/NewsPage/World
    url(r'^NewsPage/World/$', views.load_world_news_page, name="WorldNewsPage"),

    # /SociRank/NewsPage/Entertainment
    url(r'^NewsPage/Entertainment/$', views.load_entertainment_news_page, name="EntertainmentNewsPage"),

    # /SociRank/NewsPage/Nation
    url(r'^NewsPage/Nation/$', views.load_nation_news_page, name="NationNewsPage"),

    # /SociRank/NewsPage/Search
    url(r'^NewsPage/Search/$', views.load_search_page, name="SearchPage"),

    # /SociRank/NewsPage/search
    url(r'^NewsPage/searchdata/$', views.search_keyword, name="Search"),

    # /SociRank/NewsPage/RecommendedTopics/
    url(r'^NewsPage/RecommendedTopics/$', views.load_recommended_topics_page, name="LoadRecommendedTopics"),

    # /SociRank/NewsPage/SaveTopics/
    url(r'^NewsPage/SaveTopics/$', views.save_topics, name="SaveTopics"),

    # /SociRank/NewsPage/Business/Event/SendFeedback/
    path('NewsPage/Business/<str:event>/SendFeedback/', views.load_send_feedback_page, name="SendFeedback"),

    # /SociRank/NewsPage/Health/Event/SendFeedback/
    path('NewsPage/Health/<str:event>/SendFeedback/', views.load_send_feedback_page, name="SendFeedback"),

    # /SociRank/NewsPage/Sports/Event/SendFeedback/
    path('NewsPage/Sports/<str:event>/SendFeedback/', views.load_send_feedback_page, name="SendFeedback"),

    # /SociRank/NewsPage/Nation/Event/SendFeedback/
    path('NewsPage/Nation/<str:event>/SendFeedback/', views.load_send_feedback_page, name="SendFeedback"),

    # /SociRank/NewsPage/Entertainment/Event/SendFeedback/
    path('NewsPage/Entertainment/<str:event>/SendFeedback/', views.load_send_feedback_page, name="SendFeedback"),

    # /SociRank/NewsPage/World/Event/SendFeedback/
    path('NewsPage/World/<str:event>/SendFeedback/', views.load_send_feedback_page, name="SendFeedback"),

    # /SociRank/NewsPage/Science/Event/SendFeedback/
    path('NewsPage/Science/<str:event>/SendFeedback/', views.load_send_feedback_page, name="SendFeedback"),

    # /SociRank/NewsPage/TopNews/
    url(r'^NewsPage/TopNews/$', views.get_top_news, name="TopNews"),

    # /SociRank/NewsPage/AddFeedback/
    path('NewsPage/addFeedback/', views.add_feedback, name="AddFeedback"),

    # /SociRank/NewsPage/Entertainment/Event/ViewFeedback/
    path('NewsPage/Entertainment/<str:event>/ViewFeedback/', views.load_view_feedback_page, name="ViewFeedback"),

    # /SociRank/NewsPage/ViewFeedback/
    path('NewsPage/Health/<str:event>/ViewFeedback/', views.load_view_feedback_page, name="ViewFeedback"),

    # /SociRank/NewsPage/Sports/event/ViewFeedback/
    path('NewsPage/Sports/<str:event>/ViewFeedback/', views.load_view_feedback_page, name="ViewFeedback"),

    # /SociRank/NewsPage/Nation/Event/ViewFeedback/
    path('NewsPage/Nation/<str:event>/ViewFeedback/', views.load_view_feedback_page, name="ViewFeedback"),

    # /SociRank/NewsPage/World/Event/ViewFeedback/
    path('NewsPage/World/<str:event>/ViewFeedback/', views.load_view_feedback_page, name="ViewFeedback"),

    # /SociRank/NewsPage/Business/Event/ViewFeedback/
    path('NewsPage/Business/<str:event>/ViewFeedback/', views.load_view_feedback_page, name="ViewFeedback"),

    # /SociRank/NewsPage/Science/Event/ViewFeedback/
    path('NewsPage/Science/<str:event>/ViewFeedback/', views.load_view_feedback_page, name="ViewFeedback"),

]


