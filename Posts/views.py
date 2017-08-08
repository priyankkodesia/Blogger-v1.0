from django.shortcuts import render, redirect,get_object_or_404
from .forms import PostForm,LoginForm,UserRegistrationForm,UserBioForm
from urllib.parse import quote_plus
from django.core.urlresolvers import reverse,reverse_lazy
from .models import PostModel,AuthorDetailModel
from django.contrib.auth.models import User
from django.http import Http404
from django.http.response import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView
from django.views.generic.list import ListView
from django.template import RequestContext
import datetime

# Create your views here.

def register(request):
    if request.method=="GET":
        context = {'UserRegistrationForm': UserRegistrationForm,
                   'UserBioForm': UserBioForm}
        return render(request,'registration.html',context)
    if request.method=="POST":
        RegForm = UserRegistrationForm(request.POST)
        BioForm = UserBioForm(request.POST or None,request.FILES or None)
        if RegForm.is_valid() and BioForm.is_valid():
            user=RegForm.save()
            Auth=BioForm.save(commit=False)
            Auth.Author = user
            BioForm.save()
            return redirect('login')
        else:
            
            return render(request, 'registration.html', {'RegForm.errors': RegForm.errors,
                                                         'BioForm.errors': BioForm.errors})

class register_author_bio(CreateView):
    form_class = UserBioForm
    template_name='registration_author_bio.html'
    success_url = reverse_lazy('login')

    

def loginView(request):
    if request.method=="GET":
         return render(request,'login.html',{'form':LoginForm})
    else:
        form = LoginForm(request.POST or None)
        username=request.POST.get('username')
        password=request.POST.get('password')
    
        user= authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                response= redirect('Posts:list')
                
                response.set_cookie('last_connection',datetime.datetime.now())
                response.set_cookie('username',datetime.datetime.now())

                return response
        else:
            invalid_message="Invalid Credentials"
            return render(request,'login.html',{'invalid_message':invalid_message,'form':form})
    
        return render(request,'login.html',{'form':form})

@login_required
def createView(request):
    if not request.user.is_authenticated:
        raise Http404
    form =PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.Author=request.user
        instance.save()
        return redirect('Posts:list')
    return render(request,'create_post.html',{'form':PostForm})

def searchPosts(request):
    result=[]
    query=request.POST.get('q')
    print('query is %s' %(query))
    res=PostModel.objects.filter(title__icontains=query)
    for r in res:
        full_name=r.Author.get_full_name()
        
        if r.image :
            result.append({'title':r.title,
                           'content':r.content,
                           'image':r.image.url,
                           'full_name':full_name,
                           'timestamp':r.timestamp,
                           'slug':r.slug})
        else:
            result.append({'title':r.title,
                           'content':r.content,
                           'full_name':full_name,
                           'timestamp':r.timestamp,
                           'slug':r.slug})
    print(result)
    return JsonResponse({'result':result})


def searchAuthors(request):
    result=[]
    query=request.POST.get('query',None)
    print('query is %s' %(query))
    res=AuthorDetailModel.objects.filter(full_name__icontains=query)
    print(res)
    for r in res:       
        if r.profile_pic :
            result.append({'pk':r.Author.pk,
                            'full_name':r.full_name,
                            'work':r.work,
                            'profile_pic':r.profile_pic.url,                         
                            'address':r.address,})
        else:
            result.append({'pk': r.Author.pk,
                            'full_name': r.full_name,
                            'work': r.work,
                            'address': r.address, })
    print(result)
    return JsonResponse({'result':result})


@login_required
def postListView(request):
    print("inside post list ")
    query = PostModel.objects.all()
    print(query)
    return render(request, 'posts_list.html', {'posts_list': query})


@login_required
def authorListView(request):
    print("inside authors list ")
    query = AuthorDetailModel.objects.all()
    print(query)
    return render(request, 'authors_list.html', {'authors_list': query})

@login_required
def listView(request):
    if not request.user.is_authenticated:
        raise Http404

    if 'username' in request.COOKIES and 'last_connection' in request.COOKIES:
        username=request.COOKIES['username']
        
        last_connection=request.COOKIES['last_connection']
        last_connection_time = datetime.datetime.strptime(last_connection[:-7],
            "%Y-%m-%d %H:%M:%S")

        if (datetime.datetime.now() - last_connection_time).seconds <500:
            current_user=User.objects.get(pk=request.user.pk)
            print("current user is %s"%(current_user))
            posts_list = PostModel.objects.all().order_by('-pk')
            paginator = Paginator(posts_list, 3)
            page = request.GET.get('page1')
            try:
                posts_list = paginator.page(page)
            except PageNotAnInteger:
                posts_list = paginator.page(1)
            except EmptyPage:
                posts_list = paginator.page(paginator.num_pages)

            authors_list = AuthorDetailModel.objects.exclude(pk=1).order_by('-pk')
            paginator = Paginator(authors_list, 3)
            page = request.GET.get('page2')
            try:
                authors_list = paginator.page(page)
            except PageNotAnInteger:
                authors_list = paginator.page(1)
            except EmptyPage:
                authors_list = paginator.page(paginator.num_pages)

            context = {'posts_list': posts_list, 'authors_list': authors_list,'current_user':current_user}
            return render(request, 'index.html', context)

        else:
            return reverse_lazy('login')
    else:        
        return render(request, 'login.html', {})


@login_required
def postDetailView(request,slug=None):
    if not request.user.is_authenticated:
        raise Http404
    queryset=PostModel.objects.get(slug=slug)
    share_string=quote_plus(queryset.content)
    context={'object':queryset,'share_string':share_string}
    return render(request,'post_detail.html',context)

class postLikeToggle(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        slug=self.kwargs.get('slug')
        obj=PostModel.objects.get(slug=slug)
        print("obj is %s"%(obj))
        url_=obj.get_absolute_url()
        print('so url_ becomes %s'%(url_))
        user=self.request.user
        if user.is_authenticated():
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_


@login_required
def authorDetailView(request,pk=None):
    print("inside author detail view")
    if not request.user.is_authenticated:
        raise Http404
    query=AuthorDetailModel.objects.get(pk=pk)
    queryset=PostModel.objects.filter(Author=query.Author.pk)
    context={'author':query,'posts':queryset}
    return render(request,'author_detail.html',context)

@login_required
def deleteView(request,pk=None):
    if not request.user.is_authenticated:
        raise Http404
    queryset=PostModel.objects.get(pk=pk)
    queryset.delete()
    return redirect('Posts:list')

@login_required
def editView(request,slug=None):
    if not request.user.is_authenticated:
        raise Http404
    instance= get_object_or_404(PostModel,slug=slug)
    form =PostForm(request.POST or None,request.FILES or None, instance=instance)
    if request.user.is_authenticated:
        if form.is_valid():
            instance=form.save(commit=False)
            instance.Author=request.Author
            instance.save()
            instance.edited= True
            return redirect('Posts:list')
    return render(request,'create_post.html',{'form':PostForm})

@login_required
def logoutView(request):
    logout(request)
    return redirect('login')
