FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt ./requirments.txt

RUN pip install --upgrade pip
RUN pip install -r requirments.txt

COPY / .

