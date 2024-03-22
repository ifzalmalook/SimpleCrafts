from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (CreateView, ListView, DeleteView, UpdateView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Project
from .forms import ProjectForm
from django.urls import path, reverse_lazy
from django.utils.text import slugify
from django.views import generic, View

# Create your views here.



def home(request):
    return render(request, 'home.html')


class Projects(ListView):
    """
    List of Projects
    """
    queryset = Project.objects.all()
    template_name = 'projects/projects_list.html'
    model = Project   
    paginate_by = 6

   
    def get_queryset(self, **kwargs):
        search = self.request.GET.get("query")
        if search:
            projects = self.model.objects.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(category__name__icontains=search)  # search relating to a foreign key
            )
            return projects
        else:
            return Project.objects.all() 

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
    
@login_required
def full_project(request, slug):
    """
    View full project details
    """
    
    queryset = Project.objects.filter(slug=slug)
    project = get_object_or_404(queryset, slug=slug)
    has_liked = False

    if request.user.is_authenticated:
        user=request.user

        if project.likes.filter(id=user.id).exists():
            has_liked = True

    
   
    if request.method == 'POST':

        if request.user.is_authenticated:
            user=request.user

        if project.likes.filter(id=user.id).exists():
            project.likes.remove(user)
            has_liked=False
        
        else:
            project.likes.add(user)
            has_liked=True
    
    # Pass the project object to the template context
    return render(
        request,
        "projects/full_project.html",
        {"project": project,
        "has_liked":has_liked}  # Use the correct variable name here
    )

class DeleteProject(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('projects')

    def test_func(self):
        return self.request.user == self.get_object().author

    #add success message
    def form_valid(self, form):
        # If the form is valid, display a success message
        messages.success(self.request, 'The project has been removed!')
        return super().form_valid(form)

class EditProject(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'projects/edit_project.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('projects')

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author

    def get_context_data(self, **kwargs):
        context = super(EditProject, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.get_object())
        return context


    def form_valid(self, form):
        messages.success(self.request, 'Your project has been updated!')
        return super().form_valid(form)
