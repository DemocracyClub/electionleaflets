# Electionleaflets

[![Stories in Ready](https://badge.waffle.io/democracyclub/electionleaflets.png?label=ready&title=Ready)](https://waffle.io/democracyclub/electionleaflets)
[![Build Status](https://travis-ci.org/DemocracyClub/electionleaflets.svg)](https://travis-ci.org/DemocracyClub/electionleaflets)
[![Coverage Status](https://coveralls.io/repos/DemocracyClub/electionleaflets/badge.svg?branch=master)](https://coveralls.io/r/DemocracyClub/electionleaflets?branch=django_1_7)

### Welcome

This is a port to Django of the PHP election leaflets application which can be found at http://code.google.com/p/theelectionleafletproject/.

In order to speed up this port, we are running the first version using the original database structure. We'll tidy up areas of the database as necessary as new functionality is added. This shouldn't make a difference to new developers if you're starting from scratch.

### Getting started

You'll need some basic requirements installed on your machine, probably through your package manager:

- Python 2.7.x
- Node.JS 7+
- PostgreSQL
- PostGIS
- Redis
- Yarn

This should do the trick on macOS with Homebrew:

```shell
deactivate ; brew install python node postgresql postgis redis yarn
```

1. Create python virtual environment
```shell
virtualenv .venv --no-site-packages
. .venv/bin/activate
```

2. Install python requirements

For development:
```shell
pip install -r requirements/dev.txt
```

For production:
```shell
pip install -r requirements/production.txt
```

3. Settings and database
```shell
createdb electionleaflets
createuser electionleaflets
psql -c 'ALTER ROLE electionleaflets WITH SUPERUSER' # Needed to activate PostGIS
cp electionleaflets/settings/local.py.example electionleaflets/settings/local.py # Optional: add a TheyWorkForYou API key here
python manage.py migrate
python manage.py createcachetable
python manage.py constituencies_load_constituencies
mkdir -p electionleaflets/media/uploads/{thumbnail,small,medium,large}
python manage.py createsuperuser # Create a user to login to /admin with
```

4. Install frontend dependencies
```
yarn install && bower install
```

5. Run gulp in another tab for development. This will watch for changes and recompile assets automatically
```
gulp
```

6. Run django
```
python manage.py runserver
```

7. Visit the site at http://127.0.0.1:8000/

8. See our [guidelines for contributing](CONTRIBUTING.md)
