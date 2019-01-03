#!/usr/bin/env python
#_*_coding:utf-8_*_
#__author__="lihongxing"

from django.shortcuts import render
from django.db.models import Q
from django.core.urlresolvers import resolve
import user_group


web_user = str('wenqiang')
print web_user,user_group.approvel
if web_user in user_group.admin or user_group.approvel:
    print"true"
else:
    print"false"

