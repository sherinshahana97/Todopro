# Generated by Django 5.0.6 on 2024-10-24 13:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project1', '0002_remove_project_todos_todo_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project1.project'),
        ),
    ]
