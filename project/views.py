from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime

from .forms import ExportProjectForm
from itimetracker.actions import export_xlsx

def export_project(request):
  form = ExportProjectForm(auto_id="export_project_form")
  if request.GET.get("project_id"):
    if request.GET.get("start_date") or request.GET.get("end_date"):
      start_date = request.GET.get("start_date")
      end_date = request.GET.get("end_date")

      start = datetime.datetime.strptime(start_date, '%Y/%m/%d')
      end = datetime.datetime.strptime(end_date, '%Y/%m/%d')

      if start < end:
        project_id_list = request.GET.get("project_id").split(',')
        return export_xlsx(project_id_list,start,end)
      else:
        context = {
          'form': form,
          'project_id': request.GET.get('project_id'),
          'error': 'Chosen start date is after your chosen end date, please fix!'
        }

        return render(request, "export.html", context)        
    else:
      context = {
        'form': form,
        'project_id': request.GET.get('project_id'),
        'error': ''
      }

      return render(request, "export.html", context)
  else:
    return HttpResponseRedirect('/')

