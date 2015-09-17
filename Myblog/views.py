# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from Myblog.models import *
from django.http import Http404,HttpResponse, HttpResponseRedirect
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

def show_timestamp_page(request):
    return render_to_response('timestamp.html')

def show_cloud_page(request):
    return render_to_response('cloud.html')

def show_product_page(request):
    return render_to_response('product.html')    

def show_404_page(request):
    return render_to_response('404.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        try:
            login_user = 1
            user = User.objects.get(username=username)
            if user and password == user.password:

                json = {"state":0 ,"username": username, "login_user":login_user,
                 "message": "登录成功！5秒后将自动跳转，欢迎您回家！"}
                JsonData = simplejson.dumps(json, ensure_ascii=False)
                response = HttpResponse(JsonData)
                response.set_cookie('login_user', value=username)
            else:
                json = {"state": 4, "message": "密码错误！"}
                JsonData = simplejson.dumps(json, ensure_ascii=False)
                response = HttpResponse(JsonData)
            return response

        except:
            json = {"state": 3, "message": "用户名不存在！"}
            JsonData = simplejson.dumps(json, ensure_ascii=False)
            response = HttpResponse(JsonData)
            return response

@csrf_exempt
def logout(request):
    if request.method == 'GET':
        response = HttpResponseRedirect('/bbs/', {"message":"已登出"})
        response.delete_cookie("login_user")
        return response


def checkLegal(text):
    m = re.match(r'^[A-Za-z0-9_]{6,14}$', text)
    return m

@csrf_exempt
def signup(request):
    if request.method == 'GET':
        all_user = User.objects.all()
        u_list = []
        for i in all_user:
            u_list.append({ "username":i.username })

        return render_to_response('signup.html', {'lists':u_list}, context_instance=RequestContext(request))

    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        sex = request.POST.get('sex', '')
        email = request.POST.get('email', '')
        headimg = '/static/img/owner.jpg'

        is_user_exit = User.objects.filter(username=username)
        is_email_exit = User.objects.filter(email=email)

        if is_user_exit:
            response = render_to_response('signup.html',{"state": 1, "message": "用户名已存在！"}, context_instance=RequestContext(request))
        
        elif is_email_exit:
            response = render_to_response('signup.html',{"state": 2, "message": "邮箱已被注册"}, context_instance=RequestContext(request))

        else:
            if checkLegal(username) and checkLegal(password) and password != '':
                user = User(username=username, password=password, sex=sex, donate=0, email=email, headimg=headimg)
                user.save()
                response = render_to_response('signup.html', {"state": 0, "message": "注册成功，5秒后将自动跳转，请登录"}, context_instance=RequestContext(request)) 
            
            else:
                response = render_to_response('signup.html', {"state": 3, "message": "密码或用户名不合法，请不要用特殊字符，密码在6到14位"}, context_instance=RequestContext(request))
        
        return response

@csrf_exempt
def modify(request):
    if request.method == 'POST':
        try:
            login_user = request.COOKIES["login_user"]
            user = User.objects.get(username=login_user)
        
            motto = request.POST.get('motto','')
            address = request.POST.get('address','')
            password = request.POST.get('password','')
            new_password = request.POST.get('new_password','')
            headimg = request.POST.get('headimg','')
            print headimg
            if motto:
                user.motto = motto
                user.save(update_fields=['motto'])

            if address:   
                user.address = address
                user.save(update_fields=['address'])

            if headimg:
                user.headimg = headimg
                user.save(update_fields=['headimg'])

            if password:
                if password == user.password:
                    if checkLegal(new_password) and new_password != '':
                        user.password = new_password
                        user.save(update_fields=['password'])
                        json = {"state":0, "message": "修改成功"}
                        JsonData = simplejson.dumps(json, ensure_ascii=False)
                        response = HttpResponse(JsonData)
                        #保存所有修改
                        return response
                else:
                    json = {"state": 4, "message": "输入原密码错误！"}
                    JsonData = simplejson.dumps(json, ensure_ascii=False)
                    response = HttpResponse(JsonData)
                    return response

            json = {"state":0, "message": "修改成功"}
            JsonData = simplejson.dumps(json, ensure_ascii=False)      
            response = HttpResponse(JsonData)
            return response

        except:
            response = render_to_response('404.html', context_instance=RequestContext(request))


def msg(request):
    if request.method == 'GET':
        username = request.COOKIES["login_user"]
        user = User.objects.get(username=username)
            #点开消息盒子，通知清零
        user.msg_num = 0
        user.save(update_fields=['msg_num'])

        msgs = Message.objects.filter(receiver=user).order_by('-update_time')

        response = render_to_response('msg.html', {"user": user, "msgs": msgs}, context_instance=RequestContext(request))
        return response
        # try:
        #     username = request.COOKIES["login_user"]
        #     user = User.objects.get(username=username)
        #     #点开消息盒子，通知清零
        #     user.msg_num = 0
        #     user.save(update_fields=['msg_num'])

        #     msgs = Message.objects.filter(receiver=user)

        #     response = render_to_response('msg.html', {"user": user, "msgs": msgs}, context_instance=RequestContext(request))
        #     return response
        # except:
        #     return render_to_response('404.html', context_instance=RequestContext(request))

def my_article(request):
    if request.method == 'GET':
        try:
            username = request.GET.get('username','')
            author = User.objects.get(username=username)

            us = request.COOKIES["login_user"]
            user = User.objects.get(username=us)

            articles = Article.objects.filter(user=author).order_by('-update_time')

            msgs = Message.objects.filter(sender=user).order_by('-update_time')

            response = render_to_response('article.html', {"msgs":msgs, "author": author, "user":user, "articles":articles}, context_instance=RequestContext(request))
            return response
        except:
            return render_to_response('404.html', context_instance=RequestContext(request))

def article_detail(request):
    if request.method == 'GET':
        id = request.GET.get('id','')

        try:
            username = request.COOKIES["login_user"]
            user = User.objects.get(username=username)
            article = Article.objects.get(id=id)
            article.read_num += 1
            article.save(update_fields=['read_num'])
            response = render_to_response('article_detail.html', {"user":user, "article":article}, context_instance=RequestContext(request))
        
        except:
            article = Article.objects.get(id=id)
            article.read_num += 1
            article.save(update_fields=['read_num'])
            response = render_to_response('article_detail.html', {"article":article}, context_instance=RequestContext(request))
        return response

@csrf_exempt
def favor(request):
    if request.method == 'POST':
        article_id = request.POST.get('id','')
        # username = request.COOKIES["login_user"]
        
        # user = User.objects.get(username=username)
        # article = Article.objects.get(id=article_id)
        # #operation为1默认为赞操作
        # msgs = Message.objects.filter(article=article).filter(operation=1).filter(sender=user)

        # if msgs:
        #     #已经赞过了
        #     json = {"state": 1, "message": "你已经赞过这篇文章了哦"}
        #     JsonData = simplejson.dumps(json, ensure_ascii=False)
        #     response = HttpResponse(JsonData)
        # else:
        #     article.mark_num += 1
        #     article.save(update_fields=['mark_num'])
        #     send_message(request,1)

        #     json = {"state": 0, "message": "点赞！"}
        #     JsonData = simplejson.dumps(json, ensure_ascii=False)
        #     response = HttpResponse(JsonData)
        # return response

        try:
            username = request.COOKIES["login_user"]
            user = User.objects.get(username=username)
            article = Article.objects.get(id=article_id)
            #operation为1默认为赞操作
            msgs = Message.objects.filter(article=article).filter(operation=1).filter(sender=user)

            if msgs:
                #已经赞过了
                json = {"state": 1, "message": "你已经赞过这篇文章了哦"}
                JsonData = simplejson.dumps(json, ensure_ascii=False)
                response = HttpResponse(JsonData)
                return response

            else:
                article.mark_num += 1
                article.save(update_fields=['mark_num'])
                
                if send_message(request,1) == 0:
                    json = {"state": 0, "message": "点赞！么么哒"}
                    JsonData = simplejson.dumps(json, ensure_ascii=False)
                    response = HttpResponse(JsonData)

                else:
                    json = {"state": 3, "message": "系统故障"}
                    JsonData = simplejson.dumps(json, ensure_ascii=False)
                    response = HttpResponse(JsonData)
                return response
        
        except:
            #提示未登录
            json = {"state": 2, "message": "请先登录哦~"}
            JsonData = simplejson.dumps(json, ensure_ascii=False)
            response = HttpResponse(JsonData)
        return response

def send_message(request,operation):
    # recv_msg = ''
    # send_msg = ''
    # sendername = request.COOKIES["login_user"]
    # sender = User.objects.get(username=sendername)

    # article_id = request.GET.get('id', '')
    # article = Article.objects.get(id=article_id)

    # receiver = article.user
    # receiver.msg_num += 1
    # receiver.save(update_fields=['msg_num'])

    # if operation == 1:
    #     recv_msg = '%s 赞了你的文章 《%s》' % (sender.username , article.caption)
    #     send_msg = '你赞了 %s 的文章 《%s》' % (receiver.username , article.caption)
        
    # elif operation == 0:
    #     recv_msg = '%s 评论了你的文章 《%s》' % (sender.username , article.caption)
    #     send_msg = '你评论了 %s 的文章 《%s》' % (receiver.username , article.caption)

    # elif operation == 2:
    #     recv_msg = '%s 收藏了你的文章 《%s》' % (sender.username , article.caption)
    #     send_msg = '你收藏了 %s 的文章 《%s》' % (receiver.username , article.caption)
        
    # msg = Message(article=article, sender=sender, receiver=receiver, send_msg=send_msg, recv_msg=recv_msg, 
    # operation=operation, state=1) #未读消息状态是1
    # msg.save()
    try:
        recv_msg = ''
        send_msg = ''
        sendername = request.COOKIES["login_user"]
        sender = User.objects.get(username=sendername)

        article_id = request.POST.get('id', '')
        article = Article.objects.get(id=article_id)

        receiver = article.user
        receiver.msg_num += 1
        receiver.save(update_fields=['msg_num'])

        if operation == 1:
            recv_msg = '%s 赞了你的文章 《%s》' % (sender.username , article.caption)
            send_msg = '你赞了 %s 的文章 《%s》' % (receiver.username , article.caption)
        
        elif operation == 0:
            recv_msg = '%s 评论了你的文章 《%s》' % (sender.username , article.caption)
            send_msg = '你评论了 %s 的文章 《%s》' % (receiver.username , article.caption)

        elif operation == 2:
            recv_msg = '%s 收藏了你的文章 《%s》' % (sender.username , article.caption)
            send_msg = '你收藏了 %s 的文章 《%s》' % (receiver.username , article.caption)
        
        msg = Message(article=article, sender=sender, receiver=receiver, send_msg=send_msg, recv_msg=recv_msg,
         operation=operation, state=1) #未读消息状态是1
        msg.save()
        return 0

    except:
        print "send error"
        return 1
        

@csrf_exempt
def write(request):
    if request.method == 'GET':
        try:
            username = request.COOKIES["login_user"]
            user = User.objects.get(username=username)

            response = render_to_response('write.html', {"user": user}, context_instance=RequestContext(request))
            return response
        except:
            render_to_response('404.html', context_instance=RequestContext(request))

    elif request.method == 'POST':
        username = request.COOKIES["login_user"]
        user = User.objects.get(username=username)

        caption = request.POST.get('caption', '')
        content = request.POST.get('content', '')
        classification = request.POST.get('classification', '')

        new_article = Article(caption=caption, content=content, classification=classification, user=user)
        new_article.save()

        #recv_msg = '??'
        #send_msg = '%s 创建了新文章 《%s》' % (username, caption)

        #superadmin =  User.objects.get(id=0)
        #msg = Message(article=new_article, sender=user, receiver=superadmin, send_msg=send_msg, recv_msg=recv_msg,
        # operation=3, state=1)
        #msg.save()

        # response = render_to_response('write.html', {"state": 0, "message": "发布成功！", "user": user}, context_instance=RequestContext(request))
        # return response
        json = {"state": 0, "message": "发布成功！"}
        JsonData = simplejson.dumps(json, ensure_ascii=False)
        response = HttpResponse(JsonData)
        return response

    else:
        json = {"state": 2, "message": "发布失败，请重试！"}
        JsonData = simplejson.dumps(json, ensure_ascii=False)
        response = HttpResponse(JsonData)
        return response

@csrf_exempt
def test(request):
    if request.method == 'POST':
        username = request.COOKIES["login_user"]
        user = User.objects.get(username=username)

        caption = request.POST.get('caption', '')
        content = request.POST.get('content', '')
        classification = request.POST.get('classification', '')
        print username,caption,content,classification
       
        new_article = Article(caption=caption, content=content, classification=classification,
         user=user, discuss_num=0, read_num=0,mark_num=0)
        print "sad"
        new_article.save()

        recv_msg = '%s 创建了新文章 《%s》' % (username, caption)
        send_msg = ''

        msg = Message(article=new_article, sender=None, receiver=user, send_msg=send_msg, recv_msg=recv_msg,
         operation=3, state=1)
        msg.save()

        json = {"state": 0, "message": "发布成功！"}
        JsonData = simplejson.dumps(json, ensure_ascii=False)
        response = HttpResponse(JsonData)
        return response

def user_page(request):
    if request.method == 'GET':
        try:
            username = request.COOKIES["login_user"]

            user = User.objects.get(username=username)
            blogs = show_airticle(request)

            response = render_to_response('userpage.html', {"user": user}, context_instance=RequestContext(request))
        except:
            response = render_to_response('userpage.html', context_instance=RequestContext(request))
        return response

def bbs_list(request):
    articles = show_airticle(request)
    try:
        login_user = request.COOKIES["login_user"]
        user = User.objects.get(username=login_user)

        return render_to_response('bbs.html', {"user":user, "articles": articles}, context_instance=RequestContext(request))
    except:
        return render_to_response('bbs.html', {"articles": articles}, context_instance=RequestContext(request))

        
def show_airticle(request):
    article_list = Article.objects.all().order_by('-update_time')
    if request.GET.get('list_by') == 'read':
        article_list = Article.objects.all().order_by('-counts')

    elif request.GET.get('list_by') == 'classification':
        article_list = Article.objects.all().order_by('classification')

    paginator = Paginator(article_list, 20)#分页处理
    page = request.GET.get('page')

    try:
        articles = paginator.page(page)

    except PageNotAnInteger:
        articles = paginator.page(1)

    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    return articles


def blog_list(request):
    try:
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
    
    except:
        render_to_response('404.html', context_instance=RequestContext(request))


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
            alluser = User.objects.all()
            readingCount = blog.counts + 1
            blog.counts = readingCount
            blog.save()

        except Blog.DoesNotExist:
            raise Http404

        return render_to_response("detail.html", {"blog": blog, "alluser":alluser}, context_instance=RequestContext(request))
    else:
        render_to_response('404.html', context_instance=RequestContext(request))
        #raise Http404


def tag(request,id=''):
    cut_tag = Tag.objects.gei(id=id)
    blogs = cut_tag.blog_set.all()
    tags = Tag.objects.all()
    classifications = Classification.objects.all()

    return render_to_response("blog_list.html", {"blogs":blogs, "classifications":classifications, "tags":tags})
