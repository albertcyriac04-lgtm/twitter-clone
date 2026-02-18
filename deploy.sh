#!/bin/bash
# Twitter Clone (Django) - EC2 Deployment Script
# Run this on your Ubuntu EC2 instance

set -e

echo "=== 1. Updating system ==="
sudo apt update && sudo apt upgrade -y

echo "=== 2. Installing Python & Nginx ==="
sudo apt install -y python3 python3-pip python3-venv nginx git

echo "=== 3. Cloning repository ==="
cd ~
git clone https://github.com/albertcyriac04-lgtm/twitter-clone-django.git
cd twitter-clone-django

echo "=== 4. Creating virtual environment ==="
python3 -m venv venv
source venv/bin/activate

echo "=== 5. Installing dependencies ==="
pip install -r requirements.txt

echo "=== 6. Setting environment variables ==="
export DB_NAME=twitterclone
export DB_USER=postgres
export DB_PASSWORD=12345678
export DB_HOST=database-1.c4piwg0ew68j.us-east-1.rds.amazonaws.com
export DB_PORT=5432
export DEBUG=False

echo "=== 7. Running migrations ==="
python manage.py migrate

echo "=== 8. Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== 9. Creating Gunicorn systemd service ==="
sudo tee /etc/systemd/system/twitterclone.service > /dev/null << 'SERVICE'
[Unit]
Description=Twitter Clone Django App
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/twitter-clone-django
Environment="DB_NAME=twitterclone"
Environment="DB_USER=postgres"
Environment="DB_PASSWORD=12345678"
Environment="DB_HOST=database-1.c4piwg0ew68j.us-east-1.rds.amazonaws.com"
Environment="DB_PORT=5432"
Environment="DEBUG=False"
ExecStart=/home/ubuntu/twitter-clone-django/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 twitterclone.wsgi:application

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl daemon-reload
sudo systemctl start twitterclone
sudo systemctl enable twitterclone

echo "=== 10. Configuring Nginx ==="
sudo tee /etc/nginx/sites-available/twitterclone > /dev/null << 'NGINX'
server {
    listen 80;
    server_name ec2-50-16-18-165.compute-1.amazonaws.com;

    location /static/ {
        alias /home/ubuntu/twitter-clone-django/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINX

sudo ln -sf /etc/nginx/sites-available/twitterclone /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

echo ""
echo "=== DEPLOYMENT COMPLETE ==="
echo "Your app is live at: http://ec2-50-16-18-165.compute-1.amazonaws.com"
