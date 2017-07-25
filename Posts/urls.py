from django.conf.urls import url,include
from Posts import views

urlpatterns = [
    url(r'^$',views.listView,name='list'),
    url(r'^(?P<pk>\d+)/$',views.detailView,name='detail'),
    url(r'^create/$',views.createView,name='create'),
    url(r'^(?P<pk>\d+)/delete/$',views.deleteView,name='delete'),


]
