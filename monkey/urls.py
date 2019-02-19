"""monkey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include

# from das import views
from das.views import login_view
from das.views import logout_view
from das.views import register_view
# from django.contrib import das
from index import views

urlpatterns = [
    # url(r'^das/', das.site.urls),
    # url(r'^tinymce/', include('tinymce.urls')),
    url(r'^das/', include('das.urls')),
    url(r'^register.html', register_view, name='register'),
    url(r'^login.html', login_view, name='login'),
    url(r'^logout.html', logout_view, name='logout'),
    url(r'^(\d*)$', views.index_view, name='index'),
    url(r'^p/(\d*)\.html', views.post_show, name='show'),
    url(r'^preview/(\d*)\.html', views.post_preview, name='preview'),
    url(r'^category/(\d*)/(\d*)\.html', views.category_show, name='category_show'),
    url(r'^tag/(\d*)/(\d*)\.html', views.tag_show, name='tag_show'),
    url(r'^author/(\d*)/(\d*)\.html', views.user_show, name='user_show'),
    url(r'^favicon.ico$', views.get_favicon, name='get_favicon'),
    url(r'^search.html$', views.search, name='search'),
    url(r'^search/(\w.*)/(\d*)\.html', views.search_show, name='search_show'),
    url(r'^(\w.*)\.html', views.page_show, name='page_show'),

]
