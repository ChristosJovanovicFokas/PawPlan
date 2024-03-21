from django.shortcuts import render
from .models import Task, AnimalTask


# Create your views here.
def worker_dash(request):
    tasks = Task.objects.all()
    return render(
        request,
        "worker_dashboard.html",
        {
            "tasks": tasks,
        },
    )

def about_view(request):
    return render(request, 'about.html')
