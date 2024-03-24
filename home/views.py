from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth import logout
from projects.models import Project
from django.db.models import Count

# Create your views here.


class Home(ListView):
    template_name = 'home/home.html'
    model = Project

    # Display most liked projects on home page
    def get_queryset(self):
        return (Project.objects
                .annotate(num_likes=Count('likes'))
                .order_by('-num_likes')[:3])
