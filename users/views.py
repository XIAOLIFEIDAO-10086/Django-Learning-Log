from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
    """注销用户"""
    logout(request)    #我们不用亲自写login和logout方法
    return HttpResponseRedirect(reverse('learning_logs:index'))    #只需要调用写好的logout方法，并重定向到主页即可


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def register(request):
    """注册新用户"""
    if request.method != 'POST':
        # 显示空的注册表单
        form = UserCreationForm()
    else:
        # 处理填写好的表单
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # 验证用户凭据并登录
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            if authenticated_user is not None:
                login(request, authenticated_user)
                # 重定向到主页
                return HttpResponseRedirect(reverse('learning_logs:topics'))
        else:
            # 如果表单无效，返回表单并显示错误信息
            context = {'form': form}
            return render(request, 'users/register.html', context)

    # 渲染表单页面
    context = {'form': form}
    return render(request, 'users/register.html', context)
