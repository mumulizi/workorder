"""svnmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from workorder import views


urlpatterns = [
    url(r'^$',views.index,name='workindex'),
    url(r'^resolve/(?P<obj_id>[^/]+)$',views.resolve,name='resolve'),
    url(r'^workorder_post/(?P<obj_id>[^/]+)$',views.workorder_post,name='workorder_post'),
    url(r'^web_workorder',views.web_workorder,name='web_workorder'),
    url(r'^database_workorder',views.database_workorder,name='database_workorder'),
    url(r'^svn_workorder',views.svn_workorder,name='svn_workorder'),
    url(r'^permission_workorder',views.permission_workorder,name='permission_workorder'),
    url(r'^change_conf_workorder',views.change_conf_workorder,name='change_conf_workorder'),

]
