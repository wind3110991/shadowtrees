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

    url(r'^$', 'Myblog.views.show_welcome_page',name='welcome'),# 首页
    url(r'^home/', 'Myblog.views.show_home_page',name='home'), 
    url(r'^more/', 'Myblog.views.show_more_page',name='more'),
    url(r'^contact/', 'Myblog.views.show_contact_page',name='contact'),
    url(r'^about/','Myblog.views.show_about_page',name='contact'),#跳转到作者页面

    url(r'^blog/', 'Myblog.views.blog_list',name='blog_list'),
    url(r'^blog_favor/', 'Myblog.views.blog_favor',name='blog_favor'),
    url(r'^comments/',include('django.contrib.comments.urls')),
    url(r'^blog_search/$','Myblog.views.blog_search',name='blog_search'),
    url(r'^blog_classify/$','Myblog.views.blog_classify',name='blog_classify'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'media/'}), 
    #url(r'',hello),
 
)
