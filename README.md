# shadowtrees
www.shadowtrees.com

基于python的Django框架做的博客系统shadowtrees，大家可以登陆我的网站：

http://www.shadowtrees.com/

前端使用用了bootstap框架优化，以及css3技术

后台服务器语言为python

部署方案:SAE

参照SAE 文档中心 v1.0

（Django）

目前SAE上预置了多个版本的Django，默认的版本为1.2.7，在本示例中我们使用1.4版本。

创建一个新的Python应用，检出SVN代码到本地目录并切换到应用目录。

创建一个Django project：mysite。

jaime@westeros:~/pythondemo$ django-admin.py startproject mysite
jaime@westeros:~/pythondemo$ ls mysite
manage.py  mysite/
重命名该project的根目录名为1，作为该应用的默认版本代码目录。

jaime@westeros:~/pythondemo$ mv mysite 1
在默认版本目录下创建应用配置文件 config.yaml ，在其中添加如下内容：

libraries:
- name: "django"
  version: "1.4"
创建文件index.wsgi，内容如下

```python
import sae
from mysite import wsgi

application = sae.create_wsgi_app(wsgi.application)
最终目录结构如下

jaime@westeros:~/pythondemo$ ls 1
config.yaml index.wsgi manage.py mysite/
jaime@westeros:~/pythondemo/1$ ls 1/mysite
__init__.py settings.py  urls.py  views.py
```

部署代码，访问 http://<your-application-name>.sinaapp.com ，就可看到Django的欢迎页面了。

完整示例 （ django tutorial 中的poll、choice程序）

django-1.2.7示例

处理用户上传文件

在setttings.py中添加以下配置。

# 修改上传时文件在内存中可以存放的最大size为10m
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

# sae的本地文件系统是只读的，修改django的file storage backend为Storage
DEFAULT_FILE_STORAGE = 'sae.ext.django.storage.backend.Storage'
# 使用media这个bucket
STORAGE_BUCKET_NAME = 'media'
# ref: https://docs.djangoproject.com/en/dev/topics/files/
发送邮件

在settings.py中添加以下配置，即可使用sae的mail服务来处理django的邮件发送了。

ADMINS = (
    ('administrator', 'administrator@gmail.com'),
)

# ref: https://docs.djangoproject.com/en/dev/ref/settings/#email
```python
EMAIL_BACKEND = 'sae.ext.django.mail.backend.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sender@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_TLS = True
SERVER_EMAIL = DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

希望开源后能供大家来学习交流～


ps：需要转载或者使用源码请勿修改copyright下的签名，希望大家支持GNU计划中的open source环节！

（gmail） winisbest@gmail.com


