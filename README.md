# SeniorProject - Group

## Saving and Viewing the Dummy Data
1. Activate your virtual environment (if you don't have one, create one using `python -m venv venv` and activate it using `source venv/bin/activate`)
2. Install the dependencies using `pip install -r requirements.txt`
3. Run `python -m pip install --upgrade pip setuptools` to fix "ModuleNotFoundError: No module named 'pkg_resources'"
4. Perform the migrations using `python manage.py makemigrations` and `python manage.py migrate`
5. create a superuser using `python manage.py createsuperuser` (just follow the prompts and remember what you entered)
6. Create the dummy objects using `python manage.py shell < fixture.py`
7. Run the server using `python manage.py runserver`
8. Objects should be available at `http://localhost:8000/admin` (use the superuser credentials to login)
