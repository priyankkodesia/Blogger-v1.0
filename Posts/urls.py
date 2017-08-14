from django.conf.urls import url,include
from Posts import views

urlpatterns = [
    url(r'^login/$',views.loginView,name='blog_login'),
    url(r'^chat/$',views.chatView,name='chat'),
    url(r'^author/(?P<pk>\d+)/$',views.authorDetailView,name='authordetail'),
    url(r'^posts_list/$', views.postListView, name='posts'),
    url(r'^authors_list/$', views.authorListView, name='authors'),  
    url(r'^$',views.listView,name='list'),
    url(r'^change_password/$',views.password_change,name='change_password'),
    url(r'^create/$',views.createView,name='create'),
    url(r'^(?P<slug>[-\w]+)/$',views.PostDetailView.as_view(),name='postdetail'), 
    url(r'^(?P<slug>[-\w]+)/like', views.postLikeToggle.as_view(), name='like-toggle'),
    
    

    url(r'^(?P<slug>[-\w]+)/delete/$',views.deleteView,name='delete'),

]
