#coding=utf-8
from django.shortcuts import render,redirect
from django.db import transaction
from datetime import datetime

from tt_user.models import UserInfo
from tt_cart.models import CartInfo
from models import *
# Create your views here.
def list(request):
    uid=request.session.get('uid')
    user=UserInfo.objects.get(pk=uid)

    dict=request.POST
    cids=dict.getlist('cid')
    cart_list=CartInfo.objects.filter(pk__in=cids)

    context={'title':'订单页面','user':user,'cart_list':cart_list}
    return render(request,'tt_order/list.html',context)

@transaction.atomic
def handle(request):
    sid = transaction.savepoint()

    try:
        dict=request.POST
        cids=dict.getlist('cid')
        address=dict.get('address')
        uid=request.session.get('uid')
        '''
        创建订单主表对象
        判断商品库存是否足够
        遍历购物车信息，创建订单详表
        将商品数量减少
        '''
        order=OrderInfo()
        order.oid='%s%d'%(datetime.now().strftime('%Y%m%d%H%M%S'),uid)
        order.user_id=uid
        order.ototal=0
        order.oaddress=address
        order.save()

        cartlist=CartInfo.objects.filter(pk__in=cids)
        total=0
        for cart in cartlist:
            if cart.count>cart.goods.gkucun:
                #库存不足，放弃购买
                transaction.savepoint_rollback(sid)
                return redirect('/cart/')
            else:
                #库存足够，创建详单
                detail=OrderDetailInfo()
                detail.goods=cart.goods
                detail.order=order
                detail.price=cart.goods.gprice
                detail.count=cart.count
                detail.save()
                #修改库存数量
                goods=cart.goods
                goods.gkucun-=cart.count
                goods.save()
                # 计算总价
                total+=detail.price*detail.count
                #删除购物车
                cart.delete()
        #保存总价
        order.ototal=total
        order.save()
        #购买成功
        transaction.savepoint_commit(sid)
        return redirect('/user/order/')
    except:
        # raise
        transaction.savepoint_rollback(sid)
        return redirect('/cart/')

