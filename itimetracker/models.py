from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime


class Category(models.Model):
  name = models.CharField(max_length=255, default='')
  code = models.PositiveIntegerField(null=True, unique=True)

  def __str__(self):
    return self.name

class Task(models.Model):
  name = models.CharField(max_length=255, default='', unique=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
  code = models.PositiveIntegerField(null=True, unique=True)

  def __str__(self):
    return self.name

class Role(models.Model):
  name = models.CharField(max_length=255, unique=True, default='')

  def __str__(self):
    return self.name

class Client(models.Model):
  name = models.CharField(max_length=255, unique=True, default='')

  def __str__(self):
    return self.name

class Project(models.Model):
  name = models.CharField(max_length=255, default='')
  code = models.CharField(max_length=255, unique=True, null=True)
  client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
  type = models.CharField(max_length=255, default='')
  start_date = models.DateField()
  open = models.BooleanField(default=True)

  def __str__(self):
    return self.name

class ProjectTask(models.Model):
  project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
  task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  delete_date = models.DateField(null=True)
  start_date = models.DateField(null=True)

  class Meta:
    unique_together = ('project', 'task', 'user')

  def __str__(self):
    return "%s: %s, %s" % (self.user.username, self.project.name, self.task.name)

class Time(models.Model):
  duration = models.DecimalField(max_digits=5, decimal_places=2, default=0)
  date = models.DateField()
  project_task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE, null=True)

  class Meta:
    unique_together = ('date', 'project_task',)

  def __str__(self):
    return "%s: %s" % (str(self.date), str(self.duration))

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    role = models.ForeignKey(Role, null=True)


