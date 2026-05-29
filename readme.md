# High-Level Architecture
Build a RESTful backend using:
- Django
- Django REST Framework
- JWT Authentication
- Role-based permissions
- PostgreSQL (recommended)


# Functional Requirements
## Authentication
Users must:
- Login to access the API
- Receive JWT access/refresh tokens

Admin can:
- Create users
- Crate tasks for users

Authorized users can:
- Create tasks
- Read their own tasks
- Update their own tasks
- Delete their own tasks
- View tasks created by others

# Tech Stack
Layer                                   Technology
--------------------------------------------------
Backend                                 Django
API                                     Django REST Framework
Auth                                    SimpleJWT
DB                                      PostgreSQL
Permissions                             DRF Custom Permissions


# Project Strucure
task_managers/
|
|--  config /
|    |-- settings.py
|    |-- urls.py
|
|--  users /
|    |-- models.py
|    |-- serializers.py
|    |-- views.py
|    |-- permissions.py
|    |-- urls.py
|
|--  tasks /
|    |-- models.py
|    |-- serializers.py
|    |-- views.py
|    |-- permissions.py
|    |-- urls.py


# Permissions
## Rules
Action                  Admin               Normal User
--------------------------------------------------
Create users            ✅                  ❌
Create tasks            ✅                  ✅ 
View own tasks          ✅                  ✅ 
View others' tasks      ✅                  ✅ 
Update own tasks        ✅                  ✅ 
Update others' tasks    ✅                  ❌ 
Delete own tasks        ✅                  ✅ 
Delete others' tasks    ✅                  ❌


# API Endpoints
Method          Endpoint                Description
------------------------------------------------------
POST            /api/login              Login
POST            /api/token/refresh      Refresh token
GET             /api/tasks/             List tasks
POST            /api/tasks/             Create task
GET             /api/tasks/{id}/        Retreive task
PUT             /api/tasks/{id}/        Update task
DELETE          /api/tasks/{id}/        Delete task         


Method          Endpoint                Description
------------------------------------------------------
POST            /api/users/             Admin creates user
GET             /api/users/             List users
POST            /api/users/             Create user
GET             /api/users/{id}/        Retreive user
PUT             /api/users/{id}/        Update user
DELETE          /api/users/{id}/        Delete user      

# PYTHON ENVIRONMENT
sudo apt install python3 python3-pip python3-venv -y
pip freeze > requirements.txt
pip install -r requirements.txt

# POSTGRESQL

sudo apt update
sudo apt instal postgresql postgresql-contrib
sudo systemctl start postgresql

#Access PostgreSQL Shell
sudo - postgres psql
CREATE DATABASE database-name;
CRATE USER database-user WITH PASSWORD 'password';
ALTER USER database-user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE database-name to database-user;

# SETTINGS IN DJANGO
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'database-name',
        'USER': 'database-user',
    }
}
pip install psycopg2-binary
python manage.py makemigrations
python manage.py migrate


# Customize the serializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["is_admin"] = user.is_staff
        token["username"] = user.username

        return token
    
     def validate(self, attrs):
        data = super().validate(attrs)

        data["username"] = self.user.username
        data["is_admin"] = self.user.is_staff

        return data

# Include it in View

from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer