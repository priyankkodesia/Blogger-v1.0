from django.shortcuts import render, redirect,get_object_or_404
from .forms import PostForm
from urllib.parse import quote_plus
from django.core.urlresolvers import reverse
from .models import PostModel
from django.http.response import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def createView(request):
    form =PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        return redirect('Posts:list')
    return render(request,'create_post.html',{'form':PostForm})

        
def listView(request):
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

def detailView(request,slug=None):
    queryset=PostModel.objects.get(slug=slug)
    share_string=quote_plus(queryset.content)
    context={'object':queryset,'share_string':share_string}
    return render(request,'post_detail.html',context)

def deleteView(request,pk=None):
    queryset=PostModel.objects.get(pk=pk)
    queryset.delete()
    return render(request,'delete_post.html')
    