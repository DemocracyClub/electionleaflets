FROM python:2.7

WORKDIR /app

RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y python-gdal && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists

COPY requirements.txt /app/
COPY requirements/* /app/requirements/

RUN pip install -r /app/requirements.txt

ENV PORT=3000

COPY ./ /app/

RUN SECRET_KEY=None python manage.py collectstatic --noinput

CMD gunicorn electionleaflets.wsgi --log-file -
