FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY django_frontend /app/frontend
COPY webshop /app/webshop

WORKDIR /app/frontend

RUN python setup.py sdist

WORKDIR /app/frontend/dist

RUN pip install $(ls  | head -n1)

WORKDIR /app/webshop

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate
