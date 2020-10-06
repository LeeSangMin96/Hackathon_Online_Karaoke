"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from echo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_sing_url', views.get_url, name='get_url'),
    path('karaoke', views.karaoke, name='karaoke'),
    path('stop', views.stop, name='stop'),
    path('set_delay_interval', views.set_delay_interval, name='set_delay_interval'),
    path('set_delay_volume_decay', views.set_delay_volume_decay, name='set_delay_volume_decay'),
    path('set_delay_num', views.set_delay_num, name='set_delay_num')
]
