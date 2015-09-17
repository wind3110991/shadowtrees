# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import permalink
from markdown import markdown
# Create your models here.
class Classification(models.Model): # 分类表
    name = models.CharField(max_length=20)
 #   slug = models.CharField(max_length=50,unique=True)
    def __unicode__(self):
        return self.name

    #@permalink
    #def get_absolute_url(self):
    #    return ('blog_category', None, {'slug':self.slug})

    # class Meta:
    #     ordering = ['id']
   #     verbose_name_plural = verbose_name = u'分类'

class Tag(models.Model):# 标签表

    tag_name = models.CharField(max_length=20, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.tag_name

   # class Meta:
#        verbose_name_plural = verbose_name = u'标签'

class Author(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
            
    def __unicode__(self):
        return u'%s' % (self.name)

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    sex = models.CharField(max_length=4)
    donate = models.FloatField(max_length=10, default=0)
    email = models.EmailField(max_length=50)
    motto = models.CharField(max_length=200, default='')
    address = models.CharField(max_length=60, default='')
    headimg = models.CharField(max_length=200, default='')
    regist_time = models.DateTimeField(auto_now=True)
    msg_num = models.IntegerField(default=0)

class Article(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User)
    caption = models.CharField(max_length=50)
    mark_num = models.IntegerField(default=0)
    read_num = models.IntegerField(default=0)
    discuss_num = models.IntegerField(default=0)
    classification = models.CharField(max_length=10)
    update_time = models.DateTimeField(auto_now=True)
    content = models.TextField()

class Message(models.Model):
    id = models.IntegerField(primary_key=True)
    sender = models.ForeignKey(User, related_name='senders')
    receiver = models.ForeignKey(User, related_name='receivers')
    recv_msg = models.CharField(max_length=50)
    send_msg = models.CharField(max_length=50)
    update_time = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(Article)
    state = models.IntegerField(default=1)
    operation = models.IntegerField()

class Blog(models.Model): # 文章表
    caption = models.CharField(max_length=50)
    subcaption = models.CharField(max_length=50, blank=True)
    markCount = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag,blank=True)
    content = models.TextField()
    publish_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    counts = models.IntegerField(default=0)
    author = models.ForeignKey(Author)
    classification = models.ForeignKey(Classification)

    # def __unicode__(self):
    #     return u'%s %s' % (self.caption,self.publish_time,self.classification)

    @permalink
    def get_absolute_url(self):
        return ('blog_article',None,{'slug':self.slug})

    class Meta:
        get_latest_by = 'publish_time'
        ordering = ['-id']#按照后输入的id号排在前面
 #       verbose_name_plural = verbose_name = u'文章'

#class ClientInfo(models.Model):

#    ip_address = models.CharField(max_length=20)
#    time = models.DateTimeField(auto_now=True)

#    def __unicode__(self):
#        return u'%s %s' % (self.ip_address,self.time)

#    class Meta:
  #      get_latest_by = 'time'
 #       ordering = ['-id']
#        verbose_name_plural = verbose_name = u'访问时间'