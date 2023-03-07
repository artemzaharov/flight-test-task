How to Start and Use the Project
This guide will walk you through the steps to start and use the project on your local machine.

Prerequisites
Before you start, you'll need to make sure you have the following installed:

Docker
Python
Installation
Clone the repository to your local machine.

Navigate to the project directory in your terminal.

Run the following command to build the project:


$ docker-compose build 

Once the build process is complete, run the following command to start the project:

$ docker-compose up

Open new terminal with project

In project folder create venv

$ python3 -m venv env

Activate it

$ source env/bin/activate

Install requirements

(env)$ pip install -r requirements.txt

Run the following command to populate the database:

(env)$ python manage.py populate_db

Usage

http://localhost:80/api/channel           - all Tree

http://localhost:80/api/channel/<int:id>  - channel

http://localhost:80/api/content/<int:pk>   - content

Use the admininterface to interact with the project and add content and channels.

(env)$ python manage.py createsuperuser

Run the following command to generate a report:

(env)$ python manage.py report






