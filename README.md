# To-Do-List
Created a to-do-list app using Python django

1. Project Setup
Step 1: Open your terminal or CMD and run the following:

# Create project folder
mkdir todo_project
cd todo_project

# Create virtual environment
python -m venv env

# Activate virtual environment
# For Windows:
env\Scripts\activate


# Install Django
pip install django

# Start Django project
django-admin startproject todo .

# Create app
python manage.py startapp tasks
🧩 2. Register the App
In todo/settings.py, add 'tasks' to INSTALLED_APPS:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks',  # ← Add this
]
🧱 3. Create the Model
In tasks/models.py:

from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

Then run:
python manage.py makemigrations
python manage.py migrate

🖥️ 4. Admin Setup (Optional for debugging)
In tasks/admin.py:

from django.contrib import admin
from .models import Task

admin.site.register(Task)

Create a superuser:

python manage.py createsuperuser
📄 5. Views & URLs
In tasks/views.py:

from django.shortcuts import render, redirect
from .models import Task

def index(request):
    tasks = Task.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title)
        return redirect('index')
    return render(request, 'tasks/index.html', {'tasks': tasks})

def delete_task(request, task_id):
    Task.objects.get(id=task_id).delete()
    return redirect('index')

def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = True
    task.save()
    return redirect('index')
    
🧭 6. URL Configuration
In todo/urls.py:

from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
]

🎨 7. HTML Template
Create a folder templates/tasks/ and add index.html:

<!DOCTYPE html>
<html>
<head>
    <title>To-Do List</title>
</head>
<body>
    <h1>My To-Do List</h1>
    <form method="POST">
        {% csrf_token %}
        <input type="text" name="title" placeholder="Enter task">
        <button type="submit">Add</button>
    </form>
    <ul>
        {% for task in tasks %}
            <li>
                {% if task.completed %}
                    <strike>{{ task.title }}</strike>
                {% else %}
                    {{ task.title }}
                    <a href="{% url 'complete_task' task.id %}">✅</a>
                {% endif %}
                <a href="{% url 'delete_task' task.id %}">❌</a>
            </li>
        {% endfor %}
    </ul>
</body>
</html>

In tasks/views.py, add:
import os
from django.conf import settings

And make sure settings.py has:

import os

TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        ...
    },
]

🚀 8. Run the Server

python manage.py runserver
Go to: http://127.0.0.1:8000/
