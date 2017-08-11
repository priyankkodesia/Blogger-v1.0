"""Blogger_v1 URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from Posts import views
from django.contrib.auth.views import (
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
    # these are the two new imports
    password_change,
    password_change_done,
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^searchPosts/',views.searchPosts,name='search'),
    url(r'^searchAuthors/',views.searchAuthors,name='search_authors'),
    url(r'^posts/',include('Posts.urls',namespace='Posts')),
    url(r'^$',views.loginView,name='login'),
    url(r'^register/$',views.register,name='register'),
    url(r'^logout/$',views.logoutView,name='logout'),
    url(r'session_security/', include('session_security.urls')),


    url(r'^', include('django.contrib.auth.urls')),

]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
