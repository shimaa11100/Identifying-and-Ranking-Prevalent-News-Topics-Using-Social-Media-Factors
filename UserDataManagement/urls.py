from django.conf.urls import url
from . import views

app_name = 'UserDataManagement'

urlpatterns = [

    # /SociRank/
    url(r'^$', views.load_home_page, name="HomePage"),

    # /SociRank/register
    url(r'^Register/$', views.load_register_page, name="RegisterPage"),

    # /SociRank/register/register
    url(r'^register/$', views.check_sign_up_data, name="CheckSignUPData"),

    # /SociRank/InterestingTopics
    url(r'^InterestingTopics/$', views.load_topics_page, name="InterestingTopicsPage"),

    # /SociRank/Interestingtopics
    url(r'^Interestingtopics/$', views.check_selected_topics, name="CheckSelectedTopics"),

    # /SociRank/login
    url(r'^login$', views.load_login_page, name="LoginPage"),

    # /SociRank/Login
    url(r'^Login$', views.login, name="CheckLoginData"),




]
