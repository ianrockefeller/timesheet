from django import forms

class ExportProjectForm(forms.Form):
  start_date = forms.DateField()
  end_date = forms.DateField()
