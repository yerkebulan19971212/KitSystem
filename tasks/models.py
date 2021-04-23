from django.contrib.auth.models import User
from django.db import models

from .tasks import send_notification_by_time_to_email


class Status(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    performer = models.ForeignKey(User,
                                  related_name='performer',
                                  on_delete=models.CASCADE)
    observers = models.ManyToManyField(User, related_name='observers')
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    planned_completion_time = models.DateTimeField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Task, self).save()

        text = "надо проверить {} время пришло ".format(self.name)
        send_notification_by_time_to_email.apply_async([[self.performer.email],
                                                        text],
                                                       eta=self.end_time)


class Check(models.Model):
    name = models.CharField(max_length=256)
    done = models.BooleanField(default=False)
    task = models.ForeignKey(Task, related_name="check_list", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class ChangeOfStatus(models.Model):
    last_status = models.ForeignKey(Status,
                                    related_name='last_status',
                                    on_delete=models.CASCADE)
    next_status = models.ForeignKey(Status,
                                    related_name='next_status',
                                    on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    changed_by_whom = models.ForeignKey(User, on_delete=models.CASCADE)


class Notification(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    reminder_text = models.TextField()
    list_of_users_for_whom_this_notification = models.ManyToManyField(User)
