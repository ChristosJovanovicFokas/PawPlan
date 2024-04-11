from django.db import models
from polymorphic.models import PolymorphicModel
from django.utils import timezone
import datetime


class Address(models.Model):
    """
    The Address class represents a physical address. It is used as a foreign key in the Shelter and
    Person classes.

    Attributes:
    street1: A string representing the first line of the street address.
    street2: A string representing the second line of the street address (optional).
    city: A string representing the city of the address.
    state: A string representing the state of the address (max length is ).
    postal: A string representing the postal code of the address.
    country: A string representing the country of the address.
    """

    street1 = models.TextField(max_length=30)
    street2 = models.TextField(max_length=30, null=True)
    city = models.TextField(max_length=30)
    state = models.TextField(max_length=2)
    postal = models.TextField(max_length=20)
    country = models.TextField(max_length=10)

    def __str__(self):
        return f"{self.street1}, {self.city}, {self.state} {self.postal}"


class Shelter(models.Model):
    """
    The Shelter class represents an animal shelter. It is used as a foreign key in the Worker,
    Volunteer, Animal, and Task classes.

    Attributes:
    name: A string representing the name of the shelter.
    phone_number: A string representing the phone number of the shelter.
    email_address: A string representing the email address of the shelter.
    address: A foreign key to the Address class representing the address of the shelter.
    """

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Person(PolymorphicModel):
    """
    The Person class implements the PolyMorphicModel class and represents a person. This is a
    slight change that allows us to use the Person class as a foreign key in the Comment class
    without knowing if the Person is a Worker or Volunteer (polymorphism). It is referenced by
    Comment and Task objects.

    Attributes:
    name: A string representing the name of the person.
    phone_number: A string representing the phone number of the person.
    email: A string representing the email address of the person.
    address: A foreign key to the Address class representing the address of the person.
    """

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Worker(Person):
    """
    The Worker class represents a worker at an animal shelter. It is a subclass of the Person
    class.

    Additional Attributes:
    username: A string representing the username of the worker.
    role: A string representing the role of the worker (manager, regular, or veterinarian).
    hire_date: A date representing the date the worker was hired.
    shelter: A foreign key to the Shelter class representing the shelter the worker works at.
    """

    MANAGER = "MA"
    REGULAR = "RE"
    VET = "VT"

    ROLE_CHOICES = {MANAGER: "Manager", REGULAR: "Regular", VET: "Veterenarian"}

    username = models.CharField(max_length=100)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    hire_date = models.DateField()
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)


class Adopter(Person):
    """
    The Adopter class represents a person who is interested in adopting an animal from a shelter.

    Additional Attributes:
    can_adopt: A boolean representing whether the person is able to adopt an animal.
    """

    can_adopt = models.BooleanField()


class Volunteer(Person):
    """
    The Volunteer class represents a person who volunteers at an animal shelter. They do not
    require a username to log on, and they have fewer permissions than workers.

    Additional Attributes:
    start_date: A date representing the date the volunteer started working at the shelter.
    shelter: A foreign key to the Shelter class representing the shelter the volunteer works at.
    """

    start_date = models.DateField()
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)


class Animal(PolymorphicModel):
    """
    The Animal class is again a subclass of the PolyMorphicModel class. This allows us to use the
    Animal class as a foreign key in the Task class without knowing if the Animal is a Dog,
    Cat, or Turtle (polymorphism). It is referenced by the Task and AnimalComment classes.

    NOTE: The .save() method has been overridden to automatically create tasks for the animal when
    it is first saved. This base implementation has an empty list of AUTOMATIC_TASKS, but subclasses
    like Cat and Dog will override this attribute to include tasks specific to those animals. The
    overriden AUTOMATIC_TASKS attributes should be a list of dicts of the following form:

        {"title": "The task title", "description": "The task description", "required_role": "MA/VT/RE/NA"}

    Attributes:
    name: A string representing the name of the animal.
    color: A string representing the color of the animal.
    intake_type: A string representing the type of intake ("C" for captured or "S" for surrendered).
    intake_date: A date representing the date the animal was taken in by the shelter (defaults to now).
    image: An image representing the animal (optional).
    age: An integer representing the age of the animal (optional).
    description: A string representing the description of the animal.
    sex: A string reprensenting the sex of the animal ("M" or "F")
    ready_to_adopt: A boolean representing whether the animal is ready to be adopted.
    shelter: A foreign key to the Shelter class representing the shelter the animal is at.
    animal_type: A property that returns the class name as a string.
    """

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
    intake_date = models.DateTimeField(default=timezone.now)
    image = models.CharField(max_length=300)
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
                automatic_task = Task.objects.create(
                    title=task_outline["title"],
                    description=task_outline["description"],
                    shelter=self.shelter,
                    required_role=task_outline["required_role"],
                    animal=self,
                )
                automatic_task.save()

    def __str__(self):
        return self.name


class Dog(Animal):
    """
    The Dog class is a subclass of the Animal class and represents a dog. It overrides the
    AUTOMATIC_TASKS attribute to include tasks specific to dogs.

    Additional Attributes:
    is_fixed: A boolean representing whether the dog is spayed/neutered.
    breed: A string representing the breed of the dog.
    """

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
    """
    The Cat class is a subclass of the Animal class and represents a cat. It overrides the
    AUTOMATIC_TASKS attribute to include tasks specific to cats.

    Additional Attributes:
    is_fixed: A boolean representing whether the cat is spayed/neutered.
    breed: A string representing the breed of the cat.
    """

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
    """
    The Turtle class is a subclass of the Animal class and represents a turtle. It overrides the
    AUTOMATIC_TASKS attribute to include tasks specific to turtles.

    Additional Attributes:
    species: A string representing the species of the turtle.
    """

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
    assignee: A foreign key to the Person class representing the person the task is assigned to.
    due_date: A datetime representing the due date of the task.
    completion_datetime: A datetime representing the date and time the task was completed (null
        if not completed).
    creation_datetime: A datetime representing the date and time the task was created.
    required_role: A string representing the role required to complete the task.
    is_completed: A boolean representing whether the task is completed (uses @property wrapper to
        treat a method like an attribute).
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
    completion_datetime = models.DateTimeField(blank=True, null=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    required_role = models.CharField(max_length=2, choices=REQUIRED_ROLE_CHOICES)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, null=True)

    @property
    def is_completed(self):
        return self.completion_datetime not in (None, "")

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    The Comment class is an abstract base class that represents a comment. It is subclassed by the
    TaskComment and AnimalComment classes.

    Attributes:
    person: A foreign key to the Person class representing the person who made the comment.
    text: A string representing the text of the comment.
    time_stamp: A datetime representing the date and time the comment was made.
    """

    # Foreign keys
    person = models.ForeignKey(Person, null = True, on_delete=models.CASCADE)

    # Fields
    text = models.TextField()
    timeStamp = models.TimeField(default=timezone.now)


class TaskComment(Comment):
    """
    The TaskComment class is a subclass of the Comment class and represents a comment on a task.

    Additional Attributes:
    task: A foreign key to the Task class representing the task the comment is associated with.
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class AnimalComment(Comment):
    """
    The AnimalComment class is a subclass of the Comment class and represents a comment on an animal.

    Additional Attributes:
    animal: A foreign key to the Animal class representing the animal the comment is associated with.
    """

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
