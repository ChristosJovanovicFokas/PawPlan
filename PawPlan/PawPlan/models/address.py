from django.db import models 

class address(models.Model):
    #foreign keys()
    person = models.OneToOneField(Person, null = True, on_delete=models.CASCADE)
    shelter = models.OneToOneField(Shelter, null=True, on_delete=models.CASCADE)
    
    #fields(street 1, city, state, postal code, country)
    street = models.TextField(max_length=30)
    city = models.TextField(max_length=30)
    state = models.TextField(max_length=30)
    postal = models.TextField(max_length=20)
    country = models.TextField(max_length=10)
