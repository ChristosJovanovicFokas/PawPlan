class Animal(models.Model):
    SEX_CHOICES = [('M', 'Make'), ('F', 'Female')]
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
    notes = models.charField(max_length=100)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)
    isFixed = models.BooleanField()
    vaccinations = models.ManyToManyField('Vaccine', blank=True)
    readyToAdopt = models.BooleanField()
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
