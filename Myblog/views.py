# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from Myblog.models import *
from django.http import Http404,HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import re
from itertools import chain
import simplejson
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def show_welcome_page(request):
    return render_to_response('welcome.html')

def show_more_page(request):
    return render_to_response('more.html')

def show_about_page(request):
    return render_to_response('aboutme.html')

def show_home_page(request):
    return render_to_response('home.html')

def show_contact_page(request):
    return render_to_response('contact.html')

def show_cloud_page(request):
    return render_to_response('cloud.html')

def show_404_page(request):
    return render_to_response('404.html')

def blog_list(request):
    blog_list = Blog.objects.all().order_by('-publish_time')
    if request.GET.get('list_by') == 'read':
        blog_list = Blog.objects.all().order_by('-counts')
    elif request.GET.get('list_by') == 'classification':
        blog_list = Blog.objects.all().order_by('classification')

    paginator = Paginator(blog_list, 16)#分页处理
    page = request.GET.get('page')

    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)    
    return render_to_response('index.html', {"blogs": blogs}, context_instance=RequestContext(request))

# def blog_list_by_read(request):
#     blog_list = Blog.objects.all().order_by('-count')
#     paginator = Paginator(blog_list, 8)#分页处理
#     page = request.GET.get('page')

#     try:
#         blogs = paginator.page(page)
#     except PageNotAnInteger:
#         blogs = paginator.page(1)
#     except EmptyPage:
#         blogs = paginator.page(paginator.num_pages)    
#     return render_to_response('index.html', {"blogs": blogs}, context_instance=RequestContext(request))

@csrf_exempt

def blog_search(request):
    try:
        allblog = Blog.objects.all().order_by('caption')
        search_content = request.GET.get('search_content','')

        blogs = []
        for lookup in allblog:
            if search_content != '':
                tempCaption = lookup.caption
                tempContent = lookup.content
                matchCaption = re.search(search_content, tempCaption)
                matchContent = re.search(search_content, tempContent)
                if matchContent or matchCaption:
                    #blogs = Blog.objects.filter(caption = tempCaption)
                    blogs.append(Blog.objects.get(caption=tempCaption))  
        return render_to_response('index.html', {"blogs": blogs}, context_instance=RequestContext(request))          
    except:
        render_to_response('404.html', context_instance=RequestContext(request))
    # except Blog.DoesNotExit:
    #     raise Http404

    blogs = []
    return render_to_response('index.html', {"blogs": blogs, "blog_count":0}, context_instance=RequestContext(request))  

def blog_classify(request):
    allblog = Blog.objects.all().order_by('caption')
    if request.method == 'GET':
        try:
            classification = request.GET.get('classification','')
        #     tmp = classification.encode('UTF-8')
        #     print tmp
        #     tmp1 = tmp.decode('UTF-8')
        #     blogs = Blog.objects.filter(classification=tmp1)
            blogs = []
            for lookup in allblog:
                if classification != '':
                    tempClassification = str(lookup.classification)

                    if tempClassification == classification:
                        #blogs = Blog.objects.filter(caption = tempCaption)
                        blogs.append(lookup)
            return render_to_response('index.html', {"blogs": blogs}, context_instance=RequestContext(request))    
        except:
            render_to_response('404.html', context_instance=RequestContext(request))
    #except Blog.DoesNotExit:
    #    raise Http404

def blog_favor(request):
    id = request.GET.get('id','')

    try:
        blog = Blog.objects.get(id=id)
        blog.markCount = blog.markCount + 1     
        blog.save()
    
    except:
        render_to_response('404.html', context_instance=RequestContext(request))
        #raise Http404()
    return render_to_response("detail.html", {"blog": blog}, context_instance=RequestContext(request))
  

def blog_detail(request):
    if request.method == 'GET':
        id = request.GET.get('id','')
        try:
            blog = Blog.objects.get(id=id)
            readingCount = blog.counts+1
            blog.counts = readingCount
            blog.save()

        except Blog.DoesNotExist:
            raise Http404

        return render_to_response("detail.html", {"blog": blog}, context_instance=RequestContext(request))
    else:
        render_to_response('404.html', context_instance=RequestContext(request))
        #raise Http404


def tag(request,id=''):
    cut_tag = Tag.objects.gei(id=id)
    blogs = cut_tag.blog_set.all()
    tags = Tag.objects.all()
    classifications = Classification.objects.all()

    return render_to_response("blog_list.html", {"blogs":blogs, "classifications":classifications, "tags":tags})
