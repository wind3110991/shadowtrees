# -*- coding: utf-8 -*-
from django.contrib import admin
from Myblog.models import *
            
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'website')
    search_fields = ('name',)
            
class BlogAdmin(admin.ModelAdmin):
    list_display = ('caption','subcaption','author','classification','publish_time', 'update_time')
    list_filter = ('publish_time',)
    date_hierarchy = 'publish_time'
    ordering = ('-publish_time',)
    filter_horizontal = ('tags',)

    class Media:  
        js = ('/static/tinymce/tinymce.min.js', '/static/tinymce/textareas.js')
            
admin.site.register(Blog, BlogAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag)
admin.site.register(Classification)
# Register your models here.
