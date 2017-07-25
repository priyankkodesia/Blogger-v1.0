from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.


class PostModel(models.Model):
    title           =models.CharField(max_length=120)
    content         =models.TextField(max_length=256)
    timestamp       =models.DateField(auto_now_add=True)
    updated         =models.DateField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('Posts:detail',kwargs={'pk':self.pk})