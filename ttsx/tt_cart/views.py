#coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum

from models import CartInfo
from tt_user.user_decorators import user_login
# Create your views here.
def add(request):
    dict=request.GET
    gid=int(dict.get('gid'))
    count=int(dict.get('count'))

    uid=request.session.get('uid')
    #查询当前用户是否已经购买过此商品，如果未购买则创建，如果已购买则修改数量
    carts=CartInfo.objects.filter(user_id=uid,goods_id=gid)
    if len(carts)==0:
        cart=CartInfo()
        cart.user_id=request.session.get('uid')
        cart.goods_id=int(gid)
        cart.count=int(count)
        cart.save()
    else:
        cart=carts[0]
        cart.count+=count
        cart.save()

    c=calc_count(uid)

    return JsonResponse({'isok':1,'count':c})

@user_login
def cart(request):
    cart_list=CartInfo.objects.filter(user_id=request.session.get('uid'))
    context={'title':'购物车','cart_list':cart_list}
    return render(request,'tt_cart/cart.html',context)

def delcart(request):
    try:
        cid=int(request.GET.get('cid'))
        cart=CartInfo.objects.get(pk=cid)
        cart.delete()
        return JsonResponse({'isok':1})
    except:
        return JsonResponse({'isok':0})

def set(request):
    dict=request.GET
    cid=dict.get('cid')
    count=dict.get('count')

    isok=0

    try:
        cart = CartInfo.objects.get(pk=cid)
        cart.count=int(count)
        cart.save()
        isok=1
        count=cart.count
    except CartInfo.DoesNotExist as e1:
        isok=0
        count=0
    except:
        isok=0
        count=cart.count
    return JsonResponse({'isok':isok,'count':count})

def count(request):
    c=calc_count(request.session.get('uid'))
    return JsonResponse({'count': c})

def calc_count(uid):
    # c=CartInfo.objects.filter(user_id=request.session.get('uid')).count()
    c=CartInfo.objects.filter(user_id=uid).aggregate(Sum('count'))
    print c
    if c.get('count__sum')==None:
        return 0
    else:
        return c.get('count__sum')

