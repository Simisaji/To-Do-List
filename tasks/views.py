from django.shortcuts import render, redirect
from .models import Task
import os
from django.conf import settings


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
