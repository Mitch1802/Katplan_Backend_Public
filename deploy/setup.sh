#!/usr/bin/env bash

set -e

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/Mitch1802/Katplan_Backend_Public.git'

PROJECT_BASE_PATH='/usr/local/apps/katplan'

echo "Installing dependencies..."
apt-get update
apt-get install -y python3-dev python3-venv sqlite python3-pip supervisor git

# Create project directory
mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

# Create virtual environment
mkdir -p $PROJECT_BASE_PATH/env
python3 -m venv $PROJECT_BASE_PATH/env

# Install python packages
$PROJECT_BASE_PATH/env/bin/pip install -r $PROJECT_BASE_PATH/requirements.txt
$PROJECT_BASE_PATH/env/bin/pip install uwsgi==2.0.18

# Run migrations and collectstatic
cd $PROJECT_BASE_PATH/src
$PROJECT_BASE_PATH/env/bin/python manage.py wait_for_db
$PROJECT_BASE_PATH/env/bin/python manage.py makemirgrations
$PROJECT_BASE_PATH/env/bin/python manage.py migrate
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput

# Configure supervisor
cp $PROJECT_BASE_PATH/deploy/supervisor_katplan.conf /etc/supervisor/conf.d/katplan.conf
supervisorctl reread
supervisorctl update
supervisorctl restart katplan
systemctl restart supervisor.service

# Configure nginx
cp $PROJECT_BASE_PATH/deploy_new/nginx_katplan.conf /etc/nginx/sites-available/katplan.conf
sudo rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/katplan.conf /etc/nginx/sites-enabled/katplan.conf
systemctl restart nginx.service

# Wechsel in den App Ordner
cd $PROJECT_BASE_PATH

echo "DONE! :)"
