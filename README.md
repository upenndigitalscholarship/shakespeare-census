# Shakespeare Census

A database of early editions of plays attributed to Shakespeare.

License: MIT

## Basic Commands

### Setting Up Your Users

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create a **superuser account**, use this command:

```bash
$ python manage.py createsuperuser
```

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type Checks

Running type checks with mypy:

```bash
$ mypy shakespeare_census
```

### Test Coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

```bash
$ coverage run -m pytest
$ coverage html
$ open htmlcov/index.html
```

#### Running Tests with pytest

```bash
$ pytest
```

### Live Reloading and Sass CSS Compilation

Moved to [Live reloading and SASS compilation](http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html).

## Deployment

The following details how to deploy this application.

