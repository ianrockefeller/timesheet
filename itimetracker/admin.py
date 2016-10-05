from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from .models import Task, Role, Time, Project, Client, ProjectTask, UserProfile, Category
from .actions import export_xlsx


class CategoryResource(resources.ModelResource):
  class Meta:
    model = Category
    fields = ('code', 'name',)

class TaskResource(resources.ModelResource):
  category = fields.Field(
    column_name = 'category',
    attribute = 'category',
    widget = widgets.ForeignKeyWidget(Category, 'name'))

  class Meta:
    model = Task
    fields = ('code', 'category', 'name',)

class CategoryAdmin(ImportExportModelAdmin):
  pass

class TaskAdmin(ImportExportModelAdmin):
  pass

# Define an inline admin descriptor for UserProfile model
class UserProfileInline(admin.StackedInline):
  model = UserProfile
  can_delete = False
  verbose_name_plural = 'role'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
  inlines = (UserProfileInline, )

def export_projects(modeladmin, request, queryset):
  from django.http import HttpResponseRedirect

  get_var = []
  
  for qs in queryset:
    # FILTER OUT NON-CLIENT PROJECTS HERE
    if qs.open == True and qs.id != 2 and qs.id != 6:
      get_var.append(str(qs.id))

  return HttpResponseRedirect("/export/?project_id=%s" % ','.join(get_var))

export_projects.short_description = "Export selected projects"

class ProjectAdmin(admin.ModelAdmin):
  actions = [export_projects]

# Comment these out in production
admin.site.register(ProjectTask)
admin.site.register(Time)

# Leave these
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Client)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Role)
