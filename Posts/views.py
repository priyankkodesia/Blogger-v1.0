from django.shortcuts import render, redirect,get_object_or_404
from .forms import PostForm,LoginForm,RegistrationForm
from urllib.parse import quote_plus
from django.core.urlresolvers import reverse
from .models import PostModel
from django.http import Http404
from django.http.response import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    form=RegistrationForm(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.Author=request.user
        instance.save()
        return redirect('Posts:login')
    return render(request,'registration.html',{'form':form})
    

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
                print("not none")
                return redirect('Posts:list')
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
                           'updated':r.updated,
                           'slug':r.slug})
        else:
            result.append({'title':r.title,
                           'content':r.content,
                           'full_name':full_name,
                           'timestamp':r.timestamp,
                           'updated':r.updated,
                           'slug':slug})
    print(result)
    return JsonResponse({'result':result})

@login_required
def listView(request):
    if not request.user.is_authenticated:
        raise Http404
    query=PostModel.objects.all().order_by('-pk')
    paginator = Paginator(query, 10)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context={'object_list':queryset}
    return render(request,'index.html',context)

@login_required
def detailView(request,slug=None):
    if not request.user.is_authenticated:
        raise Http404
    queryset=PostModel.objects.get(slug=slug)
    share_string=quote_plus(queryset.content)
    context={'object':queryset,'share_string':share_string}
    return render(request,'post_detail.html',context)

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
