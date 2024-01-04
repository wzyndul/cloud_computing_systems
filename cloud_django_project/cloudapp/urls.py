"""
URL configuration for test_django_chmurki project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index_page'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('storage/', views.storage, name='storage'),
    path('logout/', views.logout_user, name='logout_user'),
    path('change_version/', views.change_version, name='change_version'),
    path('download_file/', views.download_file, name='download_file'),
]
