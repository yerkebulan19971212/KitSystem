from django.core.mail import send_mail

from KitSystem import settings
from KitSystem.celery import app


@app.task
def send_notification_by_time_to_email(email_list: list, name: str):
    send_mail(
        'Task',
        name,
        settings.EMAIL_HOST_USER,
        email_list,
    )
