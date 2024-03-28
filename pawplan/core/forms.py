from django import forms
from .models import Task


class AddTaskForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "completion_datetime", "assignee"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }
