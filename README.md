Dojo Madness Task
=============

#### to run app:

1. The setting assumes that there is no mongodb or rabbitmq installed on the machine, if no please stop both of the services                
2. open a new terminal and run `docker-compose build && docker-compose up -d`
3. Client side can be reached through [Here](http://localhost:8888)
4. To send msg please do as follow:
    1. open a new terminal in the same directory and run `virtualenv --distribute --no-site-packages ./venv`
    2. run `source ./venv/bin/activate`
    3. run `pip install -r requirements.pip`
    4. run `python send.py`
    5. check the client side
----

#### to connect to the db:

1. open a new terminal and run `mongo`
2. run `use task_db`
3. run `show collections`
       
