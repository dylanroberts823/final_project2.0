from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import connection

from users.models import Project, Tag, Request, RequestStatus
from .forms import CreateProjectForm, SearchForm, CreateRequestForm, CreateTagForm

# Create your views here.
def home_view(request):
    #Determine the base and projects
    if not request.user.is_authenticated:
        base = "users/base.html"
        #One raw sql query for final_project requirements
        projects = Project.objects.raw("SELECT * FROM users_project")
    else:
        user = request.user
        base = "projects/base.html"
        projects = Project.objects.exclude(contributors = request.user).exclude(manager = request.user).all()

    #Modify the projects to be returned if it's a post request
    if request.method == "POST":
        #Create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        #Check whether it's valid
        if form.is_valid():
            #Since it's valid, filter the projects by their tag
            tag = form.cleaned_data['tag']
            tag = Tag.objects.get(tag = tag)
            projects = Project.objects.filter(tags = tag.id)

    #Render the page with the appropriate context
    context = {
        "projects": projects,
        "base": base,
        "form": SearchForm()
    }
    return render(request, "projects/home.html", context)

def create_tag_view(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    if request.method == 'POST':
        #Create a form instance and populate it with data from the request:
        form = CreateTagForm(request.POST)
        #Check whether it's valid
        if form.is_valid():
            #Get the form data
            tag = form.cleaned_data['tag']

            #Create the tag
            tag = Tag.objects.create(tag = tag)

            #Redirect to previous page
            next = request.POST.get('next', '/')
            return redirect(next)
    #Since it's a get request, render the page with the form
    else:
        context = {
            "form": CreateTagForm(),
            "next": request.META['HTTP_REFERER']
        }
        return render(request, "projects/create_tag.html", context)

def create_view(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    if request.method == 'POST':
        #Create a form instance and populate it with data from the request:
        form = CreateProjectForm(request.POST)
        #Check whether it's valid
        if form.is_valid():
            #Get the form data
            name = form.cleaned_data['name']
            manager = request.user
            status = form.cleaned_data['status']
            contributors = form.cleaned_data['contributors']
            description = form.cleaned_data['description']

            #Create the project
            project = Project.objects.create(name = name, manager = manager, status = status, description = description)
            for contributor in contributors:
                project.contributors.add(contributor)

            #Redirect to manage
            return redirect('projects:manage')
    else:
        form = CreateProjectForm()

    return render(request, "projects/create.html", {'form': form})

def manage_view(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    context = {
        "managed_projects": request.user.manager.all(),
        "contributed_projects": request.user.contributor.all()
    }
    return render(request, "projects/manage.html", context)

def manage_project_view(request, project_id):
    #Get the project in question
    project = Project.objects.get(pk = project_id)

    #Set the appropriate base
    if not request.user.is_authenticated:
        base = "users/base.html"
    else:
        base ="projects/base.html"
    #Check whether the user is the contributor, the manager, or viewer
    #Return the appropriate html page
    if project.manager == request.user:
        #Pre-fill the form with all the appropriate fields
        data = {'name': project.name,
                'description': project.description,
                'status': project.status,
                'contributors': project.contributors.all(),
                'tags': project.tags.all()}
        form = CreateProjectForm(initial=data)

        #Create the context
        context = {'form': form,
                   'project': project,
                   'base': base}
        return render(request, "projects/project_manager.html", context)

    elif project.contributors.filter(id = request.user.id).count() != 0:
        role = "Contributor"
    else:
        role = "Viewer"
    #Establish the context
    context = {
        "project": project,
        "role": role,
        'base': base
    }
    return render(request, "projects/project.html", context)

def modify_project_view(request, project_id):
    if request.method == 'POST':
        #Get the current project
        project = Project.objects.get(pk = project_id)

        #Create a form instance and populate it with data from the request:
        form = CreateProjectForm(request.POST)
        #Check whether it's valid
        if form.is_valid():
            #Edit the project with the form data
            project.name = form.cleaned_data['name']
            project.status = form.cleaned_data['status']
            project.description = form.cleaned_data['description']

            #Create a separate loop for contributors and tags
            project.contributors.clear()
            for contributor in form.cleaned_data['contributors']:
                project.contributors.add(contributor)

            project.tags.clear()
            for tag in form.cleaned_data['tags']:
                project.tags.add(tag)

            project.save()

    #Redirect to manage
    return redirect('projects:manage')

def request_view(request, project_id):
    if request.method == "POST":
        #Get the information from the form
        form = CreateRequestForm(request.POST)
        #Check whether it's valid
        if form.is_valid():
            note = form.cleaned_data['note']

            #Create the new Request
            #Second required SQL code
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users_request (sender_id, project_id, status_id, note) VALUES (%s, %s, %s, %s)", [request.user.id, project_id, 3, note])

        return redirect('projects:myrequests')
    else:
        #If the user isn't signed in, redirect them to the signin page
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"next":request.path})
        #If the user is signed in but is already a member of the team, redirect them to the project page
        project = Project.objects.get(pk = project_id)
        if project.manager == request.user or request.user.contributor.filter(id=project.id).exists():
            return redirect(reverse('projects:manage_project', args=(project_id,)))
        form = CreateRequestForm()
        context = {
            "project": project,
            "form": form
        }
        return render(request, "projects/request.html", context)

def myrequests_view(request):
    user = request.user

    context = {
        "sent_requests": Request.objects.filter(sender=request.user),
        "received_requests": Request.objects.filter(project__manager = user)
    }
    return render(request, "projects/myrequests.html", context)

#If the link to approve a request is clicked
def approve_view(request, request_id):
    received_request = Request.objects.get(pk = request_id)
    if received_request.project.manager == request.user:
        #Change the status of the user
        received_request.status = RequestStatus.objects.get(status = 'Approved')
        received_request.save()

        #Add the sender to the contributors list
        received_request.project.contributors.add(received_request.sender)

        return redirect('projects:myrequests')
    else:
        raise Http401("You need to be a manager to modify the status of a request")

#If the link to deny a request is clicked
def deny_view(request, request_id):
    received_request = Request.objects.get(pk = request_id)
    if received_request.project.manager == request.user:
        received_request.status = RequestStatus.objects.get(status = 'Denied')
        received_request.save()
        return redirect('projects:myrequests')
    else:
        raise Http401("You need to be a manager to modify the status of a request")

def request_modification_view(request, request_id, modification_id):
    #Move into a try statement
    received_request = Request.objects.get(pk = request_id)

    #If they are a manager, modify the request accordingly
    if received_request.project.manager == request.user:
        received_request.status = modification_id
        #received_request.note = note
        received_request.save()
        return redirect('projects:myrequests')
    else:
        raise Http401("You need to be a manager to modify the status of a request")
