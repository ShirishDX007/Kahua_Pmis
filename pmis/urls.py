from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('client/', views.client_list, name='client_list'),
    path('client/<int:pk>/', views.client_detail, name='client_detail'),
    path('projects/', views.project_list, name='project_list'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/create/', views.project_create, name='project_create'),
    path('project/<int:pk>/update/', views.project_update, name='project_update'),
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('task/', views.task_list, name='task_list'),
    path('project/<int:project_id>/tasks/', views.task_list, name='task_list'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/<int:task_id>/update/', views.task_update, name='task_update'),
    path('task/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('upload_tasks_csv/', views.upload_tasks_csv, name='upload_tasks_csv'),


]