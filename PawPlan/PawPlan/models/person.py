from django.db import models

#

class Person(models.Model):
    name = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

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