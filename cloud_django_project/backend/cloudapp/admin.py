from django.contrib import admin
from cloudapp.models import UserActivityLog, FileActivityLog

admin.site.register(UserActivityLog)
admin.site.register(FileActivityLog)
