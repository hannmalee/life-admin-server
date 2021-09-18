"""lifeadmin URL Configuration

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
from lifeadminapi.views.task import TaskView
from lifeadminapi.views.household import HouseholdView
from lifeadminapi.views.household_user import HouseholdUserView
from django.contrib import admin
from django.urls import path
from lifeadminapi.views import CategoryView, login_user, register_user
from rest_framework import routers
from django.conf.urls import include


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'categories', CategoryView, 'category')
router.register(r'household_users', HouseholdUserView, 'household_user')
router.register(r'households', HouseholdView, 'household')
router.register(r'tasks', TaskView, 'task')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]

