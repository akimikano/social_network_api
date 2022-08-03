from django.contrib import admin
from apps.main.models import (
    Post,
    Like
)


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ()


class LikeAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
