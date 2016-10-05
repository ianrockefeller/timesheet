from django import forms
from django.forms import ModelForm, ModelChoiceField

from .models import Task, ProjectTask, Category, Project


class CodeChoiceField(ModelChoiceField):

  def label_from_instance(self, obj):
    return "%s - %s" % (obj.code, obj.name)

class ProjectTaskForm(ModelForm):
  class Meta:
    model = ProjectTask
    fields = ['project', 'task']
    field_classes = {
      'project': CodeChoiceField,
      'task': CodeChoiceField
    }

  def __init__(self, *args, **kwargs):
    category = kwargs.pop('category', None)
    super(ProjectTaskForm, self).__init__(*args, **kwargs)

    self.fields['project'].queryset = Project.objects.filter(open=True)

    if category:
      self.fields['task'].queryset = Task.objects.filter(category=category).order_by('code')
    else:
      self.fields['task'].queryset = Task.objects.order_by('code')

class CategoryForm(forms.Form):
  category = CodeChoiceField(queryset=Category.objects.order_by('code'))


