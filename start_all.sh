#!/bin/bash

# Start Redis
echo "Starting Redis..."
redis-server &

# Start Celery Worker
echo "Starting Celery Worker..."
celery -A Nexo worker -l info &

# (Optional) Start Celery Beat
# echo "Starting Celery Beat..."
# celery -A Nexo beat -l info &

# Start Django server
echo "Starting Django Server..."
python manage.py runserver
