### Task Description

* As a user, I want to register in the app with my name, email, and password.

* As a user, I want to log in with my e-mail and password.

* As a user, after logging in I would like to receive JWT token, that later I could use for authorization.

* As a user, I would like to download a list of available movies and basic information such as the name of the movie and its price.

* As a user, I would like to download a particular movie with information such as the name of the movie, its price, and its rating (scale from 1 to 10)

* As a user, I would like to have a possibility to purchase a movie ticket for my registered account

* As a user, I would like to have a possibility to download a list of my purchased tickets in the past

* As an administrator, I would like to have access to a build-in, simple Django administration panel where I can manage users, films, and tickets

### Tech Stack
I have used `python 3.9` and `sqlite` as database to keep everything simple for now.

### Steps to run the project
* `pip install -r requirements.txt`
* `python manage.py migrate`
* `python manage.py runserver`

### Admin
* Create a superuser to manage users, movies, tickets in django admin. Run `python manage.py createsuperuser` in terminal.
* Login to admin :  `http://127.0.0.1:8000/admin/`

### Show available api endpoints in the project
* Just run `python manage.py show_urls` in terminal.
### Testing
I have added `12 tests` to test all the specified features in task description.

* `python manage.py test --keepdb`
