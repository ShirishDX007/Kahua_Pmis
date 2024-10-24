from django.contrib import admin
from .models import Client, Project, Task
from import_export.admin import ImportExportModelAdmin

class PmisAdmin(ImportExportModelAdmin):
    pass
admin.site.register(Task, PmisAdmin)
admin.site.register(Project, PmisAdmin)

# Register your models here.
class PmisAdmin(admin.ModelAdmin):
    pass

admin.site.register(Client, PmisAdmin)

