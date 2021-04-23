"""KitSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from tasks.views import (NewTaskView, StatusListView, TaskListView,
                         TaskRetrieveDestroyView, TaskUpdateView, CheckUpdateView)

from rest_framework.documentation import include_docs_urls


class Login(TokenObtainPairView):
    """ Получить JWT токен чтобы войти """
    pass


class RefreshToken(TokenRefreshView):
    """ Получить refresh_token """
    pass


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name='token_login'),
    path('refresh/', RefreshToken.as_view(), name='token_refresh'),
    path('status-list/', StatusListView.as_view(), name='status_list'),
    path('new-task/', NewTaskView.as_view(), name='new_task'),
    path('task-list/', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/',
         TaskRetrieveDestroyView.as_view(),
         name='task_retrieve_destroy'),
    path(
        'task-update/<int:pk>/', TaskUpdateView.as_view(), name='task_update'
    ),
    path(
        'check-update/<int:pk>/', CheckUpdateView.as_view(), name='task_update'
    ),
    path('', include_docs_urls(title='Blog API'))
]
