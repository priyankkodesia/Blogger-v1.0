from django.shortcuts import render, redirect
from .forms import PostForm
from django.core.urlresolvers import reverse
from .models import PostModel
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
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

def detailView(request,pk=None):
    queryset=PostModel.objects.get(pk=pk)
    context={'object':queryset}
    return render(request,'post_detail.html',context)

def deleteView(request,pk=None):
    queryset=PostModel.objects.get(pk=pk)
    queryset.delete()
    return render(request,'delete_post.html')
    