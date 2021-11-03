FROM python:3.9-alpine
LABEL AUTHOR="Litesh Garg" version='1.0'

ENV PYTHONNUMBUFFERED 1


COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D djangoUser
USER djangoUser
