from django.contrib import admin
"""在Django中，contrib是一个缩写，代表了"contribution"（贡献）一词。contrib模块是Django框
架提供的一组官方贡献模块的集合，它们为开发者提供了各种可重用的功能和组件，以便快速构建Web应用程序。
contrib模块通常包含与常见应用程序需求相关的功能，例如身份验证、会话管理、管理后台、表单处理等。
这些模块经过精心设计和广泛测试，可以大大简化开发过程，并且符合Django的设计哲学和最佳实践。"""
# Register your models here.在admin.py中注册模型
from learning_logs.models import Topic,Entry      #导入需要注册的模型
admin.site.register(Topic)      #让Django通过管理网站来管理我们的模型
admin.site.register(Entry)