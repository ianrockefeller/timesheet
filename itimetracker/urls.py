from django.conf.urls import url

from . import views


urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^project/(?P<id>\d+)', views.project_time, name='project_time'),
  url(r'^delete/projecttask/(?P<id>\d+)/$', views.delete_project_task, name='delete_project_task'),
  url(r'^(?P<username>\w+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)', views.by_user, name='by_user'),
  url(r'^(?P<username>\w+)/save', views.save_time, name='save_time'),
  url(r'^(?P<username>\w+)', views.by_user, name='by_user'),
]

