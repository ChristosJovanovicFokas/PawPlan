from django.db import models


class Comment(models.Model):
    # Foreign keys
    task = models.ForeignKey(Task, null = True, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, null = True, on_delete=models.CASCADE)

    # Fields
    text = models.TextField()
    timeStamp = models.TimeField()