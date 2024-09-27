from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
    """注销用户"""
    logout(request)    #我们不用亲自写login和logout方法
    return HttpResponseRedirect(reverse('learning_logs:index'))    #只需要调用写好的logout方法，并重定向到主页即可


def register(request):
    """注册新用户"""
    if request.method != 'POST':
        # 即用户的需求一开始没有涉及到提交的时候，就显示空的注册表单
        form = UserCreationForm()   # 此处是创建一个UserCreationForm实例，
    else:
        # 如果用户有post了，就处理填写好的表单
        form = UserCreationForm(request.POST)    #此处是创建一个UserCreationForm实例，该实例提供了用户注册功能所需的基本表单字段，并自动处理了密码验证、哈希存储等安全措施。
        if form.is_valid():
            new_user = form.save()
            #让用户自动登录，再重定向到主页
            authenticated_user = authenticate(username=new_user.username,password=request.POST['password1'])    #验证用户凭据，POST从字典中获取键！！！证明上传的参数中有key叫password1的，且不能使用 new_user.password1 因为 new_user.password 中存储的是加密后的哈希值，而不是用户提交的原始密码。
# 应该从 request.POST 中获取密码，因为这是用户输入的明文密码，authenticate() 需要它来验证用户身份。
            login(request,authenticated_user)
            if authenticated_user is not None:
                login(request, authenticated_user)
                # 重定向到主页
                return HttpResponseRedirect(reverse('learning_logs:index'))
        else:
            # 表单无效时，显示错误信息
            context = {'form': form}
            return render(request, 'users/register.html', context)
        return HttpResponseRedirect(reverse('learning_logs:index'))
    context = {'form':form}     #是一个python字典，用来存储将要传递给模板的数据。
    return render(request,'users/register.html',context)   # 视图会把 form 对象传递给模板。模板会使用这个 form 对象在页面上渲染表单控件，或者在验证失败时显示用户输入的内容和相应的错误消息。
