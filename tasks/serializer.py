from django.contrib.auth.models import User
from rest_framework import serializers

from tasks.models import ChangeOfStatus, Status, Task, Notification, Check

from .tasks import send_notification_by_time_to_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'first_name', 'last_name', 'email')


class CheckListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Check
        fields = ('pk', 'name', 'done')
        extra_kwargs = {
            'pk': {'read_only': True}
        }


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ('pk', 'name')


class NewTaskSerializer(serializers.ModelSerializer):
    check_list = CheckListSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ('pk',
                  'name',
                  'description',
                  'performer',
                  'observers',
                  'status',
                  'start_time',
                  'end_time',
                  'planned_completion_time',
                  'check_list')
        extra_kwargs = {
            'pk': {'read_only': True}
        }

    def create_check_list(self, task, check_list):
        print(check_list)
        Check.objects.bulk_create([
            Check(task=task, **d) for d in check_list
        ])

    def create(self, validated_data):
        check_list = validated_data.pop('check_list', [])
        task = super().create(validated_data)
        self.create_check_list(task, check_list)
        return task

    def update(self, instance, validated_data):
        status = validated_data.get('status', None)
        request = self.context.get('request', None)
        if request:
            user = request.user
        if status and status != instance.status:
            observer_users = instance.observers.all()
            text = "изменен статус на " + status.name

            ChangeOfStatus.objects.create(
                last_status=instance.status,
                next_status=status,
                task=instance,
                changed_by_whom=user
            )

            notification = Notification.objects.create(
                task=instance,
                reminder_text=text
            )
            notification.list_of_users_for_whom_this_notification.add(
                *observer_users)

            users_email = [user.email for user in observer_users]
            send_notification_by_time_to_email.delay(users_email, text)

        return super().update(instance, validated_data)


class TaskSerializer(serializers.ModelSerializer):
    performer = UserSerializer(read_only=True)
    observers = UserSerializer(read_only=True, many=True)
    status = StatusSerializer(read_only=True)
    check_list = CheckListSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ('pk',
                  'name',
                  'description',
                  'performer',
                  'observers',
                  'status',
                  'start_time',
                  'end_time',
                  'planned_completion_time',
                  'check_list')
# {
#     "name": "12345678",
#     "description": "kdslknslfgn",
#     "performer": 3,
#     "observers": [
#         2
#     ],
#     "status": 1,
#     "start_time": "2021-04-23T03:50:00Z",
#     "end_time": "2021-04-23T03:50:00Z",
#     "planned_completion_time": "2021-04-23T03:50:00Z",
#     "check_list": [
#         {"name":"sdfgh"},
#        {"name":"edrftgyhuj"},
# {"name":"123124"}
#     ]
# }