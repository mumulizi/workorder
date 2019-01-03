#!/usr/bin/env python
#_*_coding:utf-8_*_
#__author__="lihongxing"


from django.shortcuts import render,HttpResponse
from workorder import models
from django.db.models import Q
from app01 import models as app01models
from assets import models as asset_models
from controller import sedmail
from workorder.workorder_permission import check_online_permission
import user_group
import time
from workorder.utils import Auto_Create_WebSvn

from  app01.views import login_required
@login_required(login_url='/login/')
def index(request):
    if request.method =="POST":
        search = request.POST.get("search",'null')
        #模糊查询
        qset = (
        Q(mywork_title__contains = search) |
        Q(mywork_memo__contains = search) |
        Q(mywork_user__contains = search) |
        Q(mywork_ret__contains = search) |
        Q(mywork_status__contains = search) )
        workorder_obj= models.mywork.objects.filter(qset)
        print "-------->>>workorder_obj:",workorder_obj
        return render(request,'workorder/index.html',{'title':workorder_obj})

    else:
        workorder_obj = models.mywork.objects.all()
        # print(workorder_obj)
        # for obj in workorder_obj:
        #     server_host_name = obj.mywork_server_ip.select_related()
        #     # for onehost in server_host_name:
        #     # print(server_host_name)
        # if request.user.username in user_group.admin:
        #     user = 'admin'
        # else:
        #     user = 'False'
        return render(request,'workorder/index.html',{
            # 'u':user,
             'title':workorder_obj
        }
                      )

#处理工单主页
@login_required(login_url='/login/')
@check_online_permission
def resolve(request,obj_id):
    info = models.mywork.objects.get(id = obj_id)
    true_id = info.other_id
    type = info.mywork_type
    admins = user_group.admin
    if type =='web':
        web_info = models.web_workorder.objects.get(id = true_id)
        title = web_info.web_title
        name = web_info.web_name
        path = web_info.web_path
        memo = web_info.web_memo
        svn_status = web_info.web_create_svn_status
        cdn_status = web_info.web_create_cdn_status
        https_status = web_info.web_create_https_status
        domainTime = web_info.domain_time
        ret = web_info.web_ret
        return  render(request,'workorder/web_resolve.html',{'obj_id':obj_id,'admins':admins,
                                                     'title':title,'name':name,'path':path,'memo':memo,
                                                      'svn_status':svn_status,"https_status":https_status,
                                                      "cdn_status":cdn_status,'domainTime':domainTime,  'ret':ret})
    if type =='svn':
        svn_info = models.svn_workorder.objects.get(id = true_id)
        title = svn_info.svn_title
        name = svn_info.svn_name
        memo = svn_info.svn_memo
        pangu = svn_info.svn_create_pangu_status
        svn_domain_Time = svn_info.domain_time
        svn_ret = svn_info.svn_ret
        return render(request,'workorder/svn_resolve.html',{'obj_id':obj_id,'admins':admins,
            'title':title,'name':name,'memo':memo,
            'pangu':pangu,'svn_domain_Time':svn_domain_Time,
            'ret':svn_ret
        })
    if type =='sql':
        sql_info = models.data_workorder.objects.get(id = true_id)
        title = sql_info.sql_title
        name = sql_info.sql_name
        memo = sql_info.sql_memo
        #获取choice里的值，在前段显示中文
        status = sql_info.get_sql_action_status_display()

        sql_ret = sql_info.sql_ret
        return render(request,'workorder/sql_resolve.html',{'obj_id':obj_id,'admins':admins,
            'title':title,'name':name,'memo':memo,
            'status':status,
            'ret':sql_ret
        })

#admin 处理工单操作
@login_required(login_url='/login/')
@check_online_permission
def workorder_post(request,obj_id):
    if request.POST.get("ret") != '':
        # info = models.mywork.objects.get(id = obj_id)
        ret = request.POST.get("ret")
        info = models.mywork.objects.get(id=obj_id)
        web_user  = info.mywork_user
        web_title = info.mywork_title
        action_type = request.POST.get("status_choice")
        models.mywork.objects.filter(id=obj_id).update(mywork_status = action_type)
        models.mywork.objects.filter(id=obj_id).update(mywork_ret=ret)

        #更新web svn表
        true_id = info.other_id
        type = info.mywork_type

        login_pangu_user = str(request.user.username)
        pangu_admin_usergroup = user_group.admin

        if type == 'web':
            models.web_workorder.objects.filter(id=true_id).update(web_status = action_type)
            models.web_workorder.objects.filter(id=true_id).update(web_ret=ret)
            web_value = models.web_workorder.objects.get(id = true_id)
            web_svn_value = web_value.web_create_svn_status
            web_name_value = web_value.web_name
            web_user_value = web_value.web_user
            # 添加自动执行的步骤，如审核通过自动创建svn
            if web_svn_value == "on" and login_pangu_user in pangu_admin_usergroup:
                Auto_Create_WebSvn.create_mysvn(web_name_value,web_user_value,svn_rw="rw")
                os.system("mkdir /alidata/www/%s" %(web_name_value))
                os.system("touch /alidata/rsync_exclude_file/%s" %(web_name_value))
                os.system('echo ".svn/" /alidata/rsync_exclude_file/%s' %(web_name_value))

                print("成功创建，svn和web项目...")
        elif type =='svn':
            models.svn_workorder.objects.filter(id=true_id).update(svn_status = action_type)
            models.svn_workorder.objects.filter(id=true_id).update(svn_ret=ret)
        elif type =='sql':
            models.data_workorder.objects.filter(id=true_id).update(sql_status = action_type)
            models.data_workorder.objects.filter(id=true_id).update(sql_ret=ret)


        # 处理完工单后回复邮件
        try:
            if action_type ==u'已驳回':
                sedmail.pangu_reply(web_user,obj_id,web_title,ret,action_type)
                print(u"驳回成功 send mail success")
            if action_type ==u'已同意':
                to_user_list = user_group.admin
                to_user_list.append(web_user)
                for i in to_user_list:
                    sedmail.pangu_reply(i,obj_id,web_title,ret,action_type)
            if action_type ==u'已处理':
                user_lists = user_group.approvel
                user_lists.append(web_user)

                for user_list in user_lists:
                    sedmail.pangu_reply(user_list,obj_id,web_title,ret,action_type)
        except:
            print(u"工单回复的时候发生失败，可能用户不存在")
        return HttpResponse("save ok")
    else:
        return HttpResponse(u"处理结果为空")


@login_required(login_url='/login/')
def web_workorder(request):
    if request.method =="POST":
        print(request.POST)
        # web_host = request.POST.getlist('host') #获取前端提交的多台主机  getlist
        # print("webbhost:",web_host)
        # web_type = request.POST.get('type')
        # web_feature = request.POST.get('feature')
        web_title = request.POST.get('title')
        web_name = request.POST.get('pro_name')
        web_path = request.POST.get('pro_path')
        web_memo = request.POST.get('memo')
        web_action_user = request.POST.getlist('check_box_list')
        web_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        web_mywork_user = request.user.username
        web_svn = request.POST.get('svn_yes')
        web_cdn = request.POST.get('cdn_yes')
        web_https = request.POST.get('https_yes')
        domain_web_time = request.POST.get('time')


        #增加新数据
        new_mywork = models.web_workorder(
            # mywork_type=web_type,mywork_feature=web_feature,
            web_title=web_title,
            web_name = web_name,
            web_path = web_path,
            web_memo=web_memo,
            web_date=web_time,
            # web_action_user=web_action_user,
            web_user=web_mywork_user,
            web_status= u'待处理',
            web_create_svn_status = web_svn,
            web_create_cdn_status = web_cdn,
            web_create_https_status = web_https,
            domain_time = domain_web_time
        )

        new_mywork.save()

        other_mywork = models.mywork(
            mywork_title=web_title,
            mywork_type='web',
            other_id =models.web_workorder.objects.get(web_title=web_title).id,
            mywork_memo = web_memo,
            mywork_date=web_time,
            # web_action_user=web_action_user,
            mywork_user=web_mywork_user,
            mywork_status= u'待处理',

        )

        other_mywork.save()

        #new_mywork.mywork_server_ip.add(*web_host) 报错
        #多对多的关联查询 然后插入list   .add()里的东西是数字   切是manyTomany的关系
        #错误提示invalid literal for int() with base 10 django    或者   before a many-to-many relationship can be used
        host_ids = []
        # for h in web_host:
        #     host_id =asset_models.Server.objects.get(host_name=h).id
        #     # print(host_id)
        #     host_ids.append(host_id)

        user_ids = []
        for w_user in web_action_user:
            #处理工单 发送邮件
            try:
                sedmail.pangu_sendmail(w_user,
                                       web_mywork_user,
                                       # web_feature,
                                       web_title,
                                       web_memo)
            except:
                print(u"%s邮件发送失败" %(w_user))

            #获取用户 在前端展示checkbox
            u_id = app01models.User.objects.get(username=w_user).id
            user_ids.append(u_id)
        #保存选中的服务器和提交的用户，多对多的关系，所以得.add添加
        # new_mywork.mywork_server_ip.add(*host_ids)
        new_mywork.web_action_user.add(*user_ids)
        other_mywork.mywork_action_user.add(*user_ids)

        # print("webHost:",web_host,web_type,web_mywork_user,web_action_user)

        return HttpResponse(" add save ok")
    # info_user = app01models.User.objects.all()
    approve_users = user_group.approvel
    return render(request, 'workorder/web_workorder.html',{
        'approve_users':approve_users,
        # "users":info_user
    })


@login_required(login_url='/login/')
def database_workorder(request):
    if request.method =="POST":
        # print(request.POST)
        sql_title_value = request.POST.get("title")
        sql_name_value = request.POST.get("sql_name")
        sql_action_value = request.POST.get("sql_action")
        sql_memo_value = request.POST.get("memo")
        sql_time_value = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql_action_user = request.POST.getlist('check_box_list')
        sql_mywork_user = request.user.username
        print(sql_action_value,sql_memo_value,sql_name_value,sql_title_value)


        #增加新数据
        new_sql_mywork = models.data_workorder(
            sql_title=sql_title_value,
            sql_name = sql_name_value,
            sql_memo=sql_memo_value,
            sql_status= u'待处理',
            sql_user = request.user.username,
            sql_date = sql_time_value,
            sql_action_status = sql_action_value,
        )
        new_sql_mywork.save()

        #总表增加数据
        other_mywork = models.mywork(
            mywork_title=sql_title_value,
            mywork_type='sql',
            other_id =models.data_workorder.objects.get(sql_title=sql_title_value).id,
            mywork_memo = sql_memo_value,
            mywork_date=sql_time_value,
            mywork_user=request.user.username,
            mywork_status= u'待处理',
        )

        other_mywork.save()



        user_ids = []
        for w_user in sql_action_user:
            #处理工单 发送邮件
            try:
                sedmail.pangu_sendmail(w_user,
                                       sql_mywork_user,
                                       # web_feature,
                                       sql_title_value,
                                       sql_memo_value)
            except:
                print(u"%s邮件发送失败" %(w_user))

            #获取用户 在前端展示checkbox
            u_id = app01models.User.objects.get(username=w_user).id
            user_ids.append(u_id)
        #保存选中的服务器和提交的用户，多对多的关系，所以得.add添加
        # new_mywork.mywork_server_ip.add(*host_ids)
        new_sql_mywork.sql_action_user.add(*user_ids)
        other_mywork.mywork_action_user.add(*user_ids)

        # print("webHost:",web_host,web_type,web_mywork_user,web_action_user)

        return HttpResponse(" add save ok")

    approve_users = user_group.approvel

    return render(request,'workorder/database_workorder.html',{'approve_users':approve_users,})



@login_required(login_url='/login/')
def svn_workorder(request):
    if request.method =="POST":
        print(request.POST)
        svn_title = request.POST.get('title')
        svn_name = request.POST.get('pro_name')
        svn_memo = request.POST.get('memo')
        svn_action_user = request.POST.getlist('check_box_list')
        svn_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        svn_get_user = request.user.username
        svn_pangu = request.POST.get('svn_yes')
        domain_web_time = request.POST.get('time')


        #增加新数据
        svn_new_mywork = models.svn_workorder(
            svn_title=svn_title,
            svn_name = svn_name,
            svn_memo=svn_memo,
            svn_time=svn_time,
            svn_user=request.user.username,
            svn_status= u'待处理',
            svn_create_pangu_status = svn_pangu,
            domain_time = domain_web_time
        )

        svn_new_mywork.save()

        other_mywork = models.mywork(
            mywork_title=svn_title,
            mywork_type='svn',
            mywork_user = request.user.username,
            other_id =models.svn_workorder.objects.get(svn_title=svn_title).id,
            mywork_memo = svn_memo,
            mywork_date=svn_time,
            mywork_status= u'待处理',

        )
        other_mywork.save()
        user_ids = []
        for w_user in svn_action_user:
            #处理工单 发送邮件
            try:
                sedmail.pangu_sendmail(w_user,
                                       svn_get_user,
                                       # web_feature,
                                       svn_title,
                                       svn_memo)
            except:
                print(u"%s邮件发送失败" %(w_user))
            #获取用户 在前端展示checkbox
            u_id = app01models.User.objects.get(username=w_user).id
            user_ids.append(u_id)
        svn_new_mywork.svn_action_user.add(*user_ids)
        other_mywork.mywork_action_user.add(*user_ids)
        return HttpResponse(" add save ok")
    # info_user = app01models.User.objects.all()
    approve_users = user_group.approvel

    return render(request, 'workorder/svn_workorder.html',{
        'approve_users':approve_users,
    })





@login_required(login_url='/login/')
def permission_workorder(request):
    info_user = app01models.User.objects.all()
    return render(request,'workorder/permission_workorder.html',{'users':info_user})

@login_required(login_url='/login/')
def change_conf_workorder(request):
    info_user = app01models.User.objects.all()
    return render(request,'workorder/change_conf_file_workorder.html',{'users':info_user})
