from django.contrib import admin

# Register your models here.
from .models import PostModel

class PostModelAdmin(admin.ModelAdmin):
    list_display=['title','timestamp','updated']
    list_display_links = ['title','timestamp']

    class Meta:
        model=PostModel


admin.site.register(PostModel, PostModelAdmin)