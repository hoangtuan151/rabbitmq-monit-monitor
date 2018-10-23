# Rabbitmq Monit Monitor
Monitor RabbitMQ total queue's messages with Monit

# Monit config script as follow:
```
check program _check_message_in_queue_ with path _/path/to/check_rabbit_queue_msg.py_
    if status != 0 then alert
```
