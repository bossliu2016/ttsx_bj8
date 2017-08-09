#coding=utf-8
from django.shortcuts import redirect
def user_login(func):
    def func1(request,*args,**kwargs):
        #判断用户是否登录
        if request.session.has_key('uid'):
            #如果登录，则继续执行视图
            return func(request,*args,**kwargs)
        else:
            #如果没登录，则转到登录页
            return redirect('/user/login/')
    return func1

# def fun1(func):
#     def fun2():
#         pass
#     return fun2
