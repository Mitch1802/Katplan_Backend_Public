# Katplan_Backend

Test Repo for Setup a Docker Image

E-3ZcIYquF


set -e
apt-get update
apt-get upgrade
apt-get install -y python3-dev python3-venv sqlite python3-pip supervisor nginx git
rm -r /usr/local/apps/katplan
mkdir -p /usr/local/apps/katplan
git clone https://github.com/Mitch1802/Katplan_Backend_Public.git /usr/local/apps/katplan
mkdir -p /usr/local/apps/katplan/env
python3 -m venv /usr/local/apps/katplan/env
/usr/local/apps/katplan/env/bin/pip install -r /usr/local/apps/katplan/requirements.txt
/usr/local/apps/katplan/env/bin/pip install uwsgi==2.0.18
cd /usr/local/apps/katplan/src
/usr/local/apps/katplan/env/bin/python manage.py wait_for_db
/usr/local/apps/katplan/env/bin/python manage.py makemirgrations
/usr/local/apps/katplan/env/bin/python manage.py migrate
/usr/local/apps/katplan/env/bin/python manage.py collectstatic --noinput
cp /usr/local/apps/katplan/deploy/supervisor_katplan.conf /etc/supervisor/conf.d/katplan.conf
supervisorctl reread
supervisorctl update
supervisorctl restart katplan
systemctl restart supervisor.service
cp /usr/local/apps/katplan/deploy_new/nginx_katplan.conf /etc/nginx/sites-available/katplan.conf
sudo rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/katplan.conf /etc/nginx/sites-enabled/katplan.conf
systemctl restart nginx.service
cd /usr/local/apps/katplan
