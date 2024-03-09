from . import models as m
from django.contrib import admin


model_list = [
    m.Address,
    m.Worker,
    m.Adopter,
    m.Volunteer,
    m.Shelter,
    m.Dog,
    m.Cat,
    m.Turtle,
    m.Task,
    m.AnimalTask,
    m.AnimalComment,
    m.TaskComment,
]

for model in model_list:
    admin.site.register(model)
