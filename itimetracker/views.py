
from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import login as login_view
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.db import IntegrityError
from django.forms import inlineformset_factory
from django.db.models import Q

from datetime import datetime, timedelta, date
import re

from .models import Time, Task, Role, ProjectTask, Project, Category
from .forms import ProjectTaskForm, CategoryForm

def isfloat(n):
  try:
    float(n)
    return True
  except ValueError:
    return False

# /internal/itimetracker/ index
def index(request):
  # print('index()')
  if request.user.username:
    url = '/timetracker/%s' % request.user.username
  else:
    url = '/'

  return HttpResponseRedirect(url)

# login screen or redirect to user's time sheet
def login_or_redirect(request):
  # print('login or redirect')
  if request.user.is_authenticated():
    return index(request)
  elif request.method == 'POST':
    # print('request is POST')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
      if user.is_active:
        login(request, user)
        return HttpResponseRedirect('/timetracker/%s' % username)
  else:
    return login_view(request)

def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/')

def help(request):
  context = {'is_superuser': request.user.is_superuser}
  return render(request, 'help.html', context)

def delete_project_task(request, id):
  project_task = get_object_or_404(ProjectTask, id=id)

  next = request.GET.get("next") # we're going to extract the current date from this

  username = project_task.user.username

  next_date = re.search('/timetracker/%s/(.*)' % username, next).group(1)

  # just make it the beginning of the week, i.e. Monday
  today = datetime.strptime(next_date, '%Y/%m/%d')
  monday = today - timedelta(days=(today.isocalendar()[2]-1))

  project_task.delete_date = monday

  project_task.save()

  return HttpResponseRedirect(request.GET.get("next"))

def save_time(request, username):
  if request.method == 'POST':
    if 'calendar_submit' in request.POST:
      week_start_date = request.POST.get('monday')
      for item in request.POST.items():
        # print(item)
        # ptid vs tid
        # We distinguish between the two cases by assigning ptid or tid to the input name
        # The project_task id is given to know which project_task to assign the new value to
        # the time id is given to know which time record to update
        if 'ptid' in item[0]:
          # item was set with a duration
          if isfloat(item[1]):
            duration = float(item[1])
            if duration > 0:
              # add it to the DB
              t_list = re.findall(r'\d+', item[0])
              day = int(t_list[1]) - 1 # start counting at 0

              today = datetime.strptime(week_start_date, '%Y/%m/%d') # arbitrary date from datepicker input
              monday = today - timedelta(days=(today.isocalendar()[2] - 1)) # get the corresponding monday

              # now take the integer from the input name in variable 'day'
              # that will be your day of the week to insert into the DB
              date = monday

              if day > 0:
                date += timedelta(days=day)

              ptid = t_list[0]

              project_task = ProjectTask.objects.get(id=ptid)

              time = Time(project_task=project_task, duration=duration, date=date)
              time.save()
        elif 'tid' in item[0]: # it has a value, update the DB *if value is different*
          user = get_object_or_404(User, username=username)
          t_list = re.findall(r'\d+', item[0])
          tid = t_list[0]
          day = t_list[1]
          time = Time.objects.get(id=tid)

          if isfloat(item[1]):
            duration = float(item[1])
            if duration > 0:
              time.duration = duration
              time.save()
            else:
              # print('deleting time row')
              time.delete()
            
  return HttpResponseRedirect('/timetracker/%s' % username)

def by_user(request, username, year=0, month=0, day=0):
  # WHAT ARE YOU DOING HERE?!
#  if request.user.username != username:
#    return HttpResponseRedirect('/')

  if not request.user.is_authenticated():
    return HttpResponseRedirect('/')

  # get the user object
  user = get_object_or_404(User, username=username) # confirm username exists or 404

  # need to rearrange so it is year/month/day
  year = int(year)
  month = int(month)
  day = int(day)

  curr_week = ''

  if month > 0 and month < 13 and day > 0 and day < 32 and year > 0:
    today = date(year, month, day)
    curr_week = 'this is not the current week'
  else:
    today = timezone.now().date()
    curr_week = 'this is the current week'

  this_monday = today - timedelta(days=(today.isocalendar()[2] - 1))
  next_monday = this_monday + timedelta(days=7)

  dates = [(this_monday + timedelta(days=(i))).strftime('%-m/%-d') for i in range(7)]

  date_picked = today.strftime('%Y/%m/%d') # Add '-' between '%' and 'm' to remove leading 0
  calendar = [] # formatting DB data to be displayed in a table in the template
  duration_totals = [0,0,0,0,0,0,0] # duration sums by week day

  last_monday = this_monday - timedelta(days=7)

  lastweek = this_monday - timedelta(days=7)
  nextweek = this_monday + timedelta(days=7)

  project_task_list = ProjectTask.objects.filter(user=user, project__open=True).filter(Q(delete_date__isnull=True) | Q(delete_date__gt=this_monday)).order_by('project', 'task') # ProjectTasks by User

  project_totals = {}

  for project_task in project_task_list: # For each of the user's ProjectTasks
    week = [] # capture the current week for a given ProjectTask
    times = Time.objects.filter(date__gte=this_monday, date__lt=next_monday, project_task=project_task)
    for x,i in enumerate([2,3,4,5,6,7,1]): # For each user's ProjectTask by DotW, Django uses Sunday = 1, so Monday = 2
      day = times.filter(date__week_day=i) # For a given day
      week.append(day)
      if day:
        duration_totals[x] += day[0].duration
        if project_task.project.name in project_totals:
          project_totals[project_task.project.name] += day[0].duration
        else:
          project_totals[project_task.project.name] = day[0].duration
      elif project_task.project.name not in project_totals:
        project_totals[project_task.project.name] = 0
    calendar.append([project_task.project.name, project_task.task.name, week, project_task.id])

  # REQUEST HANDLER

  start_monday = None

  if request.method == 'POST': # page save handler
    if 'project_task' in request.POST:
      project = Project.objects.get(id=request.POST['project'])
      task = Task.objects.get(id=request.POST['task'])

      pt_instance = ProjectTask.objects.get_or_create(project=project, task=task, user=user)

      pt_form = ProjectTaskForm(request.POST, instance=pt_instance[0])

      if pt_form.is_valid():
        project_task = pt_form.save(commit=False)

        project_task.user = user
        project_task.delete_date = None
        project_task.save()

        next = request.POST.get('next')

        return HttpResponseRedirect(next)
  else:
    if request.GET.get("category"):
      category_form = CategoryForm()

      cid = request.GET.get("category")

      pt_form = ProjectTaskForm(category=cid)

      if request.GET.get("project"):
        pid = request.GET.get("project")
      else:
        pid = None
    else:
      category_form = CategoryForm()
      pt_form = ProjectTaskForm()

      pid = None
      cid = None

  context = {
    'calendar': calendar,
    'user': user,
    'duration_totals': duration_totals,
    'totals_sum': sum(duration_totals),
    'project_task_form': pt_form,
    'date_picked': date_picked,
    'calendar_len': len(calendar),
    'dates': dates,
    'project_totals': project_totals,
    'current_user': request.user.first_name,
    'category_form': category_form,
    'pid': pid,
    'cid': cid,
    'lastweek': lastweek.strftime('%Y/%m/%d'),
    'nextweek': nextweek.strftime('%Y/%m/%d'),
  }

  return render(request, 'timetracker/by_user.html', context)

def project_time(request, id):
  project = get_object_or_404(Project, id=id)

  return HttpResponseRedirect('/')
