from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.


def upload_location(object,filename):
    print(object.pk)
    print(object.id)
    print(object.title)


    return "%s/%s" %(object.title,filename)

class PostModel(models.Model):
    title           =models.CharField(max_length=120)
    content         =models.TextField(max_length=256)
    image           =models.ImageField(upload_to=upload_location,null=True,blank=True)
    timestamp       =models.DateField(auto_now_add=True)
    updated         =models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('Posts:detail',kwargs={'pk':self.pk})
    

    
