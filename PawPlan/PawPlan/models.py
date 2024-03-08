class Address(models.Model):
    #fields(street 1, city, state, postal code, country)
    street1 = models.TextField(max_length=30)
    street2 = models.TextField(max_length=30, null=True)
    city = models.TextField(max_length=30)
    state = models.TextField(max_length=30)
    postal = models.TextField(max_length=20)
    country = models.TextField(max_length=10)


class Person(models.Model):
    name = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Worker(Person):
    MANAGER = "MA"
    REGULAR = "RE"

    ROLE_CHOICES = {
        MANAGER: "Manager",
        REGULAR: "Regular"
    }

    username = models.CharField(max_length=100)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    hireDate = models.DateField()


class Adopter(Person):
    canAdopt = models.BooleanField()
    

class Volunteer(Person):
    startDate = models.DateField()


class Shelter(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    worker = models.ManyToManyField(Worker)


class Animal(models.Model):
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    INTAKE_CHOICES = ['']
    species = models.CharField(max_length=30)
    breed = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=30)
    intake_type = models.CharField(max_length=30)
    image = models.ImageField()
    age = models.IntegerField(null=True)
    intake_date = models.DateTimeField()
    description = models.TextField()
    notes = models.CharField(max_length=100)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)
    isFixed = models.BooleanField()
    vaccinations = models.ManyToManyField('Vaccine', blank=True)
    readyToAdopt = models.BooleanField()
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)

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
    assignee = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True)
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


class Comment(models.Model):
    # Foreign keys
    task = models.ForeignKey(Task, null = True, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, null = True, on_delete=models.CASCADE)

    # Fields
    text = models.TextField()
    timeStamp = models.TimeField()

