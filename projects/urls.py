from django.urls import path
from . import views


urlpatterns = [
    path('', views.AddProject.as_view(), name='add_project'),
    path('projects/', views.Projects.as_view(), name='projects'),
    path('<slug:slug>/', views.full_project, name='full_project'),
]
