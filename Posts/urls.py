from django.conf.urls import url,include
from Posts import views

urlpatterns = [
    url(r'^$',views.listView,name='list'),
    url(r'^create/$',views.createView,name='create'),
    url(r'^(?P<slug>[-\w]+)/$',views.postDetailView,name='postdetail'),
    url(r'^(?P<slug>[-\w]+)/like', views.postLikeToggle.as_view(), name='like-toggle'),
    url(r'^author/(?P<pk>\d+)/$',views.authorDetailView,name='authordetail'),

    url(r'^(?P<pk>\d+)/delete/$',views.deleteView,name='delete'),

]
