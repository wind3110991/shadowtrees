# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from Myblog.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog_detail/$', 'Myblog.views.blog_detail',name='blog_detail'),
    url(r'^$', 'Myblog.views.welcome',name='welcome'),# 首页
    url(r'^home/', 'Myblog.views.home',name='home'), 
    url(r'^more/', 'Myblog.views.more',name='more'),
    url(r'^blog/', 'Myblog.views.blog_list',name='blog_list'),
    url(r'^blog_favor/', 'Myblog.views.blog_favor',name='blog_favor'),
    url(r'^about/','Myblog.views.about',name='about'),#跳转到作者页面
    url(r'^comments/',include('django.contrib.comments.urls')),
    url(r'^blog_search/$','Myblog.views.blog_search',name='blog_search'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'media/'}), 
    #url(r'',hello),
 
)
