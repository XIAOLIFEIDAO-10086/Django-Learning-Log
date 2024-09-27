from django.db import models    #模型就是一个类，包含属性和方法
from django.contrib.auth.models import User
# Create your models here.
"""新建一个app应用后第一步是建立模型"""
"""建立模型时需要想想涉及的数据，首先模型中的数据包含，1、主题，2、条目，3、时间戳，都将以文本的方式显示"""


class Topic(models.Model):
    """用户学习的主题"""
    text = models.CharField(max_length=200)     #需要存储少量的文本，如名称、标题或城市时，可以使用CharField
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)      #当删除用户User时，需要将相关联的数据全部删掉，此语句是建立到user的外键，加了这个外键之后就需要制定owner对应的user的id，owner的值是每个主题对应的用户
    def __str__(self):
        return self.text     #str 是一个特殊的方法（也称为“魔术方法”或“双下划线方法”），用于定义对象的字符串表示形式。当你尝试使用 print() 函数打印一个对象或者使用 str() 函数将对象转换为字符串时，Python会自动调用该对象的 str 方法。


class Entry(models.Model):
    """学到的某个主题的具体知识"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE) #在创建一对多的关系的,需要在ForeignKey的第二参数中加入on_delete=models.CASCADE 主外关系键中，级联删除，也就是当删除主表的数据的时候从表中的数据也随着一起删除。
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    class Meta:             #Meta类是元数据的意思
        verbose_name_plural = 'entries'
    def __str__(self):       #用于返回对象的呈现方式
        """返回模型的字符串表示"""
        text_len = len(self.text)
        if text_len > 50:
            return self.text[:50]+"..."
        else:
            return self.text