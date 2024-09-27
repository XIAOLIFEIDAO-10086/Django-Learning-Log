"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('learning_logs.urls',namespace='learning_logs')),     #URLconf是一个文件（通常称为网址.py)它包含给定特定应用程序的所有url模式映射。
    path('users/',include('users.urls',namespace='users')),     #命名空间namespace是用来隔离不同app中的相同url的，一旦你为应用的 URL 定义了命名空间，你在使用 reverse() 函数或者在模板中使用 {% url %} 标签时，必须指定该命名空间，以便 Django 能正确找到 URL。
]           #当包含其他url模式时，应总是使用include（），admin.site.urls是唯一的例外
