from django.conf.urls import url

# from django.contrib import das
# from index import views
import views

urlpatterns = [
    # url(r'^das/', das.site.urls),
    url(r'^$', views.index_view, name='das_index'),
    url(r'^category/(\d+)/del/(\d+)', views.category_del, name='category_del'),
    url(r'^category/modify/(\d*)/', views.category_modify, name='category_modify'),
    url(r'^category/(\d*)', views.category_view, name='category'),
    url(r'^tag/(\d+)/del/(\d+)', views.tag_del, name='tag_del'),
    url(r'^tag/modify/(\d*)/', views.tag_modify, name='tag_modify'),
    url(r'^tag/(\d*)', views.tag_view, name='tag'),
    url(r'^post/new/$', views.post_new_view, name='post_new'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^getTag/$', views.json_get_tags, name='getTag'),
    url(r'^comment/$', views.comment, name='comment'),
    url(r'^comment/list/(\d*)/(\d*)', views.comment_show, name='comment_list'),
    url(r'^comment/audit/(\d+)/(accept|reject)/$', views.comment_audit, name='comment_audit'),
    url(r'^comment/del/(\d+)/$', views.comment_del, name='comment_del'),
    url(r'^post/like/(\d+)/(\d+)/$', views.like_article, name='like_article'),
]
