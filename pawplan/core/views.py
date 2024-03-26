from django.shortcuts import render
from .models import Animal, Shelter

# Create your views here.

def animal_list(request):

    sexOptions = list(Animal.objects.order_by().values_list('sex', flat=True).distinct())
    colorOptions = list(Animal.objects.order_by().values_list('color', flat=True).distinct())
    locationOptions = list(Shelter.objects.order_by().values_list('name', flat=True).distinct())

    if request.method == "GET":
    
        params = dict(request.GET)
        query = {}
        for param in params:
            if param == 'location':
                query.update({'shelter__name__in' : params.get(param)})
            if param == 'color':
                query.update({'color__in' : params.get(param)})
            if param == 'sex':
                query.update({'sex__in' : params.get(param)})
        print(query)
        animal = Animal.objects.filter(**query)

        return render(request, "animals.html", {
            'animals' : animal,
            'sexOptions' : sexOptions,
            'colorOptions' : colorOptions,
            'locationOptions' : locationOptions
        })

def animal(request, pet_id):
    animal = Animal.objects.get(pk=pet_id)

    return render(request, "animal.html", {
        'animal' : animal
    })