from django.contrib import admin

# Register your models here.
from .models import PostModel,AuthorDetailModel,CommentsModel

class PostModelAdmin(admin.ModelAdmin):
    list_display=['title','timestamp']
    list_display_links = ['title','timestamp']

    class Meta:
        model=PostModel

admin.site.register(PostModel,PostModelAdmin)
admin.site.register(AuthorDetailModel)
admin.site.register(CommentsModel)
