from django.conf.urls import url,include
from Posts import views

urlpatterns = [
    url(r'^$',views.listView,name='list'),
    url(r'^create/$',views.createView,name='create'),

    url(r'^(?P<slug>[-\w]+)/$',views.detailView,name='detail'),
    url(r'^(?P<pk>\d+)/delete/$',views.deleteView,name='delete'),


]
