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
]
