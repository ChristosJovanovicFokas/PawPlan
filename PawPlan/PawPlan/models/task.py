"""
The Task class is a Django model that represents tasks that can be created and assigned to
instances of the Person class. It is a concrete class, meaning it can be used on its own.
It also has multiple child classes that inherit from it, representing common specific tasks
that need special attributes.
"""

from django.db import models
from .person import Person
from .comment import Comment
from .animal import Animal
from .shelter import Shelter


class Task(models.Model):
    """
    Concrete base implementation of a task.

    Attributes:
    title: A string representing the title of the task.
    description: A string representing the description of the task.
    shelter: A foreign key to the Shelter class representing the shelter the task is associated with.
    comments: A foreign key to the Comment class representing the comments on the task.
    assignee: A foreign key to the Person class representing the person the task is assigned to.
    due_date: A datetime representing the due date of the task.
    completion_datetime: A datetime representing the date and time the task was completed (null
        if not completed).
    creation_datetime: A datetime representing the date and time the task was created.
    required_role: A string representing the role required to complete the task.
    """

    title = models.CharField(max_length=100)
    description = models.TextField()
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE)
    assignee = models.ForeignKey(Person, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    # There is no boolean field for whether a task is completed or not, but the presence
    # of a completed_datetime field can be used to determine if a task is completed or not.
    completion_datetime = models.DateTimeField(null=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    required_role = models.CharField(max_length=2)


class AnimalTask(Task):
    """
    A subclass of the Task class representing a task associated with an animal. Can be further
    subclassed to represent specific tasks (see below).

    Additional Attributes:
    animal: A foreign key to the Animal class representing the animal associated with the task.
    """

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)


class MicrochippingTask(AnimalTask):
    """
    A subclass of the AnimalTask class representing a task to microchip an animal.

    Additional Attributes:
    chip_ID: A string representing the microchip number of the animal.
    """

    chip_ID = models.CharField(max_length=100)


class VaccinationTask(AnimalTask):
    """
    A subclass of the AnimalTask class representing a task to vaccinate an animal.

    Additional Attributes:
    vaccine: A string representing the vaccine to be administered to the animal.
    """

    vaccine_type = models.CharField(max_length=100)
    protocol = models.TextField()


class HealthCheckTask(AnimalTask):
    """
    A subclass of the AnimalTask class representing a task to perform a health check on an animal.

    Additional Attributes:
    health_check_notes: A string representing the notes from the health check.
    """

    health_check_notes = models.TextField()
    results = models.TextField()
