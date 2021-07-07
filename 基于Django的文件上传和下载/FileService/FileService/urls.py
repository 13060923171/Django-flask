"""FileService URL Configuration

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
from django.conf.urls import url
from django.urls import include
from fileoperation import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$', views.render_home_template, name='render_home_template'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^download/(?P<filename>.+)$', views.download, name='download'),
    url(r'^deleteFile/(?P<filename>.+)$', views.deleteFile, name='deleteFile'),
]
