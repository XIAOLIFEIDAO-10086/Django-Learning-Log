from lib2to3.fixes.fix_input import context
from django.http import HttpRequest, HttpResponse,HttpResponseRedirect,Http404    #最后这个是重定向的类，用户提交主题后，我们返回显示全部主题的页面
from django.urls import reverse
from django.shortcuts import render     #django.shortcuts是快捷函数的意思，其中render是用于渲染模版，并将其呈现给用户
from .forms import TopicForm,EntryForm
from learning_logs.models import Topic,Entry     #.models和learning_logs.models的区别，一个是相对导入，在同一app下即可，一个是绝对导入，在任何条件下均可，这个就相当于把Topic和Entry模型中的数据都用上了
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Topic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your views here.是命令python manage.py startapp自动生成的
"""待回答：视图的作用,视图用于编写url中写的函数，视图函数多用于返回页面数据等等"""

def index(request):
    """学习笔记的主页"""
    return render(request,'learning_logs/index.html')
    # html = '<h1> Hello World </h1>'
    # return HttpResponse(html, status=200)
#这里给render函数提供了两个实参，一个是原始请求对象，一个是可用于创建网页的模版,应该是模版路径下面的文件的路径）
"""request: 是一个固定参数
template_name: templates中定义的文件，注意路径名。比如：“templates/polls/index.html,
总的来说render是用来封装一个比较大的html模版的，不方便写在views里
而HttpResponse则是简单的返回某些http模版"""

@login_required # 这个修饰器让Python在运行topics（）代码前先运行login_required（）的代码
def topics(request):
    """显示所有主题，需要从数据库中获取一些数据，并将其发送给模版"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')  #这里和models中的topic类联系起来了,filter（owner=request.user） 是一种常见的查询方式，用于从数据库中过滤出与当前登录用户关联的对象。
    context = {'topics': topics}
    return render(request,'learning_logs/topics.html', context)  #这里和templates中的html模版联系起来了，context应该是要发送给模版的上下文，上下文是一个字典

@login_required
def topic(request,topic_id):
    """显示单个主题及其所有的条目"""
    topic = Topic.objects.get(id=topic_id)    #我们通过get来获取对应id条目的topic主题
    # 确认请求的主题属于当前用户
    if topic.owner != request.user:       #这两者都是id
        raise Http404
    entries = topic.entry_set.order_by('-date_added')     #将对应的条目按创建时间倒序排列，先显示最近条目
    context = {'topic': topic, 'entries': entries}        #将主题和条目都存储在字典context中，再将字典发送给模版
    return render(request,'learning_logs/topic.html',context)     #将字典发送给模版

@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单,就是一开始的时候显示一个表单
        form = TopicForm()
    else:
        # POST提交数据，对数据进行处理
        form = TopicForm(request.POST)     #将用户提交的数据绑定到表单实例 form，以便后续进行验证和处理。request 是 Django 视图中的参数，它包含了浏览器发送到服务器的整个 HTTP 请求，包括请求方法（GET、POST 等）、请求头、请求体等。request.POST 表示从 HTTP 请求中提取的POST 数据。
        if form.is_valid():     #valid是有效的意思
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))    #动态的url，对应宏观主题页，区别微观展现每个主题话题的主题页
    context = {'form': form}
    return render(request,'learning_logs/new_topic.html',context)    #初次执行时if都成立，然后执行最后一句，返回一个表单给用户，然后如果提交后执行了else就重定向了


@login_required
def new_entry(request,topic_id):
    """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # 未提交数据，创建一个空表单
        form = EntryForm()
    else:
        # Post提交数据，对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=(topic_id,)))    #reverse是动态生成url用的库，args 是 reverse 的一个参数，用来为 URL 中的动态部分传递参数。
# (topic_id,)：这里的 args 是一个元组，其中的 topic_id 是动态生成的 ID。它会替换 URL 中的变量（通常是像 <int:topic_id> 这样的路径参数）。
    context = {'topic':topic,'form': form}
    return render(request,'learning_logs/new_entry.html',context)
# 当用户访问 URL /topics/1/new_entry/ 时，Django 会将 1 作为 topic_id 传递给 new_entry 视图函数。这样，视图中的 topic_id 就会自动获得 URL 中的参数值。


@login_required
def edit_entry(request,entry_id):
    """编辑即有条目"""
    entry = Entry.objects.get(id=entry_id)    #这个是通过点击传入的,也就是获取用户要修改的条目对象
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)    #使用instance=entry 时，Django 会用这个 entry 实例的现有数据来填充表单字段，以便用户可以看到当前条目内容并对其进行修改。
    else:
        # Post提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)    #instance是确保修改这个已有实例
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=(topic.id,)))
    context = {'entry':entry,'topic':topic,'form': form}
    return render(request,'learning_logs/edit_entry.html',context)
#虽然edit能编辑但是不能删除


@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        topic.delete()
        return redirect('learning_logs:topics')  # 确保重定向到主题列表页面


@login_required
def delete_entry(request, entry_id):
    """删除特定条目"""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic  # 获取对应的主题，方便重定向
    if request.method == 'POST':
        entry.delete()
        return redirect('learning_logs:topic', topic.id)  # 删除后重定向到该主题页面

    class CustomUserCreationForm(UserCreationForm):
        class Meta:
            model = User
            fields = ('username', 'password1', 'password2')

        def __init__(self, *args, **kwargs):
            super(CustomUserCreationForm, self).__init__(*args, **kwargs)

            # Remove help text
            self.fields['username'].help_text = None
            self.fields['password1'].help_text = None
            self.fields['password2'].help_text = None

            # Remove labels if needed or modify them
            self.fields['username'].label = 'Username'
            self.fields['password1'].label = 'Password'
            self.fields['password2'].label = 'Password confirmation'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # Remove help text
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        # Remove labels if needed or modify them
        self.fields['username'].label = 'Username'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Password confirmation'