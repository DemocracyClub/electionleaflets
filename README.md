# ElectionLeaflets

[![Coverage Status](https://coveralls.io/repos/DemocracyClub/electionleaflets/badge.svg?branch=master)](https://coveralls.io/r/DemocracyClub/electionleaflets?branch=django_1_7)
[![CI](https://circleci.com/gh/DemocracyClub/electionleaflets.svg?style=shield)](https://app.circleci.com/pipelines/github/DemocracyClub/electionleaflets)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Welcome

This is a port to Django of the PHP election leaflets application which can be found at https://code.google.com/archive/p/theelectionleafletproject/.

In order to speed up this port, we are running the first version using the original database structure. We'll tidy up areas of the database as necessary as new functionality is added. This shouldn't make a difference to new developers if you're starting from scratch.

### Getting started

You'll need some basic requirements installed on your machine, probably through your package manager:

- Python 3.12.x
- Node.js 18+
- PostgreSQL
- PostGIS
- Redis
- Yarn

This should do the trick on macOS or Linux with Homebrew:

```shell
brew install python node postgresql postgis redis yarn pipenv
```

1. Launch a shell with pipenv
```shell
pipenv shell
```

2. Settings and database
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

3. Install frontend dependencies
```
yarn install && bower install
```

4. Run gulp in another tab for development. This will watch for changes and recompile assets automatically. You'll need [gulp-cli](https://www.npmjs.com/package/gulp-cli) 
```
gulp
```

5. Run django
```
python manage.py runserver
```

6. Visit the site at http://127.0.0.1:8000/

7. See our [guidelines for contributing](CONTRIBUTING.md)

### Deploying

The app is deployed to AWS using the [Serverless
Framework](https://serverless.com/). This manages resources in AWS Lambda and
AWS API Gateway.

The app is deployed through CircleCI. The staging deployment is triggered by temporarily adding the current branch to context in the sam-deploy job. The production deployment is triggered by merging to master.