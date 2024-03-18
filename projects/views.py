from django.shortcuts import render
from django.views.generic import CreateView
from .models import Project
from django.urls import path, reverse_lazy

# Create your views here.

def home(request):
    return render(request, 'home.html')

class AddProject(CreateView):
    """
    View for adding craft projects
    """
    template_name = 'projects/add_project.html'
    model = Project
   
    success_url = reverse_lazy('projects')

    def form_valid(self, form):
        form.instance.author = self.request.user