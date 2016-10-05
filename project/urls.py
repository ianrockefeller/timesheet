
"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from itimetracker import views as itt_views
from . import views

urlpatterns = [
  url(r'^$', itt_views.login_or_redirect, name='login_or_redirect'),
  url(r'^logout/', itt_views.user_logout, name='user_logout'),
  url(r'^timetracker/', include('itimetracker.urls')),
  url(r'^help/', itt_views.help, name='help'),
# url(r'change-password', auth_views.password_change),
  url(r'^export/$', views.export_project, name='export_project'),
  url(r'^admin/', admin.site.urls),
  url(r'^password-reset/$',
    auth_views.password_reset,
    {'post_reset_redirect' : '/password-reset-done/'},
    name='password_reset_form'
  ),
  url(r'^password-reset-done/$',
    auth_views.password_reset_done,
    name='password_reset_done'
  ),
  url(r'^password-reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
    auth_views.password_reset_confirm,
    {'post_reset_redirect' : '/password-done/'},
    name = 'password_reset_confirm'
  ),
  url(r'^password-done/$',
        auth_views.password_reset_complete
  ),
]

