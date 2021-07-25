from django.contrib import admin

from blog.models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    prepopulated_fields = {"slug": ("comment"[:45],)}


class PostAdminView(admin.ModelAdmin):
    list_display = ('title', 'post', 'created_at')
    list_display_links = ('title', 'post')
    search_fields = ('title', 'post')
    prepopulated_fields = {"slug": ("title",)}

    inlines = [CommentInline]


#
# class CommentAdminView(admin.ModelAdmin):
#     list_display = ('comment', 'created_at')
#     list_display_links = ('comment',)
#     search_fields = ('comment',)


admin.site.register(Post, PostAdminView)
# admin.site.register(Comment, CommentAdminView)
