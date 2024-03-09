from django.db import models
from polymorphic.models import PolymorphicModel
from django.utils import timezone
import datetime


class Address(models.Model):
    # fields(street 1, city, state, postal code, country)
    street1 = models.TextField(max_length=30)
    street2 = models.TextField(max_length=30, null=True)
    city = models.TextField(max_length=30)
    state = models.TextField(max_length=30)
    postal = models.TextField(max_length=20)
    country = models.TextField(max_length=10)


class Shelter(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Person(PolymorphicModel):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Worker(Person):
    MANAGER = "MA"
    REGULAR = "RE"
    VET = "VT"

    ROLE_CHOICES = {MANAGER: "Manager", REGULAR: "Regular", VET: "Veterenarian"}

    username = models.CharField(max_length=100)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    hire_date = models.DateField()
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)


class Adopter(Person):
    can_adopt = models.BooleanField()


class Volunteer(Person):
    start_date = models.DateField()
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)


class Animal(PolymorphicModel):
    MALE = "M"
    FEMALE = "F"
    SEX_CHOICES = {MALE: "Male", FEMALE: "Female"}

    CAPTURED = "C"
    SURRENDERED = "S"
    INTAKE_CHOICES = {
        CAPTURED: "Captured in wild",
        SURRENDERED: "Surrendered by previous owner",
    }

    AUTOMATIC_TASKS = []

    name = models.CharField(max_length=100)
    color = models.CharField(max_length=30)
    intake_type = models.CharField(max_length=1, choices=INTAKE_CHOICES, blank=True)
    intake_date = models.DateTimeField(default=timezone.now())
    image = models.ImageField(null=True)
    age = models.IntegerField(null=True)
    description = models.TextField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)
    ready_to_adopt = models.BooleanField()
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)

    @property
    def animal_type(self):
        """Returns the class name as a string."""
        return self.__class__.__name__

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            for task_outline in self.AUTOMATIC_TASKS:
                automatic_task = AnimalTask.objects.create(
                    title=task_outline["title"],
                    description=task_outline["description"],
                    shelter=self.shelter,
                    required_role=task_outline["required_role"],
                    animal=self,
                )
                automatic_task.save()


class Dog(Animal):
    AUTOMATIC_TASKS = [
        {
            "title": "Wash and Groom",
            "description": "Give the dog a bath, shave any matted fur, and trim claws.",
            "required_role": "NA",
        },
        {
            "title": "Spay/Neuter",
            "description": "Spay or neuter the dog, depending on sex.",
            "required_role": "VT",
        },
        {
            "title": "Health Check",
            "description": "Administer the disease panel to check for possible diseases the dog may have.",
            "required_role": "VT",
        },
        {
            "title": "Vaccination",
            "description": "Give required vaccines to dog (Rabies, Distemper, Parvovirus, Hepatitus)",
            "required_role": "VT",
        },
        {
            "title": "Heartworm Prevention",
            "description": "Feed medication for prevention/treatment of Heartworm.",
            "required_role": "RE",
        },
        {
            "title": "Deworming Medication",
            "description": "Feed dewormer to dog.",
            "required_role": "RE",
        },
        {
            "title": "Microchip",
            "description": "Check for previous microchip and attach one if necessary.",
            "required_role": "VT",
        },
    ]

    is_fixed = models.BooleanField()
    breed = models.CharField(max_length=30, blank=True)


class Cat(Animal):
    AUTOMATIC_TASKS = [
        {
            "title": "Wash and Groom",
            "description": "Give the cat a bath, shave any matted fur, and trim claws.",
            "required_role": "NA",
        },
        {
            "title": "Spay/Neuter",
            "description": "Spay or neuter the cat, depending on sex.",
            "required_role": "VT",
        },
        {
            "title": "Health Check",
            "description": "Administer the disease panel to check for possible diseases the cat may have.",
            "required_role": "VT",
        },
        {
            "title": "Vaccination",
            "description": "Give required vaccines to cat (Rabies, Distemper, FVR, Calicivirus)",
            "required_role": "VT",
        },
        {
            "title": "Deworming Medication",
            "description": "Feed dewormer to cat.",
            "required_role": "RE",
        },
        {
            "title": "Microchip",
            "description": "Check for previous microchip and attach one if necessary.",
            "required_role": "VT",
        },
    ]

    is_fixed = models.BooleanField()
    breed = models.CharField(max_length=30, blank=True)


class Turtle(Animal):
    AUTOMATIC_TASKS = [
        {
            "title": "Wash",
            "description": "Clean the turtle.",
            "required_role": "NA",
        },
        {
            "title": "Health Check",
            "description": "Administer the disease panel to check for possible diseases the turtle may have.",
            "required_role": "VT",
        },
    ]

    species = models.CharField(max_length=30)


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
    is_completed: A boolean representing whether the task is completed.
    """

    MANAGER = "MA"
    REGULAR = "RE"
    VET = "VT"
    ANY = "NA"

    REQUIRED_ROLE_CHOICES = {
        MANAGER: "Manager",
        REGULAR: "Regular",
        VET: "Veterenarian",
        ANY: "Any Role",
    }

    title = models.CharField(max_length=100)
    description = models.TextField()
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    assignee = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True)
    # If a due_date is not specified, it defaults to seven days from the creation time
    due_date = models.DateTimeField(default=timezone.now() + datetime.timedelta(days=7))
    completion_datetime = models.DateTimeField(null=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    required_role = models.CharField(max_length=2, choices=REQUIRED_ROLE_CHOICES)

    @property
    def is_completed(self):
        return self.completion_datetime is not None


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


class Comment(models.Model):
    # Foreign keys
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    # Fields
    text = models.TextField()
    time_stamp = models.DateTimeField(default=timezone.now())


class TaskComment(Comment):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class AnimalComment(Comment):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
