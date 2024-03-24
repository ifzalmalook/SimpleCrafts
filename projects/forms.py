from django import forms
from djrichtextfield.widgets import RichTextWidget
from .models import Project


class ProjectForm(forms.ModelForm):
    materials = forms.CharField(widget=RichTextWidget())
    steps = forms.CharField(widget=RichTextWidget())

    class Meta:
        model = Project
        fields = ['title', 'description', 'materials',
                  'steps', 'image', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
