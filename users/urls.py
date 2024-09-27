"""为应用程序users定义URL模式"""
from django.urls import path
from django.contrib.auth.views import LoginView
from .import views      #这个.指的是从当前模块中导入view
app_name = 'users'    #django4中需要为每个urls文件加一个app_name,来确保命名空间正常使用
urlpatterns = [
    # 登录页面
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    # 它将用户访问特定 URL 的请求与相应的视图类进行关联，
    # name='login' 为这个 URL 模式命名，使得在 Django 的模板或视图中可以通过名字引用这个 URL，而不必硬编码实际的路径。
    # 例如，在模板中可以使用 {% url 'login' %} 来生成 /login/ 的 URL。
]

