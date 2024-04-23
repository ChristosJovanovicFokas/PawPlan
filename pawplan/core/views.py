from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.urls import reverse
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
    TaskItem
)
from .forms import (
    TaskForm,
    AdoptionForm,
    AddTaskForm,
    CommentForm,
    AnimalForm,
    LoginForm,
)

from django.core.paginator import Paginator
from datetime import datetime

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

        p = Paginator(Animal.objects.filter(**query), 5)
        page = request.GET.get("page")
        animal = p.get_page(page)

        # animal = Animal.objects.filter(**query)

        return render(request, "partials/animals.html", {"animals": animal})


def animal(request, pet_id):
    animal = Animal.objects.get(pk=pet_id)

    adoptionForm = AdoptionForm()

    return render(
        request, "animal.html", {"animal": animal, "form": adoptionForm}
    )


def worker_dash(request):

    if "is_valid" not in request.session:
        request.session["is_valid"] = False

    if request.session.get("is_valid") == False:
        return redirect(login)

    tasks = Task.objects.all().prefetch_related("taskcomment_set")
    animals = Animal.objects.all().prefetch_related("animalcomment_set")
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


def add_animal(request):
    if request.method == "POST":
        form = AnimalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("animal_dashboard"))
    else:
        form = AnimalForm()

    return render(request, "add_animal.html", {"form": form})


def edit_animal(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    if request.method == "POST":
        form = AnimalForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            return redirect("animal_dashboard")
    else:
        form = AnimalForm(instance=animal)

    return render(request, "edit_animal.html", {"form": form, "animal": animal})


@require_POST
def delete_animal(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    animal.delete()
    return redirect("worker_dash")


def sort_animals(request):
    sort_by = request.POST.get("sort", "name")  # Default sort by name
    animals = Animal.objects.all().order_by(sort_by)
    return render(request, "dash_animal_list.html", {"animals": animals})

def display_all_comments(request):
    # Fetch all animal comments and task comments from the database
    animal_comments = AnimalComment.objects.all()
    task_comments = TaskComment.objects.all()
    
    # Render the HTML template and pass the comments as context variables
    return render(request, 'all_comments.html', {'animal_comments': animal_comments, 'task_comments': task_comments})


def filter_animals(request):
    sex = request.POST.get("sex")
    ready_to_adopt = request.POST.get("ready_to_adopt")

    animals = Animal.objects.all()

    if sex:
        animals = animals.filter(sex=sex)
    if ready_to_adopt:
        animals = animals.filter(ready_to_adopt=ready_to_adopt == "true")

    return render(request, "dash_animal_list.html", {"animals": animals})


def home(request):

    animals = Animal.objects.order_by("?")[:3]

    return render(request, "home.html", {"animals": animals})


def adoption(request, pet_id):
    if request.method == "POST":
        form = AdoptionForm(request.POST)
        if form.is_valid():
            print("valid")
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
                    can_adopt=False,
                )
                adopter.save()
                print("Person added to database.")

            animal = Animal.objects.get(id=pet_id)

            shelter = animal.shelter

            task = Task(title="Adoption",
                description=f"{full_name} is interested in adopting. Please contact them.",
                required_role="MA",
                shelter=shelter,
                animal=animal)
            task.save()

            task_item = TaskItem(item_number = 1, text="Contact client", is_complete=False, task=task)
            task_item.save()
            task_item = TaskItem(item_number = 2, text="Fill out paperwork", is_complete=False, task=task)
            task_item.save()
            task_item = TaskItem(item_number = 3, text="Interview client", is_complete=False, task=task)
            task_item.save()
            print("Saved task")

    return redirect(animal_list)


def about_view(request):
    return render(request, "about.html")


def adapt(request):
    return render(request, "adopt.html")


def login(request):

    loginForm = LoginForm()

    form = LoginForm(request.GET)
    if form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        worker = Worker.objects.filter(email=email, password=password).first()

        if worker:
            request.session["is_valid"] = True
            request.session["worker"] = worker.email
            if worker.role == 'MA':
                request.session["is_manager"] = True
            else:
                request.session["is_manager"] = False
            return redirect(worker_dash)
        else:
            return render(
                request, "login.html", {"loginForm": loginForm, "invalid": True}
            )

    return render(request, "login.html", {"loginForm": loginForm})

def logout(request):
    request.session.flush()

    return redirect(home)


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


def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
   
    task.completion_datetime = datetime.now()
    task.save()

    return redirect("worker_dash")

def add_task(request):
    if request.method == "POST":
        form = AddTaskForm(request.POST)
        if form.is_valid():
            task = form.save()

            item_text_list = list(request.POST.getlist('item'))
            item_text_list.insert(0, form.cleaned_data['task_item'])

            for i, item in enumerate(item_text_list):
                task_item = TaskItem.objects.create(item_number=i+1, text=item, is_complete=False, task=task)
                task_item.save()
            
            return redirect("worker_dash")  # Redirect to the tasks list
    else:
        form = AddTaskForm()
    return render(request, "add_task.html", {"form": form})


def release_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
   
    task.is_released = True
    task.save()

    return redirect("worker_dash")


def swap_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
   
    worker = Worker.objects.get(email=request.session.get("worker"))
    task.assignee = worker
    task.is_released = False
    task.save()

    return redirect("worker_dash")

@require_POST
def add_task_comment(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    worker = Worker.objects.filter(email=request.session['worker']).first()
    text = request.POST.get("text")
    comment = TaskComment(task=task, person=worker, text=text)
    comment.save()
    return redirect(worker_dash)


@require_POST
def add_animal_comment(request, task_id):
    animal = get_object_or_404(Animal, pk=task_id)
    worker = Worker.objects.filter(email=request.session['worker']).first()
    text = request.POST.get("text")
    comment = TaskComment(animal=animal, person=worker, text=text)
    comment.save()
    return redirect("worker_dash")


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

            shelter = Shelter.objects.get(pk=shelter_id)

            if not Person.objects.filter(email=email).exists():

                address = Address.objects.get(
                    street1=address_one,
                    street2=address_two,
                    city=city,
                    state=state,
                    postal=postal,
                    country=country,
                )

                volunteer = Volunteer.objects.create(
                    name=name,
                    phone_number=phone_number,
                    email=email,
                    address=address,
                    start_date=datetime.date.today(),
                    shelter=shelter,
                )
                volunteer.save()

            task = Task(title="Volunteer",
                        description=f"{name} is interested in being a volunteer. Please contact them.",
                        required_role="MA",
                        shelter=shelter)
            task.save()
            task_item = TaskItem(item_number = 1, text="contact volunteer", is_complete = False, task=task)
            task_item.save()
            print("Saved task")

            return redirect("home")
    else:
        form = AdoptionForm()

    return render(request, "volunteer_form.html", {"form": form, "shelters": shelters})


@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("worker_dash")  # Redirect to the tasks list

@require_POST
def complete_item(request, item_id):
    TaskItem.objects.filter(pk=item_id).update(is_complete=True)
    return redirect("worker_dash")


def task_items(request):
    task_id = request.GET.get('task_id')
    task_item_list = TaskItem.objects.filter(task=task_id)

    return render(request, "partials/task_item_list.html" ,{
        'task_items' : task_item_list
    })