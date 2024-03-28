from django.shortcuts import render
from .models import Animal, Task, Worker

# Create your views here.


def animal_list(request):
    animal = Animal.objects.all()[:10]

    return render(request, "animals.html", {"animals": animal})


def worker_dash(request):
    tasks = Task.objects.all()
    animals = Animal.objects.all()
    workers = Worker.objects.all()

    return render(
        request,
        "worker_dashboard.html",
        {
            "tasks": tasks,
            "animals": animals,
            "workers": workers,
        },
    )


def home(request):

    return render(request, "home.html", {})


def adopt(request):

    return render(request, "adopt.html", {})


def about_view(request):
    return render(request, "about.html")


def login(request):

    return render(request, "login.html", {})


def filter_tasks(request):
    """
    A POST request to this view should contain a 'filter' parameter with a value of 'completed',
    'incomplete', or 'all'. This view will return a list of tasks based on the filter value.
    Additional filtering logic can be added as needed. See worker_dashboard.html for an idea of
    how to structure the form that will send the POST request.
    """
    completion_status = request.POST.get("filter")
    assignee = request.POST.get("assignee")
    animal = request.POST.get("animal")

    filter_params = {}

    if completion_status == "completed":
        filter_params["completion_datetime__isnull"] = False
    elif completion_status == "incomplete":
        filter_params["completion_datetime__isnull"] = True

    if assignee:
        filter_params["assignee"] = assignee

    if animal:
        filter_params["animal"] = animal

    tasks = Task.objects.filter(**filter_params)

    return render(request, "task_list.html", {"tasks": tasks})


def sort_tasks(request):
    """
    A POST request to this view should contain a 'sort' parameter with a value of 'title',
    'due_date', or 'creation_datetime'. This view will return a list of tasks sorted by the
    specified field. Again, see worker_dashboard.html for an idea of how to structure the form
    that will send the POST request.
    """
    sort_value = request.POST.get("sort")

    # default sort in case of unexpected sort values
    sort_key = "title"
    if sort_value in ["due_date", "creation_datetime"]:
        sort_key = sort_value

    tasks = Task.objects.all().order_by(sort_key)

    return render(request, "task_list.html", {"tasks": tasks})
