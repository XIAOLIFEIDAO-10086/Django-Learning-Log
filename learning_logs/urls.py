"""定义learning——logs的URL模式"""
from django.urls import path
#用来将 URL 模式与视图函数（或视图类）连接起来。Django 通过这个连接来确定当用户访问某个 URL 时应该执行哪个视图。
#使用 path 可以让你指定 URL 路径，以及当请求匹配该路径时，应该由哪个视图函数来处理。
from . import views
app_name = 'learning_logs'
"""这句代码导入当前应用目录下的 views.py 文件中的内容（即模块）。views.py 文件通常包含多个视图函数或
视图类，这些视图是处理用户请求的核心逻辑。每个视图函数通常会返回一个响应（例如 HTML 页面、JSON 数据等）。"""
urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),    #通过views方法中的topic来获取topic的id，从而完成url的编写，说白了也是一个动态的
    #定义了topics后，与该模式匹配点请求都用views中的函数topics（）进行处理
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>', views.new_entry, name='new_entry'),   #这个动态传参在view中实现
    path('edit_entry/<int:entry_id>',views.edit_entry, name='edit_entry'),
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
]

#urlpatterns是一个列表，包含在learning_logs应用中能请求的网页，第一个表达的是要匹配的路径，第二个实参指定了要
#调用的视图函数，请求匹配时，Django将调用view.index这个视图函数，第三个实参是将这个URL模式的名称指定为index，让我们能够在
#其他地方引用它，每当需要提供这个主页的链接时，我们都使用这个名称，而不是编写URL。也就是在html中以{% url ‘应用名：命名空间’%}来找到他
"""类似于层层传导，这个是总的url的下级路由"""