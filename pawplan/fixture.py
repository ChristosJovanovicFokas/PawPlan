import datetime

import requests
import core.models as m
from django.utils import timezone


model_list = [
    m.TaskComment,
    m.AnimalComment,
    m.Task,
    m.Turtle,
    m.Cat,
    m.Dog,
    m.Volunteer,
    m.Adopter,
    m.Worker,
    m.Shelter,
    m.Address,
]


# Start with clean slate by deleting all existing objects
for model in model_list:
    model.objects.all().delete()


# Create new address objects
addresses = {
    "dr_baliga": ["1700 Rowan Blvd.", "Room 318", "Glassboro", "NJ", "08080", "US"],
    "steve_p": ["721 Broad St.", None, "Glassboro", "NJ", "08080", "US"],
    "steve_b": ["41 Penns Ave.", "Suite 7070", "Beverly", "CA", "90210", "US"],
    "ricky_k": ["1800 5th St.", None, "New York", "NY", "19945", "US"],
    "derek_p": ["999 South St.", "Apt. B7", "Philadelphia", "PA", "19977", "US"],
    "connor_h": ["15 Juniper Dr.", None, "Edison", "NJ", "08745", "US"],
    "christos_j": ["113 W 34th St.", "Suite 744", "Ocean City", "NJ", "08332", "US"],
    "shelter": ["1447 N Shelter Dr.", None, "Lawnside", "NJ", "08447", "US"],
}

for name, info in addresses.items():
    street1, street2, city, state, postal, country = (
        info[0],
        info[1],
        info[2],
        info[3],
        info[4],
        info[5],
    )
    addresses[name] = m.Address.objects.create(
        street1=street1,
        street2=street2,
        city=city,
        state=state,
        postal=postal,
        country=country,
    )
    addresses[name].save()


# create a shelter object
shelter = m.Shelter.objects.create(
    name="Furry Friends Animal Shelter",
    phone_number="800-123-456",
    email_address="info@furryfriends.com",
    address=addresses["shelter"],
)
shelter.save()


# create new person objects (worker, adopter, and volunteer)
dr_baliga = m.Adopter.objects.create(
    name="Dr. Baliga",
    phone_number="123-456-7899",
    email="drbaliga@gmail.com",
    address=addresses["dr_baliga"],
    can_adopt=True,
)
steve_p = m.Worker.objects.create(
    name="Stephen Piccolo",
    phone_number="123-456-7899",
    email="stevepic95@gmail.com",
    address=addresses["steve_p"],
    username="stevep95",
    password="password",
    role="RE",
    hire_date=timezone.now(),
    shelter=shelter,
)
steve_b = m.Worker.objects.create(
    name="Steven Beltran",
    phone_number="555-123-4567",
    email="steveb@email.com",
    address=addresses["steve_b"],
    username="steveb235",
    password="password",
    role="MA",
    hire_date=timezone.now(),
    shelter=shelter,
)
ricky_k = m.Worker.objects.create(
    name="Ricky Kramer",
    phone_number="777-123-4567",
    email="rickyk@email.com",
    address=addresses["ricky_k"],
    username="rickyk777",
    password="password",
    role="VT",
    hire_date=timezone.now(),
    shelter=shelter,
)
derek_p = m.Worker.objects.create(
    name="Derek Pruestel",
    phone_number="222-123-4567",
    email="derekp@email.com",
    address=addresses["derek_p"],
    username="derekp777",
    password="password",
    role="RE",
    hire_date=timezone.now(),
    shelter=shelter,
)
connor_h = m.Volunteer.objects.create(
    name="Connor Handley",
    phone_number="999-123-4567",
    email="connorh@email.com",
    address=addresses["connor_h"],
    start_date=timezone.now(),
    shelter=shelter,
)
christos_j = m.Volunteer.objects.create(
    name="Christos Jovanovic",
    phone_number="111-123-4567",
    email="christosj@email.com",
    address=addresses["christos_j"],
    start_date=timezone.now(),
    shelter=shelter,
)

for person in [dr_baliga, steve_p, steve_b, ricky_k, derek_p, connor_h, christos_j]:
    person.save()


# Create new animal objects (which will also automatically create Task objects for each)

def get_jpg():
    run = True
    while run:
        response = requests.get("https://random.dog/woof.json")
        img_info = dict(response.json())
        if img_info.get('url').split('.')[2] == 'jpg':
            return img_info
    
animal_list = []

img_info = get_jpg()

animal_list.append(
    m.Dog.objects.create(
        name="Bubba",
        color="black and brown",
        intake_type="S",
        age=3,
        description="A very large, very friendly dog. Loves cats and children.",
        sex="M",
        is_fixed=False,
        ready_to_adopt=False,
        shelter=shelter,
        breed="Rotweiler",
        image=img_info.get("url"),
    )
)

img_info = get_jpg()

animal_list.append(
    m.Cat.objects.create(
        name="Charlie",
        color="tuxedo",
        intake_type="C",
        age=5,
        description="A small, playful cat who loves people but doesn't like other cats.",
        sex="M",
        is_fixed=True,
        ready_to_adopt=True,
        shelter=shelter,
        breed="Tabby",
        image=img_info.get("url"),
    )
)

img_info = get_jpg()

animal_list.append(
    m.Cat.objects.create(
        name="Princess",
        color="orange",
        intake_type="C",
        age=2,
        description="A beautiful but mean cat who hates everyone. Patient owners required.",
        sex="F",
        is_fixed=True,
        ready_to_adopt=False,
        shelter=shelter,
        breed="Tabby",
        image=img_info.get("url"),
    )
)

img_info = get_jpg()

animal_list.append(
    m.Turtle.objects.create(
        name="Jennifer",
        color="yellow/green",
        intake_type="S",
        age=22,
        description="A large, healthy Red-eared Slider who requires a large habitat to thrive.",
        sex="F",
        ready_to_adopt=False,
        shelter=shelter,
        species="Red-eared Slider",
        image=img_info.get("url"),
    )
)

img_info = get_jpg()

animal_list.append(
    m.Dog.objects.create(
        name="Larry",
        color="Tricolor",
        intake_type="S",
        age=1,
        description="Affectionate, Friendly, Playful, Gentle, Athletic, Curious.",
        sex="M",
        is_fixed=False,
        ready_to_adopt=False,
        shelter=shelter,
        breed="Shepherd Mix",
        image=img_info.get("url"),
    )
)

img_info = get_jpg()

animal_list.append(
    m.Dog.objects.create(
        name="Gadget",
        color="White",
        intake_type="S",
        age=5,
        description="Very cuddly.",
        sex="M",
        is_fixed=False,
        ready_to_adopt=False,
        shelter=shelter,
        breed="Maltese",
        image=img_info.get("url"),
    )
)

img_info = get_jpg()

animal_list.append(
    m.Dog.objects.create(
        name="Mitra",
        color="Brindle",
        intake_type="S",
        age=4,
        description="Friendly, Affectionate, Loyal, Smart, Athletic.",
        sex="F",
        is_fixed=True,
        ready_to_adopt=True,
        shelter=shelter,
        breed="Terrier Mix",
        image=img_info.get("url"),
    )
)

img_info = get_jpg()

animal_list.append(
    m.Dog.objects.create(
        name="Rosie",
        color="Multi",
        intake_type="S",
        age=1,
        description="Sweet puppy looking for a home.",
        sex="F",
        is_fixed=True,
        ready_to_adopt=True,
        shelter=shelter,
        breed="Shepherd Mix",
        image=img_info.get("url"),
    )
)

img_info = get_jpg()

animal_list.append(
    m.Dog.objects.create(
        name="Hooch",
        color="Multi",
        intake_type="S",
        age=2,
        description="Very playfull.",
        sex="M",
        is_fixed=False,
        ready_to_adopt=False,
        shelter=shelter,
        breed="Terrier Mix",
        image=img_info.get("url"),
    )
)

img_info = get_jpg()

animal_list.append(
    m.Dog.objects.create(
        name="Ella",
        color="Cream",
        intake_type="S",
        age=6,
        description="Has accidents at times in the house.",
        sex="F",
        is_fixed=True,
        ready_to_adopt=True,
        shelter=shelter,
        breed="Maltese",
        image=img_info.get("url"),
    )
)

for animal in animal_list:
    animal.save()


# Create some new Task objects that are not associated with any animal
clean_toilets_task = m.Task.objects.create(
    title="Clean the Toilets",
    description="Don't miss any spots like last time",
    shelter=shelter,
    assignee=steve_p,
    required_role="NA",
)

post_jobs_task = m.Task.objects.create(
    title="Post Available Jobs Online",
    description="Use Indeed to post job listings for the roles 'Veteranarian' and 'Reegular Employee'",
    shelter=shelter,
    required_role="MA",
)

feed_cats_task = m.Task.objects.create(
    title="Feed the Cats",
    description="The cats are hungry. Hurry up.",
    shelter=shelter,
    required_role="RE",
)

for task in [clean_toilets_task, post_jobs_task, feed_cats_task]:
    task.save()


# Add some comments to the animals
bubba_comment1 = m.AnimalComment.objects.create(
    person=steve_b,
    text="Bubba bit me",
    animal=animal_list[0],
)

bubba_comment2 = m.AnimalComment.objects.create(
    person=ricky_k,
    text="No way",
    animal=animal_list[0],
)
jennifer_coment1 = m.AnimalComment.objects.create(
    person=derek_p,
    text="Who named this turtle Jennifer",
    animal=animal_list[3],
)

for comment in [bubba_comment1, bubba_comment2, jennifer_coment1]:
    comment.save()


# Add some comments to the tasks
clean_toilets_task_comment = m.TaskComment.objects.create(
    person=connor_h,
    text="Clean those toilets steve",
    task=clean_toilets_task,
)
feed_cats_task_comment = m.TaskComment.objects.create(
    person=christos_j,
    text="Be careful the cats are really mad",
    task=feed_cats_task,
)

for comment in [clean_toilets_task_comment, feed_cats_task_comment]:
    comment.save()
