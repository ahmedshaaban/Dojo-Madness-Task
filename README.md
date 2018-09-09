Tornado-Rabbitmq
=============

* consume messages (content type "application/json") from [RabbitMQ](https://www.rabbitmq.com/) and store them in [MongoDB](https://www.mongodb.com/)
* provide websocket endpoint that publishes incoming messages to websocket clients _as they arrive_ from RabbitMQ
* the routing key format is `{collection}.{_id}` denoting MongoDB collection and document `_id` eg. a message with routing key `foo.bar` should be inserted in collection "foo" with document \_id "bar"

#### to run app:

1. The setting assumes that there is no mongodb or rabbitmq installed on the machine, if no please stop both of the services                
2. open a new terminal and run `docker-compose build && docker-compose up`
3. Client side can be reached through [Here](http://localhost:8888)
4. To send msg please do as follow:
    1. open a new terminal in the same directory and run `virtualenv --distribute --no-site-packages ./venv`
    2. run `source ./venv/bin/activate`
    3. run `pip install -r requirements.pip`
    4. run `python send.py` (please not if you Interrupt the python send.py command the rabbitmq client session get closed according to the test file you sent earlier it deleted the exchange)
    5. check the client side 
----

#### to connect to the db:

1. open a new terminal and run `mongo`
2. run `use task_db`
3. run `show collections`
       
