from django.shortcuts import render, redirect, get_object_or_404
from . models import Client, Project, Task
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ClientForm, ProjectForm, TaskForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import JsonResponse
import csv
from datetime import datetime 


def index(request):
      
    return render(request, 'index.html')


#client view

@login_required
def client_list(request):
    clients = Client.objects.all()
    context = {'clients': clients}
    return render(request, 'client_list.html', context)

@login_required
def client_detail(request, pk):
    client = Client.objects.get(pk=pk)
    projects = Project.objects.filter(client=client)
    context = {'client': client, 'projects': projects}
    return render(request, 'client_detail.html', context)
#project view
@login_required(login_url='kahua_users:login')
def project_list(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'project_list.html', context)

@login_required
def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    tasks = Task.objects.filter(project=project)
    context = {'project': project, 'tasks': tasks, 'client': project.client}
    return render(request, 'project_detail.html', context)

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user.client
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    context = {'form': form}
    return render(request, 'project_create.html', context) 

#project update

@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            client = getattr(project, 'client', None)
            form.save()
            return JsonResponse({'success': True, 'message': 'Project updated successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
            
    else:
        form = ProjectForm(instance=project)
    context = {'form': form , 'project': project}
    return render(request, 'project_update.html', context)

@login_required
def project_delete(request, pk):
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    context = {'project': project}
    return render(request, 'project_delete.html', context)


#task view

@login_required
def task_list(request, project_id=None):
    if project_id:
        tasks = Task.objects.filter(project_id=project_id)
        project =get_object_or_404(Project, pk=project_id)
        context = {'tasks': tasks, 'project': project}
    else:
        tasks = Task.objects.all()
        projects = Project.objects.prefetch_related('tasks').all()
   
        context = {'projects': projects}
    return render(request, 'task_list.html', context)

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    context = {'task': task}
    url = reverse('task_detail', args=[task.pk])
    
    return render(request, 'task_detail.html', context)

@login_required
@permission_required('pmis.can_assign_task', raise_exception=True)
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if request.user.has_perm('pmis.can_assign_task_to_client', task.assigned_to):
                task.save()
                return redirect('task_list', project_id=task.project.id)
            else:
                messages.error(redirect, "You do not have permissions to assign tasks.")
                return redirect('task_list')
    else:
        form = TaskForm()
    context = {'form': form}
    return render(request, 'task_create.html', context)

@login_required
@permission_required('pmis.can_assign_task', raise_exception=True)
def task_update(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    project = task.project
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            if request.user.has_perm('pmis.can_assign_task_to_client', task.assigned_to):
                form.save()
                return JsonResponse({'success': True, 'message': 'Task updated successfully.', 'project_id': task.project.id})
                #return redirect('task_list', project_id=task.project.id)
            else:
                return JsonResponse({'success': False, 'message': 'You do not have permissions to assign tasks.'})
                # messages.error(request, "you dont have permissions to assign tasks.")
                # return redirect('task_update', task_id=task.pk)
    else:
        form = TaskForm(instance=task)
    context = {'form': form, 'task': task, 'project': project}
    return render(request, 'task_update.html', context)

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
     
    if request.method == 'POST':
        project_id = task.project.id
        task.delete()
        return redirect('task_list', project_id=project_id)
    context = {'task': task}
    return render(request, 'task_delete.html', context)

@login_required
def upload_tasks_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file.')
            return redirect('task_list')

        # Decode file to handle different file encodings
        file_data = csv_file.read().decode('utf-8').splitlines()

        reader = csv.reader(file_data)
        # Skip the header row if your CSV file has one
        next(reader)

        for row in reader:
            # Assuming CSV columns are: task_name, status, start_date, end_date, assigned_to_email, project_id
            try:
                task_name, date_created,status, project_id, assigned_to_id, task_start_date, task_end_date = row

                # Fetch the Project object
                project = Project.objects.get(id=project_id)
                assigned_to_user = User.objects.get(email=assigned_to_email)
                
                date_created = datetime.strptime(date_created, "%Y-%m-%d").date()
                task_start_date = datetime.strptime(task_start_date, "%Y-%m-%d").date()
                task_end_date = datetime.strptime(task_end_date, "%Y-%m-%d").date()

                # Create the Task object
                Task.objects.create(

                    name=task_name,
                    date_created=date_created,
                    status=status,
                    project=project,
                    assigned_to_id=assigned_to_id,
                    start_date=task_start_date,
                    end_date=task_end_date,
                    
                    
                )
            except Exception as e:
                messages.error(request, f"Error processing row {row}: {e}")
                continue

        messages.success(request, "Tasks have been uploaded successfully.")
        return redirect('task_list')
    else:
        return redirect('task_list')



