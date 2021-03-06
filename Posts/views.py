from django.shortcuts import render, redirect,get_object_or_404
from .forms import PostForm,LoginForm,UserRegistrationForm,UserBioForm,CommentsForm
from urllib.parse import quote_plus
from django.core.urlresolvers import reverse,reverse_lazy
from .models import PostModel,AuthorDetailModel,CommentsModel,Post_views,LoggedUser
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from django.http.response import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView,DetailView
from django.views.generic.list import ListView
from django.contrib.auth.views import password_reset, password_reset_confirm,password_reset_complete
from django.template import RequestContext
import datetime
from django.core.exceptions import ObjectDoesNotExist


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
            messages.success(request,"Your profile has been created.Welcome to the Blog.!!!",extra_tags='alert')
            return redirect('login')
        else:
            messages.warning(request,"Please correct the errors below")
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
    return JsonResponse({'result':result})


def searchAuthors(request):
    result=[]
    query=request.POST.get('query',None)
    res=AuthorDetailModel.objects.filter(full_name__icontains=query)
    for r in res:       
        if r.profile_pic :
            result.append({'pk':r.Author.pk,
                            'full_name':r.full_name,
                            'work':r.work,
                            'profile_pic':r.profile_pic.url,                         
                            'address':r.address,
                             'author_bio':r.author_bio})
        else:
            result.append({'pk': r.Author.pk,
                            'full_name': r.full_name,
                            'work': r.work,
                            'address': r.address,
                            'author_bio':r.author_bio })
    return JsonResponse({'result':result})


@login_required
def postListView(request):
    posts_list = PostModel.objects.all().order_by('-likes')
    posts_count=PostModel.objects.all().count()
    paginator = Paginator(posts_list, 6)
    page = request.GET.get('page1')
    try:
        posts_list = paginator.page(page)
    except PageNotAnInteger:
        posts_list = paginator.page(1)
    except EmptyPage:
        posts_list = paginator.page(paginator.num_pages)
    return render(request, 'posts_list.html', {'posts_list': posts_list,'posts_count':posts_count})


@login_required
def authorListView(request):
    authors_list = AuthorDetailModel.objects.exclude(pk=1).order_by('-pk')
    authors_count=AuthorDetailModel.objects.all().count()
    paginator = Paginator(authors_list, 6)
    page = request.GET.get('page2')
    try:
        authors_list = paginator.page(page)
    except PageNotAnInteger:
        authors_list = paginator.page(1)
    except EmptyPage:
        authors_list = paginator.page(paginator.num_pages)
    return render(request, 'authors_list.html', {'authors_list': authors_list,'authors_count': authors_count})

@login_required
def listView(request):
    if not request.user.is_authenticated:
        raise Http404

    current_user=User.objects.get(pk=request.user.pk)
    posts_list = PostModel.objects.all().order_by('-pk')[:3]
    authors_list = AuthorDetailModel.objects.exclude(pk=1).order_by('-pk')[:3]

    logged_users= [user.user for user in LoggedUser.objects.all()]
    context = {'posts_list': posts_list,'authors_list': authors_list,'current_user':current_user,'logged_users':len(logged_users)}
    return render(request, 'index.html', context)


class PostDetailView(DetailView,LoginRequiredMixin):
    model = PostModel
    template_name = "post_detail.html"

    def get_object(self,*args,**kwargs):
        self.Flag=False
        self.slug=self.kwargs['slug']
        self.query=get_object_or_404(PostModel,slug=self.slug)

        if(self.query.Author.pk == self.request.user.pk):
            self.Flag =True
        self.share_string= quote_plus(self.query.content)
        return self.query


    def get_client_ip(self):
        ip = self.request.META.get("HTTP_X_FORWARDED_FOR", None)
        if ip:
            ip = ip.split(", ")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR", "")
        return ip

    def tracking_hit_post(self):
        entry = self.model.objects.get(slug=self.kwargs['slug'])

        try:
            Post_views.objects.get(entry=entry, ip=self.get_client_ip(), session=self.request.session.session_key)
        except ObjectDoesNotExist:
                import socket
                dns = str(socket.getfqdn(self.get_client_ip())).split('.')[-1]
                try:
                    if str(dns) == 'localhost':
                        view = Post_Views(entry=entry, 
                                                  ip=self.get_client_ip(),
                                                  created=datetime.datetime.now(),
                                                  session=self.request.session.session_key)
                        view.save()
                    else: pass
                except ValueError: pass
        return Post_views.objects.filter(entry=entry).count()
        
    def get_context_data(self, **kwargs):
        context_data = super(PostDetailView, self).get_context_data(**kwargs)

        context_data['get_client_ip'] = self.get_client_ip()
        context_data['tracking_hit_post'] = self.tracking_hit_post()
        context_data['flag'] = self.Flag
        context_data['share_string'] = self.share_string
        context_data['object'] = self.get_object()

        return context_data


@login_required
def chatView(request,*args,**kwargs):
     if request.method=="GET":

        try:
            comments=CommentsModel.objects.all().order_by('-pk')
        except:
            comments = None
        return render(request,'chat.html',{'comments':comments})
     if request.method=="POST":
        q=request.POST.get('comment_query')
        CommentForm = CommentsForm(request.POST)
        if CommentForm.is_valid():
            comment_instance = CommentForm.save(commit=False)
            comment_instance.Author = request.user
            comment_instance.content = q
            comment_instance.save()
        return redirect('Posts:chat')
    

class postLikeToggle(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        slug=self.kwargs.get('slug')
        obj=PostModel.objects.get(slug=slug)
        url_=obj.get_absolute_url()
        user=self.request.user
        if user.is_authenticated():
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_


@login_required
def authorDetailView(request,pk=None):
    if not request.user.is_authenticated:
        raise Http404
    query=AuthorDetailModel.objects.get(pk=pk)
    queryset=PostModel.objects.filter(Author=query.Author.pk)
    context={'author':query,'posts':queryset}
    return render(request,'author_detail.html',context)

@login_required
def deleteView(request,slug=None):
    if not request.user.is_authenticated:
        raise Http404
    queryset=PostModel.objects.get(slug=slug)
    queryset.delete()
    return redirect('Posts:posts')


@login_required
def password_change(request):
    form_class =PasswordChangeForm(request.user)
    if request.method == "GET":
        return render(request,'password_change.html',{'form':form_class})
    if request.method == "POST":
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            return redirect("Posts:list")
        else:
            messages.warning(request,"Please correct the errors below")
    return render(request,'password_change.html',{'form':form})


@login_required
def logoutView(request):
    logout(request)
    return render(request,'login.html',{})

def reset_confirm(request, uidb36=None, token=None):
    return password_reset_confirm(request, template_name='registration/password_reset_confirm.html',
        uidb36=uidb36, token=token, post_reset_redirect='login.html')

def reset(request):
    return password_reset(request, template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        post_reset_redirect=reverse('login'))
