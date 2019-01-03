#!/usr/bin/env python
#_*_coding:utf-8_*_
#__author__="lihongxing"
#Date:2017/7/26

from django.db import models
from assets import models as asset_models
from app01 import models as app01_models

class mywork(models.Model):

    mywork_title = models.CharField(max_length=100,verbose_name=u"工单标题")
    other_id = models.CharField(max_length=1000,verbose_name=u'详细id')
    mywork_type_choice = (
    ('web',u'web相关'),
    ('sql',u'数据库相关'),
    ('svn',u'svn相关'),
    ('permission',u'新增权限'),
    ('other',u'其他'),
    ('conf_change',u'配置文件修改'),
    ('permission_change',u'权限变更'),
    ('sql_change)',u'数据库变更'),
    ('other_change',u'其他变更'),
    ('problem',u'故障申报'),
        )
    mywork_type = models.CharField(max_length=100,choices=mywork_type_choice,default='web',verbose_name=u"工单类型")
    mywork_memo = models.TextField(verbose_name=u"工单描述")
    mywork_action_user = models.ManyToManyField(app01_models.User,verbose_name=u"处理人")
    mywork_user = models.CharField(max_length=25,verbose_name=u"提交者")
    mywork_date = models.DateTimeField(verbose_name=u"提交时间")
    mywork_status = models.CharField(max_length=25,verbose_name=u"处理状态")
    mywork_ret = models.TextField(verbose_name=u"处理办法和结果",blank=True,null=True)

    def __str__(self):
        return self.mywork_title
    class Meta:
        verbose_name = u'工单列表'
        verbose_name_plural = u"工单列表"

class web_workorder(models.Model):
    web_title = models.CharField(max_length=100,verbose_name=u"工单标题")
    web_name = models.CharField(max_length=100,verbose_name=u"项目名")
    web_path = models.CharField(max_length=100,verbose_name=u"项目路径")
    web_memo = models.TextField(verbose_name=u"工单描述")
    web_action_user = models.ManyToManyField(app01_models.User,verbose_name=u"处理人")
    web_user = models.CharField(max_length=25,verbose_name=u"提交者")
    web_date = models.DateTimeField(verbose_name=u"提交时间")
    web_status = models.CharField(max_length=25,verbose_name=u"处理状态")
    web_ret = models.TextField(verbose_name=u"处理办法和结果",blank=True,null=True)
    web_create_svn_choice = (
        ('on',u'是'),
        ('off',u'否'),
    )
    web_create_svn_status = models.CharField(max_length=10,choices=web_create_svn_choice,default='off',verbose_name=u'是否创建svn',blank=True,null=True)
    web_create_cdn_choice = (
        ('on',u'是'),
        ('off',u'否'),
    )
    web_create_cdn_status = models.CharField(max_length=10,choices=web_create_cdn_choice,default='off',verbose_name=u'是否创建cdn',blank=True,null=True)

    web_create_https_choice = (
        ('on',u'是'),
        ('off',u'否'),
    )
    web_create_https_status = models.CharField(max_length=10,choices=web_create_https_choice,default='off',verbose_name=u'是否需要https',blank=True,null=True)

    domain_time = models.CharField(max_length=40,verbose_name=u'域名解析时间')


    def __str__(self):
        return self.web_title

    class Meta:
        verbose_name = u'web'
        verbose_name_plural = u"web"

class data_workorder(models.Model):
    sql_title = models.CharField(max_length=100,verbose_name=u"工单标题")
    sql_memo = models.TextField(verbose_name=u"工单描述")
    sql_name = models.CharField(max_length=100,verbose_name=u"数据库或表")
    sql_action_user = models.ManyToManyField(app01_models.User,verbose_name=u"处理人")
    sql_user = models.CharField(max_length=25,verbose_name=u"提交者")
    sql_date = models.DateTimeField(verbose_name=u"提交时间")
    sql_status = models.CharField(max_length=25,verbose_name=u"处理状态")
    sql_ret = models.TextField(verbose_name=u"处理办法和结果",blank=True,null=True)
    sql_action_choice = (
    ('add',u'增'),
    ('del',u'删'),
    ('change',u'改'),
    ('find',u'查'),
    ('other',u'其他'),
    )
    sql_action_status = models.CharField(max_length=10,choices=sql_action_choice,default='other',verbose_name=u'操作',blank=True,null=True)

    def __str__(self):
        return self.sql_title
    class Meta:
        verbose_name = u'数据库工单'
        verbose_name_plural = u"数据库工单"


class svn_workorder(models.Model):
    svn_title = models.CharField(max_length=100,verbose_name=u"工单标题")
    svn_name = models.CharField(max_length=100,verbose_name=u"SVN项目名")
    svn_memo = models.TextField(verbose_name=u"工单描述")
    svn_action_user = models.ManyToManyField(app01_models.User,verbose_name=u"处理人")
    svn_user = models.CharField(max_length=25,verbose_name=u"提交者")
    svn_time = models.DateTimeField(verbose_name=u"提交时间")
    svn_status = models.CharField(max_length=25,verbose_name=u"处理状态")
    svn_ret = models.TextField(verbose_name=u"处理办法和结果",blank=True,null=True)
    svn_create_pangu_choice = (
        ('on',u'是'),
        ('off',u'否'),
    )
    svn_create_pangu_status = models.CharField(max_length=10,choices=svn_create_pangu_choice,default='off',verbose_name=u'盘古是否创建对应',blank=True,null=True)
    domain_time = models.CharField(max_length=40,verbose_name=u'域名解析时间')

    def __str__(self):
        return self.svn_title
    class Meta:
        verbose_name = u'svn工单'
        verbose_name_plural = u"svn工单"


