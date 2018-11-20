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
    url(r'^upload/(\d*)/$', views.upload, name='upload'),
    url(r'^getTag/$', views.json_get_tags, name='getTag'),
    url(r'^comment/$', views.comment, name='comment'),
    url(r'^comment/list/(\d*)/(\d*)', views.comment_show, name='comment_list'),
    url(r'^comment/audit/(\d+)/(accept|reject)/$', views.comment_audit, name='comment_audit'),
    url(r'^comment/del/(\d+)/$', views.comment_del, name='comment_del'),
    url(r'^post/like/(\d+)/(\d+)/$', views.like_article, name='like_article'),
    url(r'^comment/like/(\d+)/(\d+)/$', views.like_comment, name='like_comment'),
    url(r'^post/list/(\d*)/(\d*)', views.post_view, name='post_list'),
    url(r'^post/modify/(\d*)', views.post_modify, name='post_modify'),
    url(r'^post/(\d+)/del/(\d+)', views.post_del, name='post_del'),
    url(r'^post/(\d+)/revoke/(\d+)', views.post_revoke, name='post_revoke'),
    url(r'^site_edit/$', views.set_site, name='site_edit'),
    url(r'^upload_page/(\d*)', views.upload_page, name='upload_page'),
    url(r'^media/list/(\d*)', views.media_view, name='media_view'),
    url(r'^media/modify/(\d*)', views.media_modify, name='media_modify'),
    url(r'^media/del/(\d*)/$', views.media_del, name='media_del'),
    url(r'^media/new/$', views.media_new_view, name='media_del'),
    url(r'^media/delByOName/(\w.*)', views.media_del_by_o_name, name='media_del_by_o_name'),

]
