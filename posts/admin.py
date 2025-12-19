from django.contrib import admin
from posts.models import Post, Category, Tag, Comment

# admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'content')
    list_display = ('title','content','category', 'author', 'created_at', 'updated_at', 'rate')
    list_filter = ('category', 'created_at','updated_at')



admin.site.register(Comment)    