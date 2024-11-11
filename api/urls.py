from django.urls import path, include
from .views import ClientList, ClientDetail, ProjectList, ProjectDetail, TaskList, TaskDetail, TaskCreate, upload_tasks_csv
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin




urlpatterns = [
    
    path('clients/', ClientList.as_view()),
    path('clients/<int:pk>/', ClientDetail.as_view()),
    path('projects/', ProjectList.as_view()),
    path('projects/<int:pk>/', ProjectDetail.as_view()),
    path('tasks/', TaskList.as_view()),
    path('api_task/create/', TaskCreate.as_view(), name='api_task_create'),
    path('tasks/<int:pk>/', TaskDetail.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]