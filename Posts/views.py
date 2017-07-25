from django.shortcuts import render
from .forms import PostForm
from django.core.urlresolvers import reverse
from .models import PostModel
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
# Create your views here.


def createView(request):
    form=PostForm()
    if request.method =="GET":
        context={'form':form}
        return render(request,'create_post.html',context)
    
    if request.method=="POST":
        form =PostForm(request.POST or None)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
    return HttpResponseRedirect(instance.get_absolute_url())
        
def listView(request):
    queryset=PostModel.objects.all()
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
    