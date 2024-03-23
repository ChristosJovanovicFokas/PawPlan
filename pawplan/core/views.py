from django.shortcuts import render
from .models import Animal, Shelter

# Create your views here.

def animal_list(request):
    animal = Animal.objects.all()[:10]

    sexOptions = list(Animal.objects.order_by().values_list('sex', flat=True).distinct())
    colorOptions = list(Animal.objects.order_by().values_list('color', flat=True).distinct())
    locationOptions = list(Shelter.objects.order_by().values_list('name', flat=True).distinct())

    return render(request, "animals.html", {
        'animals' : animal,
        'sexOptions' : sexOptions,
        'colorOptions' : colorOptions,
        'locationOptions' : locationOptions
    })