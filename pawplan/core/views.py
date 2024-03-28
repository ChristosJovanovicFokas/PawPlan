from django.shortcuts import render
from .models import Animal, Task, AnimalTask

# Create your views here.


def animal_list(request):
    animal = Animal.objects.all()[:10]

    return render(request, "animals.html", {"animals": animal})


def worker_dash(request):
    tasks = Task.objects.all()
    animals = Animal.objects.all()
    return render(
        request,
        "worker_dashboard.html",
        {
            "tasks": tasks,
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
    filter_value = request.POST.get("filter")
    if filter_value == "completed":
        tasks = Task.objects.filter(completion_datetime__isnull=False)
    elif filter_value == "incomplete":
        tasks = Task.objects.filter(completion_datetime__isnull=True)
    else:
        tasks = Task.objects.all()

    # Assuming you have a 'tasks/task_list.html' template to render just the task list part
    return render(request, "tasks/task_list.html", {"tasks": tasks})


def sort_tasks(request):
    """
    A POST request to this view should contain a 'sort' parameter with a value of 'title',
    'due_date', or 'creation_datetime'. This view will return a list of tasks sorted by the
    specified field. Again, see worker_dashboard.html for an idea of how to structure the form
    that will send the POST request.
    """
    sort_value = request.POST.get("sort")

    # Define a default sort in case of unexpected sort values
    sort_key = "title"
    if sort_value in ["due_date", "creation_datetime"]:
        sort_key = sort_value

    tasks = Task.objects.all().order_by(sort_key)

    # Assuming you have a 'tasks/task_list.html' template to render just the task list part
    return render(request, "tasks/task_list.html", {"tasks": tasks})
