# JIKAN CONTROL

## Introduction
Jikan Control is an application, developed in python, developed for students, by students. Its main purpose is to help each user manage their most precious belonging, time. It is often the case that students have little sense of time, like how long does it take to study for an exam and actually get a good grade or where can I find the time to study for so many homeworks and exams, or even know if you have enough free time to complete whatever task you need to complete. These sort of problems is what we aim on solving. We want students to learn the rewards of organizing your time and what can be accomplish with it.


### What is this?

Jikan Control is an application that can be treated as an intelligent calendar for students. A calendar is a tool used for organizing days and hours into events and activities. Usually, a student's performance in a course is measured with several exams, which can be considered events. This application is able to predict the score that a student will receive in any given exam and how much time they need to dedicate to studying to get a specified grade. This will be done with the help of a machine learning model created using a dataset which contains correlations between study time and exam performance. Eventually the application will use the information obtained from the users to enlarge the dataset and improve the Machine Learning model’s accuracy. The application will analyze the amount of time that a student has dedicated (or will dedicate) to studying for an exam and predict the result that the student will receive. 

In addition to predicting the student’s performance, this application can identify how much time a student has to spend studying in order to get a specific exam result. This is important when determining the optimal amount of time that should be dedicated to multiple exams that are taken in a similar time period. 

Jikan Control’s main user interface feature is the calendar. In this part, the user can view and add events. An event can be an exam, study time period, reminder, and any other regular activity such as the period in which an academic course is being given. These events can also have one or multiple notes attached to them.

Finally, this is a web application, so it can be accessed from any desktop, laptop, and mobile device with a supported web browser. It will be hosted on the Heroku platform. 

## Application Features

* View Calendar with monthly and weekly view
* Create various types of events with options
* Add notes to events
* Add Exam events
* Add Courses
* Create/change/alter profile
* Forgot password
* Search exam/events/notes/courses
* Push notifications
* Exam score/studytime predictions
* Mobile friendly


## How to Run on Docker

### Prerequisites

#### Windows/Mac
Your system needs [Docker Desktop](https://www.docker.com/products/docker-desktop) installed

#### Linux
You need both [Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) installed

### Commands
Once you have the prerequisites go to the root of the project and run the command below to run and build the docker (on Linux you might need run all commands with superuser privilege).

```
sudo docker-compose up -d --build
```

When the above finishes you will need to run the next two commands **only the first time**
```
sudo docker-compose exec web python manage.py migrate --noinput
```
```
sudo docker-compose exec db psql -f defaultVals.sql -f get_events_in_range.sql -f generate_study_events.sql -f update_study_events.sql --username=postgres --dbname=jikan_control_db
```
Now the project should show up in your browser on [localhost:8000](http://localhost:8000/).

To stop the application you can look up running containers with:
```
docker container ps
```
And stop them with:
```
docker container stop [CONTAINER]
```

The next time you want to run the application you don't need to build it, therefore you can simply run:
```
docker-compose up
```
*You can add the* ```-d``` *tag if you wish to detach the container from the terminal and run it in the background*

## Extra Information

### How to use - Manual

Click [here](https://google.com) to go to the Use Manual.

### Project Report

Click [here](https://google.com) to go to the Project Report.

### Icons Provided By

* [Font Awesome](https://fontawesome.com/)

## Contributors

* [Axviel A. Benítez Dorta](https://github.com/axviel)
* [Fernando Guzmán Fernández](https://github.com/FernandoLGuzman)
* [Angel Rivera Camacho](https://github.com/anrarivera)


