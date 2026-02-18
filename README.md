# Twitter Clone (Django)

A Twitter clone built with **Python Django**, **HTML/CSS/JavaScript**, and **PostgreSQL**.

## Features
- User registration & login
- Post tweets (280 char limit)
- Like/unlike tweets
- Delete your own tweets
- Dark Twitter-like UI
- Responsive design

## Tech Stack
- **Backend**: Python Django 4.2
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL (AWS RDS)
- **Server**: Gunicorn + Nginx
- **Deployment**: AWS EC2 (Ubuntu)

## Deploy to EC2

```bash
ssh -i your-key.pem ubuntu@ec2-50-16-18-165.compute-1.amazonaws.com
curl -O https://raw.githubusercontent.com/albertcyriac04-lgtm/twitter-clone-django/main/deploy.sh
chmod +x deploy.sh
bash deploy.sh
```

## Local Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
