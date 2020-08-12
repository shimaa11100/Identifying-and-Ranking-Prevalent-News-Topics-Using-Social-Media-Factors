from django.shortcuts import render
from .models import User, Topic
from django.shortcuts import redirect
import UserDataManagement.MainData
from django.http import HttpResponseNotFound


# User Data Management views here.
def load_home_page(request):
    return render(request, 'HomePage.html')


def load_login_page(request):
    return render(request, 'login.html')


def load_register_page(request):
    return render(request, 'Register.html')


def check_sign_up_data(request):
    if request.method == "POST":
        socirankusers = User.objects.all()
        if len(socirankusers) != 0:
            for socirankuser in socirankusers:
                if socirankuser.UserEmail == (request.POST["email"]):
                    context = {'Check': "UserEmail", "Message": "UserMail already exist"}
                    return render(request, 'Register.html', context)
            if (request.POST["pass"]) != (request.POST["repeat-pass"]):
                context = {'Check': "pass", "Message": "password does not match", "re": request.path}
                return render(request, 'Register.html', context)

            else:
                user = User.objects.create(UserEmail=request.POST["email"], UserName=request.POST["username"],
                                           UserPassword=request.POST["pass"])
                user.save()
                UserDataManagement.MainData.EnteredUser.UserEmail = request.POST["email"]
                return redirect('UserDataManagement:InterestingTopicsPage')
        else:
            user = User.objects.create(UserEmail=request.POST["email"], UserName=request.POST["username"],
                                       UserPassword=request.POST["pass"])
            user.save()
            UserDataManagement.MainData.EnteredUser.UserEmail = request.POST["email"]
            return redirect('UserDataManagement:InterestingTopicsPage')


def load_topics_page(request):
    return render(request, 'choosetopics.html')


def check_selected_topics(request):
    topics = request.POST.getlist('checks[]')
    if len(topics) == 0:
        return redirect('UserDataManagement:InterestingTopicsPage')
    else:
        new_user = User.objects.get(pk=UserDataManagement.MainData.EnteredUser.UserEmail)
        for i in topics:
            a = Topic.objects.get(pk=i)
            a.TopicMembers.add(new_user)
        return redirect('UserDataManagement:LoginPage')


def login(request):
    email = request.POST['Email']
    password = request.POST['pass']
    users = User.objects.all()
    for x in users:
        if str(email) == (str(x.UserEmail)) and str(password) == (str(x.UserPassword)):
            UserDataManagement.MainData.EnteredUser.UserEmail = email
            entered_user = User.objects.get(pk=email)
            UserDataManagement.MainData.EnteredUser.UserName = entered_user.UserName
            return redirect('NewsTopicsManagement:NewsPage')
    return HttpResponseNotFound("Email or password invalid")

