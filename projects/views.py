from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project
from .forms import ProjectForm
from django.urls import path, reverse_lazy

# Create your views here.

def home(request):
    return render(request, 'home.html')

class AddProject(LoginRequiredMixin, CreateView):
    """
    View for adding craft projects
    """
    template_name = 'projects/add_project.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('projects')

    def form_valid(self, form):
        form.instance.author = self.request.user

        form.instance.slug = slugify(form.instance.title)
        messages.success(self.request, "Your project has been added!")
        return super(AddProject, self).form_valid(form)