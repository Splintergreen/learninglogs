#!/bin/bash
# exit if errors
set -e

echo "### Deployment started ..."

cd ~/coding/learninglogs/

source venv/bin/activate
echo "### Virtual Env Activated !"

git pull origin master
echo "### New changes copied to server !"

echo "### Installing Dependencies..."
pip install --upgrade pip
pip install -r requirements.txt --no-input

echo "Serving Static Files..."
# cd /learninglogs and remember previous directory
pushd learninglogs
python manage.py collectstatic --noinput

echo "Running Database migration"
python3 manage.py makemigrations
python3 manage.py migrate
echo "### Migrations complete"
# return to previous directory
popd

deactivate
echo "### Virtual Env Deactivated !"

# kill and restart gunucorn process
systemctl status gunicorn |  sed -n 's/.*Main PID: \(.*\)$/\1/g p' | cut -f1 -d' ' | xargs kill -HUP
echo "### Gunicorn restarted"

echo "### Deployment Finished! :rocket:"