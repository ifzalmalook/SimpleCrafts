# Generated by Django 4.2.11 on 2024-03-18 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-published_on']},
        ),
    ]
