from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import datetime
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .search import search_data
from coreApp.scripts.techNewsAPI import getTechNews


# Create your views here.
#hot_topics
hot_topics = getTechNews()

@login_required(login_url="/login/")
def tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(user =request.user,created_at__gte = datetime.datetime.now().date())
        if(tasks.count()!=0):
            page = request.GET.get("page", 1)
            p = Paginator(tasks, 25)
            try:
                tasks = p.page(page)
            except:
                tasks = p.page(1)
                
        recent_tasks = Task.objects.filter(user=request.user).order_by("-created_at")
        print(tasks)
        # context={"blogs": blogs, "page_obj": blogs, "recent_blogs": recent_blogs}
        context = {"tasks": tasks , "page_obj": tasks,"recent_tasks": recent_tasks,'hot_topics':hot_topics}
        return render(request, "task.html",context)
    
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        obj = Task.objects.create(user = User.objects.get(username = request.user.username), title=title, description=description)
        # registration_mail(email)
        task_id = obj.id
        query_string = title
        
        try:
            search_data(query_string,task_id)
        except Exception as e:
            messages.success(request, "Please enter a descriptive task ")
            return redirect("/core/task/")  # recorded
        
        messages.success(request, "Your task has been added.")
        return redirect("/core/task/")  # recorded
    return render(request, "task.html")



@login_required(login_url="/login/")
def planYourDay(request):
    tasks = Task.objects.filter(user =request.user,created_at__gte = datetime.datetime.now().date())
    if(tasks.count()!=0):
        page = request.GET.get("page", 1)
        p = Paginator(tasks, 6)
        try:
            tasks = p.page(page)
        except:
            tasks = p.page(1)
    recent_tasks = Task.objects.filter(user=request.user).order_by("-created_at")
    print(tasks)
    # context={"blogs": blogs, "page_obj": blogs, "recent_blogs": recent_blogs}
    context = {"tasks": tasks , "page_obj": tasks,"recent_tasks": recent_tasks}
    return render(request, "planYourDay.html",context)

@login_required(login_url="/login/")
def addTask(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        obj = Task.objects.create(user = User.objects.get(username = request.user.username), title=title, description=description)
        # registration_mail(email)
        task_id = obj.id
        query_string = title
        try:
            search_data(query_string,task_id)
        except Exception as e:
            messages.success(request, "Please enter a descriptive task ")
            return redirect("/addTask/")  # recorded
        messages.success(request, "Your task has been added.")
        return redirect("/planYourDay/")  # recorded
    return render(request, "addTask.html")

@login_required(login_url="/login")
def home(request):
    context= []
    today_tasks= list(Task.objects.filter(user =request.user,created_at__gte = datetime.datetime.now().date()).values())
    print(today_tasks)
    resource_obj = []
    videos = []
    resource_dict = {}
    for t in today_tasks:
        # print(t["id"])
        resources = list(Video.objects.filter(task = t["id"]).order_by('-score').values())[:3]
        resource = resources
        task = t["title"]
        resource_dict = {"task": task, "video": resource}
        # print(resources)
        # break
        videos.append(resource_dict)
        resource_obj.append(resources)
        
    #hot_topics
    hot_topics = getTechNews()
        
        
    #blogs
    topic_names = ["django","python","java",]   
    
    
    
    try:    
        # context = {"videos":  resource_obj, "tasks": today_tasks,"tvideos": videos}
        context = {"tvideos":videos,"hot_topics":hot_topics}
    except:
        context = {"videos": ""}
    print("********************************")
    print(context)
    # resources = Resource.objects.filter(tas)
    return render(request, "index.html",context)
    