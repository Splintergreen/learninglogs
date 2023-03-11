#!/bin/bash
# exit if errors
set -e

echo "Deployment started ..."

source venv/bin/activate
echo "Virtual Env Activated !"

git pull origin master
echo "New changes copied to server !"

echo "Installing Dependencies..."
pip install -r requirements.txt --no-input

# echo "Serving Static Files..."
# cd /learninglogs and remember previous directory
pushd learninglogs
# python manage.py collectstatic --noinput

echo "Running Database migration"
python manage.py makemigrations
python manage.py migrate
# return to previous directory
popd

deactivate
echo "Virtual Env Deactivated !"

# kill and restart gunucorn process
systemctl status gunicorn |  sed -n 's/.*Main PID: \(.*\)$/\1/g p' | cut -f1 -d' ' | xargs kill -HUP

echo "Deployment Finished!"