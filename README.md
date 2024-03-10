# SeniorProject - Group

## Saving and Viewing the Dummy Data
1. Activate your virtual environment (if you don't have one, create one using `python -m venv venv` and activate it using `source venv/bin/activate`)
2. Install the dependencies using `pip install -r requirements.txt`
3. Perform the migrations using `python manage.py makemigrations` and `python manage.py migrate`
4. create a superuser using `python manage.py createsuperuser` (just follow the prompts and remember what you entered)
5. Create the dummy objects using `python manage.py shell < fixture.py`
6. Run the server using `python manage.py runserver`
7. Objects should be available at `http://localhost:8000/admin` (use the superuser credentials to login)
