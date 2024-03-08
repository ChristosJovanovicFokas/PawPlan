from django.db import models

class Shelter(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    worker = models.ManytoManyField(worker)
