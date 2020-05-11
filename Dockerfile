# pull official base image
FROM python:3.8.2-buster

# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install setuptools
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /code/