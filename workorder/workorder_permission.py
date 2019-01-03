#!/usr/bin/env python
#_*_coding:utf-8_*_
#__author__="lihongxing"

from django.shortcuts import render
from django.db.models import Q
from django.core.urlresolvers import resolve
from workorder import user_group
def perm_workorder_check(request,**kwargs):
    web_user = str(request.user.username)
    print web_user,user_group.approvel
    if web_user in user_group.admin or user_group.approvel:
        return True
    else:
        return False

def check_online_permission(fun):
    def wapper(request, *args, **kwargs):
        if perm_workorder_check(request, **kwargs):
            return fun(request, *args, **kwargs)
        return render(request, 'forbiden.html', locals())
    return wapper

