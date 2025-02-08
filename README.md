This project demonstrates deploying a Django + MySQL + JWT authentication web application using Docker on AWS EC2.


### Tech Stack
- Backend: Django (DRF)
- Database: MySQL
- Authentication: JWT (JSON Web Token)
- Containerization: Docker, Docker Compose
- Cloud: AWS EC2

/chat
    │── docker-compose.yml
    │── Dockerfile
    │── requirements.txt
    │── app/  # Django project folder
    │   ├── urls.py
    │   ├── settings.py
    │   ├── ...
    │── main/ 
    │   ├── admin.py
    │   ├── app.py
    │   ├── ...
    │── .env.example
    │── README.md
    │── manage.py 
