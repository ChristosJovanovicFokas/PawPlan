from django.shortcuts import render
from .models import Animal

# Create your views here.

def animal_list(request):
    animal = Animal.objects.all()[:10]

    return render(request, "animals.html", {
        'animals' : animal
    })