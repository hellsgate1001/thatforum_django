from django.contrib import admin

from .models import ForumCategory, ForumThread, ForumPost


class ForumCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    # fields = ('name', 'order')


class ForumThreadAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    # fields = ('name', 'order')


admin.site.register(ForumCategory, ForumCategoryAdmin)
admin.site.register(ForumThread, ForumThreadAdmin)
admin.site.register(ForumPost)
