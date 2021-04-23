from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveDestroyAPIView, UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Status, Task, Check
from .serializer import NewTaskSerializer, StatusSerializer, TaskSerializer, CheckListSerializer


class StatusListView(ListAPIView):
    """ Возвращает все статусы """
    permission_classes = (AllowAny,)
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class NewTaskView(CreateAPIView):
    """ назначать задачи """
    permission_classes = (IsAuthenticated,)
    serializer_class = NewTaskSerializer


class TaskListView(ListAPIView):
    """
     следить за их статусом
     возвращает список задач
    """
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all().prefetch_related('check_list')
    serializer_class = TaskSerializer


class TaskRetrieveDestroyView(RetrieveDestroyAPIView):
    """
    delete:
    Удалить задачу

    retrieve:
    возвращает одну задачу
    """
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all().prefetch_related('check_list')
    serializer_class = TaskSerializer


class TaskUpdateView(UpdateAPIView):
    """
    put:
    обновлять данные
    и изменить статусы

    patch:
    частичное обновление данных
    """
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all().prefetch_related('check_list')
    serializer_class = NewTaskSerializer


class CheckUpdateView(UpdateAPIView):
    """ обновить и закончить Check"""
    permission_classes = (IsAuthenticated, )
    queryset = Check.objects.all()
    serializer_class = CheckListSerializer
