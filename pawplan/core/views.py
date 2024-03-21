from django.shortcuts import render
from .models import Animal, Task, AnimalTask

# Create your views here.

def animal_list(request):
    animal = Animal.objects.all()[:10]

    return render(request, "animals.html", {
        'animals' : animal
    })


def worker_dash(request):
    tasks = Task.objects.all()
    return render(
        request,
        "worker_dashboard.html",
        {
            "tasks": tasks,
        },
    )

<<<<<<< HEAD
def home(request):
    
    return render(
        request, 
        "home.html",
        {}
    )
=======
def about_view(request):
    return render(request, 'about.html')
>>>>>>> 71c77bfc009366c915687dfdc03aa93353e7ba52
