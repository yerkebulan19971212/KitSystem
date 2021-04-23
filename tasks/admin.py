from django.contrib import admin

from .models import ChangeOfStatus, Notification, Status, Task, Check

admin.site.register([Status, Task, ChangeOfStatus, Notification, Check])
