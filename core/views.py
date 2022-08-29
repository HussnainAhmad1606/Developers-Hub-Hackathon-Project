from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
# Create your views here.

db = settings.DB

def home(request):
    return render(request, "core/index.html")


def developers(request):
    devs = db.search_by_value('hackathon', 'developers', "id", "*", get_attributes=['*'])
    context = {"devs":devs}
    return render(request, 'core/developers.html', context)

def dev_profile(request, pk):
    dev = db.search_by_hash('hackathon', 'developers', [pk], get_attributes=['*'])[0]
    context = {"dev":dev}
    return render(request, 'core/dev_profile.html', context)

def add_developer(request):
    if request.method == "POST":
        data = request.POST
        db.insert('hackathon', 'developers', [{"name":data['name'], "skills":data['skills']}])
        messages.success(request, "Developer Profile Added Successfully")
        return redirect('homepage')
    return render(request, 'core/add_developer.html')

def searchDev(request):
    if request.method == "POST":
        location = request.POST.get("location")
        role = request.POST.get("role")
        skills = request.POST.get("skills")
        mini = request.POST.get("min")
        maxi = request.POST.get("max")
        experience = request.POST.get("experience")
        print(role)
        print(experience)
        devs = db.sql(f"SELECT * FROM hackathon.developers WHERE `skills` LIKE '%{skills}%' AND `experience`='{experience}' AND `location`='{location}' AND `role`='{role}' AND `currentCTC` BETWEEN '{mini}' AND '{maxi}';")
        print(devs)
        context = {"devs": devs, "length": len(devs)}
        return render(request, "core/search.html", context)

def update_developer(request, pk):
    if request.method == "POST":
        name = request.POST.get("name")
        skills = request.POST.get("skills")
        db.update('hackathon', 'developers', [{"id":pk,"name":name,"skills":skills}])
        messages.success(request, "Profile Updated Successfully")
        return redirect('homepage')

    dev = db.search_by_hash('hackathon', 'developers', [pk], get_attributes=['*'])[0]
    context = {"dev":dev}
    return render(request, 'core/update_developer.html', context)

def delete_developer(request, pk):
    if request.method == "POST":
        db.delete('hackathon', 'developers', [pk])
        messages.success(request, "Developer Profile Deleted Successfully")
        return redirect("developers")

def handleLogin(request):
    if request.method == "POST":
        data = request.POST
        user = authenticate(username=data["username"], password=data["password"])
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in Successfully")
            return redirect("homepage")
        else:
            messages.error(request, "Error! Make sure your credientials are correct & Try Again")

    return render(request, "core/login.html")


def handleSignup(request):
    if request.method == "POST":
        data = request.POST
        print(data["username"])
        if User.objects.filter(username=data["username"]).exists():
            messages.info(request, 'Username is already taken please choose different')
            return redirect("signup")
        elif User.objects.filter(email=data["email"]).exists():
            messages.info(request, 'Email is already taken')
            return redirect("signup")
        else:
            newUser = User.objects.create_user(data["username"], data["email"], data["password"])
            newUser.save()
            messages.success(request, "Account Created Successfully. You can login now.")
            return redirect("homepage")

    return render(request, "core/signup.html")

def handlelogout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Account Logout Success")
        return redirect("homepage")