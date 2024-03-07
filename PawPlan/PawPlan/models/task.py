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
import csv
from faker import Faker
from datetime import datetime, timedelta
from random import choice


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


if __name__ == "__main__":

    fake = Faker()
    tasks_data = []

    # get the dummy data from csv
    this_dir = Path(__file__).parent
    dummy_fp = this_dir.parent / "dummy_data" / "dummy_tasks.csv"
    with open("dummy_tasks.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            tasks_data.append(row)

    # Create dummy tasks
    for data in tasks_data:
        task_type = data[0]
        title = data[1]
        description = data[2]
        due_date = datetime.now() + timedelta(
            days=int(data[fake.random_int(min=3, max=30)])
        )
        required_role = choice(["MA", "RE", "VO"])

        if task_type == "Task":
            task = Task.objects.create(
                title=title,
                description=description,
                due_date=due_date,
                required_role=required_role,
            )
        elif task_type == "AnimalTask":
            animal = Animal.objects.get(id=int(data[4]))
            task = AnimalTask.objects.create(
                title=title,
                description=description,
                due_date=due_date,
                required_role=required_role,
                animal=animal,
            )
        elif task_type == "MicrochippingTask":
            animal = Animal.objects.get(id=int(data[4]))
            chip_ID = fake.random_int(min=1000000000, max=9999999999)
            task = MicrochippingTask.objects.create(
                title=title,
                description=description,
                due_date=due_date,
                required_role=required_role,
                animal=animal,
                chip_ID=chip_ID,
            )
        elif task_type == "VaccinationTask":
            animal = Animal.objects.get(id=int(data[4]))
            vaccine_type = fake.word()
            protocol = fake.text()
            task = VaccinationTask.objects.create(
                title=title,
                description=description,
                due_date=due_date,
                required_role=required_role,
                animal=animal,
                vaccine_type=vaccine_type,
                protocol=protocol,
            )
        elif task_type == "HealthCheckTask":
            animal = Animal.objects.get(id=int(data[4]))
            health_check_notes = fake.text()
            results = fake.text()
            task = HealthCheckTask.objects.create(
                title=title,
                description=description,
                due_date=due_date,
                required_role=required_role,
                animal=animal,
                health_check_notes=health_check_notes,
                results=results,
            )
