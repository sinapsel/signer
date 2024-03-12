#!/bin/bash

if [[ "${1}" == "worker" ]]; then
  echo "celery Worker"
  celery -A main.celery worker --beat --loglevel=info --broker="${CELERY_BROKER_URL}" #--pidfile=/opt/signer/app/storage/celeryd.pid #--broker="${CELERY_BROKER_URL}"
elif [[ "${1}" == "flower" ]]; then
  echo "Celery Flower"
  celery -A main.celery flower --loglevel=info --broker="${CELERY_BROKER_URL}"
elif [[ "${1}" == "beat" ]]; then
echo "Celery Beat"
celery -A main.celery beat --loglevel=info --pidfile=/opt/signer/app/storage/celerybd.pid --broker="${CELERY_BROKER_URL}"
fi
