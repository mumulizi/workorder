from django.contrib import admin

# Register your models here.
from workorder import models

admin.site.register(models.mywork)
admin.site.register(models.web_workorder)
admin.site.register(models.data_workorder)
admin.site.register(models.svn_workorder)
# admin.site.register(models.web_workorder_add)