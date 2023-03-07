# flight-test-task
Test task 

To start project

 sh build.sh
 
 sh run.sh
 
 or 
 
 docker-compose build
 
 docker-compose up
 
 python manage.py populate_db 
 
A channel must have at least
one content or one subchannel.

!!!seems like a contradiction

If a channel has no contents, it does not affect the ratings of its parent since its value is
undefined.
