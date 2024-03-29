from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Animal, Task, Worker, Shelter
from .forms import TaskForm
from django.core.paginator import Paginator

# Create your views here.

def animal_list(request):

    sexOptions = list(Animal.objects.order_by().values_list('sex', flat=True).distinct())
    colorOptions = list(Animal.objects.order_by().values_list('color', flat=True).distinct())
    locationOptions = list(Shelter.objects.order_by().values_list('name', flat=True).distinct())

    return render(request, "animal_list.html", {
        'sexOptions' : sexOptions,
        'colorOptions' : colorOptions,
        'locationOptions' : locationOptions
    })

def animals(request):

    if request.method == "GET":
        params = dict(request.GET)
        print(request.GET)
        query = {}
        for param in params:
            if param == 'location':
                query.update({'shelter__name__in' : params.get(param)})
            if param == 'color':
                query.update({'color__in' : params.get(param)})
            if param == 'sex':
                query.update({'sex__in' : params.get(param)})

        p = Paginator(Animal.objects.filter(**query), 2)
        page = request.GET.get('page')
        animal = p.get_page(page)

        # animal = Animal.objects.filter(**query)

        return render(request, 'partials/animals.html', {
            'animals' : animal
        })

def animal(request, pet_id):
    animal = Animal.objects.get(pk=pet_id)

    return render(request, "animal.html", {
        'animal' : animal
    })

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


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks_list")  # Redirect to the tasks list
    else:
        form = TaskForm(instance=task)
    return render(request, "edit_task.html", {"form": form})


@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("tasks_list")  # Redirect to the tasks list
