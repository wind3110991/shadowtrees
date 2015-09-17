# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from Myblog.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^t/$', 'Myblog.views.blog_detail',name='blog_detail'),
    url(r'^a/$', 'Myblog.views.article_detail',name='article_detail'),

    url(r'^$', 'Myblog.views.show_welcome_page',name='welcome'),# 首页
    url(r'^home/', 'Myblog.views.show_home_page',name='home'), 
    url(r'^more/', 'Myblog.views.show_more_page',name='more'),
    url(r'^timestamp/', 'Myblog.views.show_timestamp_page',name='timestamp'),
    url(r'^about/','Myblog.views.show_about_page',name='contact'),#跳转到作者页面

    url(r'^cloud/', 'Myblog.views.show_cloud_page',name='cloud'),
    url(r'^product/', 'Myblog.views.show_product_page',name='product'),

    url(r'^login/', 'Myblog.views.login',name='login'),
    url(r'^logout/', 'Myblog.views.logout',name='logout'),

    url(r'^signup/', 'Myblog.views.signup',name='signup'),
    url(r'^modify/', 'Myblog.views.modify',name='modify'),
    url(r'^favor/', 'Myblog.views.favor',name='favor'),
    url(r'^write/', 'Myblog.views.write',name='write'),
    url(r'^test/', 'Myblog.views.test',name='test'),
    url(r'^user_page/', 'Myblog.views.user_page',name='user_page'),
    url(r'^msg/', 'Myblog.views.msg',name='msg'),
    url(r'^u/', 'Myblog.views.my_article',name='my_article'),

    url(r'^404/', 'Myblog.views.show_404_page',name='404'),
    url(r'^blog/', 'Myblog.views.blog_list',name='blog_list'),
    url(r'^bbs/', 'Myblog.views.bbs_list',name='bbs_list'),
    url(r'^blog_favor/', 'Myblog.views.blog_favor',name='blog_favor'),
    url(r'^comments/',include('django.contrib.comments.urls')),
    url(r'^blog_search/$','Myblog.views.blog_search',name='blog_search'),
    url(r'^blog_classify/$','Myblog.views.blog_classify',name='blog_classify'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'media/'}), 
    #url(r'',hello),
 
)
