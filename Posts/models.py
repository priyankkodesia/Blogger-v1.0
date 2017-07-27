from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
# Create your models here.


def upload_location(object,filename):
    return "%s/%s" %(object.pk,filename)

class PostModel(models.Model):
    Author          =models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
    title           =models.CharField(max_length=120,null=True)
    slug            =models.SlugField(unique=True,null=True,blank=True)
    content         =models.TextField(max_length=256,null=True)
    image           =models.ImageField(upload_to=upload_location,null=True,blank=True)
    timestamp       =models.DateField(auto_now_add=True)
    updated         =models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('Posts:detail',kwargs={'slug':self.slug})
 
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = PostModel.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)



pre_save.connect(pre_save_post_receiver, sender=PostModel)
 
#    
# def pre_save_post_reciever(sender,intance,*args,**kwargs):
#     slug=slugify(instance.title)
#     print(slug)
#     exists=PostModel.objects.filter(slug=instance.slug).exists()
#     if exists:
#         slug="%s-%s" %(slug,instance.id)
#     instance.slug=slug    
# 
# pre_save.connect(pre_save_post_reciever,sender=PostModel)
#     
