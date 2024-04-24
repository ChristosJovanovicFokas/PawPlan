from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(source="due_date")

    class Meta:
        model = Task
        fields = ["title", "start"]
