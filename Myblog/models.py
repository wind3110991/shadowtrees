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

    @permalink
    def get_absolute_url(self):
        return ('blog_category',None,{'slug':self.slug})

    class Meta:
        ordering = ['id']
   #     verbose_name_plural = verbose_name = u'分类'

class Tag(models.Model): # 标签表

    tag_name = models.CharField(max_length=20,blank=True)
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

class Blog(models.Model): # 文章表
    caption = models.CharField(max_length=50)
    subcaption = models.CharField(max_length=50, blank=True)
    markCount = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag,blank=True)
    content = models.TextField()
    publish_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    counts = models.IntegerField(default=0)
    author=models.ForeignKey(Author)
    classification = models.ForeignKey(Classification)

#    def __unicode__(self):
 #       return u'%s %s' % (self.caption,self.publish_time)

#    @permalink
#    def get_absolute_url(self):
 #       return ('blog_article',None,{'slug':self.slug})

    class Meta:
        get_latest_by = 'publish_time'
        ordering = ['-id'] #按照后输入的id号排在前面
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