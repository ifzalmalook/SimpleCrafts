from django.db import models
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField
from cloudinary.models import CloudinaryField


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Project(models.Model):
    author = models.ForeignKey(User, related_name='project_author',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=255, unique=True, null=False)
    description = models.CharField(max_length=600, blank=False, null=False)
    materials = RichTextField(max_length=10000, blank=False, null=False)
    steps = RichTextField(max_length=10000, blank=False, null=False)
    image = CloudinaryField('image', default='placeholder')
    published_on = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, null=False,
                                 blank=False, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, default=None, blank=True,
                                   related_name='project_post')

    class Meta:
        ordering = ['-published_on']

    def __string__(self):
        return str(self.title)
