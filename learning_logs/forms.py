from django import forms
from .models import Topic,Entry
class TopicForm(forms.ModelForm):   #定义一个名为 TopicForm 的类，继承自 forms.ModelForm。ModelForm 是 Django 提供的一个方便类，它可以基于数据库模型自动生成表单，处理表单字段验证和数据保存等功能。
    class Meta:     #这是 ModelForm 的内部类，用来指定表单与哪个模型关联，以及要使用哪些字段。
        model = Topic     #这里指定了该表单基于 Topic 模型。它会根据 Topic 模型的定义来创建表单的字段。
        fields = ['text']      #指定表单只包含 Topic 模型中的 text 字段。这个列表可以包含模型中的多个字段，但这里仅使用了 text 字段。
        labels = {'text':''}     #这是用来自定义字段的标签（label）。在表单中，字段通常会有默认标签（一般为字段名的首字母大写形式）。此处将 text 字段的标签设为空字符串，因此在表单中该字段不会显示标签。

class EntryForm(forms.ModelForm):    #这里的表单文件是决定表单具有哪些东西，如标签介绍，文本框等，而css则可以写表单的样式
    class Meta:
        model = Entry
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'style': 'resize: none;'}),
        }
# widgets 字典用于指定表单字段的渲染方式。
# forms.Textarea 将 text 字段渲染为一个多行文本区域 (<textarea>)，并通过 attrs 设置了 cols 属性，将其宽度设置为 80 个字符。
# 通过使用 widgets，你可以灵活地控制表单在前端页面中的展示形式，改善用户的输入体验。
# attrs 是一个 字典，全称为attributes（属性）
