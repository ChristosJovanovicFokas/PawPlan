from django.shortcuts import render
from .models import Animal, Shelter
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