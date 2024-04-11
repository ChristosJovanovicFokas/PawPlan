from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import (
    Animal,
    Task,
    Worker,
    Shelter,
    Person,
    Address,
    Adopter,
    AnimalComment,
    TaskComment,
    Volunteer,
)
from .forms import TaskForm, AdoptionForm, AddTaskForm, CommentForm
from django.core.paginator import Paginator
import datetime

# Create your views here.


def animal_list(request):

    sexOptions = list(
        Animal.objects.order_by().values_list("sex", flat=True).distinct()
    )
    colorOptions = list(
        Animal.objects.order_by().values_list("color", flat=True).distinct()
    )
    locationOptions = list(
        Shelter.objects.order_by().values_list("name", flat=True).distinct()
    )

    return render(
        request,
        "animal_list.html",
        {
            "sexOptions": sexOptions,
            "colorOptions": colorOptions,
            "locationOptions": locationOptions,
        },
    )


def animals(request):

    if request.method == "GET":
        params = dict(request.GET)
        print(request.GET)
        query = {}
        for param in params:
            if param == "location":
                query.update({"shelter__name__in": params.get(param)})
            if param == "color":
                query.update({"color__in": params.get(param)})
            if param == "sex":
                query.update({"sex__in": params.get(param)})

        p = Paginator(Animal.objects.filter(**query), 2)
        page = request.GET.get("page")
        animal = p.get_page(page)

        # animal = Animal.objects.filter(**query)

        return render(request, "partials/animals.html", {"animals": animal})


def animal(request, pet_id):
    animal = Animal.objects.get(pk=pet_id)

    adoptionForm = AdoptionForm()

    return render(
        request, "animal.html", {"animal": animal, "adoptionForm": adoptionForm}
    )


def worker_dash(request):
    tasks = Task.objects.all().prefetch_related("taskcomment_set")
    animals = Animal.objects.all()
    workers = Worker.objects.all()

    return render(
        request,
        "worker_dashboard.html",
        {
            "tasks": tasks,
            "animals": animals,
            "workers": workers,
        },
    )


def home(request):

    animals = Animal.objects.order_by("?")[:3]

    return render(request, "home.html", {"animals": animals})


def adoption(request, pet_id):
    if request.method == "POST":
        form = AdoptionForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["name"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            address_one = form.cleaned_data["address_one"]
            address_two = form.cleaned_data["address_two"]
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"]
            postal = form.cleaned_data["postal"]
            country = form.cleaned_data["country"]

            # check if address is already in database. if not, insert into database.
            if not Address.objects.filter(
                street1=address_one,
                street2=address_two,
                city=city,
                state=state,
                postal=postal,
                country=country,
            ).exists():

                address = Address.objects.create(
                    street1=address_one,
                    street2=address_two,
                    city=city,
                    state=state,
                    postal=postal,
                    country=country,
                )
                address.save()
                print("Address added to database")

            # check if person is already in database. if not, insert into database
            if not Person.objects.filter(email=email).exists():

                address = Address.objects.get(
                    street1=address_one,
                    street2=address_two,
                    city=city,
                    state=state,
                    postal=postal,
                    country=country,
                )

                print(address)

                adopter = Adopter.objects.create(
                    name=full_name,
                    phone_number=phone_number,
                    email=email,
                    address=address,
                    can_adopt=True,
                )
                adopter.save()
                print("Person added to database.")

            person = Person.objects.get(email=email)

    return HttpResponse(f"person id: {person.pk}, pet id: {pet_id}")


def about_view(request):
    return render(request, "about.html")


def adapt(request):
    return render(request, "adopt.html")


def login(request):

    return render(request, "login.html", {})


def filter_tasks(request):
    """
    A POST request to this view should contain a 'filter' parameter with a value of 'completed',
    'incomplete', or 'all'. This view will return a list of tasks based on the filter value.
    Additional filtering logic can be added as needed. See worker_dashboard.html for an idea of
    how to structure the form that will send the POST request.
    """
    if request.method != "POST":
        pass

    completion_status = request.POST.get("completion_status", "").lower()
    assignee = request.POST.get("assignee")
    animal = request.POST.get("animal")
    print(f"Comp: {completion_status}, Ass: {assignee}, An: {animal}")

    filter_params = {}

    if completion_status == "completed":
        filter_params["completion_datetime__isnull"] = False
    elif completion_status == "incomplete":
        filter_params["completion_datetime__isnull"] = True

    if assignee:
        filter_params["assignee"] = assignee

    if animal:
        filter_params["animal"] = animal

    tasks = Task.objects.filter(**filter_params)

    return render(request, "task_list.html", {"tasks": tasks})


def sort_tasks(request):
    """
    A POST request to this view should contain a 'sort' parameter with a value of 'title',
    'due_date', or 'creation_datetime'. This view will return a list of tasks sorted by the
    specified field. Again, see worker_dashboard.html for an idea of how to structure the form
    that will send the POST request.
    """
    sort_value = request.POST.get("sort")

    # default sort in case of unexpected sort values
    sort_key = "title"
    if sort_value in ["due_date", "creation_datetime"]:
        sort_key = sort_value

    tasks = Task.objects.all().order_by(sort_key)

    return render(request, "task_list.html", {"tasks": tasks})


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("worker_dash")  # Redirect to the tasks list
    else:
        form = TaskForm(instance=task)
    return render(request, "edit_task.html", {"form": form})


def add_task(request):
    if request.method == "POST":
        form = AddTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("worker_dash")  # Redirect to the tasks list
    else:
        form = AddTaskForm()
    return render(request, "add_task.html", {"form": form})


def add_comment(request):
    if request.method == "POST":
        comment_text = request.POST.get("comment")

        animal_id = request.POST.get("animal_id")
        animal_comment = AnimalComment(animal_id=animal_id, comment=comment_text)
        animal_comment.save()

        task_id = request.POST.get("task_id")
        task_comment = TaskComment(task_id=task_id, comment=comment_text)
        task_comment.save()
        return redirect("success_page")
    else:
        form = CommentForm()
    return render(request, "comment.html", {"form": form})


def volunteer_form(request):
    shelters = Shelter.objects.all()
    if request.method == "POST":
        form = AdoptionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            address_one = form.cleaned_data["address_one"]
            address_two = form.cleaned_data.get("address_two", "")
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"]
            postal = form.cleaned_data["postal"]
            country = form.cleaned_data["country"]
            shelter_id = request.POST.get("shelter")

            address = Address.objects.create(
                street1=address_one,
                street2=address_two,
                city=city,
                state=state,
                postal=postal,
                country=country,
            )

            shelter = Shelter.objects.get(pk=shelter_id)
            volunteer = Volunteer.objects.create(
                name=name,
                phone_number=phone_number,
                email=email,
                address=address,
                start_date=datetime.date.today(),
                shelter=shelter,
            )

            return redirect("home")
    else:
        form = AdoptionForm()

    return render(request, "volunteer_form.html", {"form": form, "shelters": shelters})


@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("worker_dash")  # Redirect to the tasks list
