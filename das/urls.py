from django.conf.urls import url, include
#from django.contrib import das
#from index import views
import views


urlpatterns = [
    #url(r'^das/', das.site.urls),
    url(r'^$', views.index_view, name='das_index')
]
