from django.contrib import admin
from apps.users.models import User
from django.contrib.auth.models import Group

admin.site.unregister(Group)


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('last_login', 'last_request', 'date_joined')


admin.site.register(User, UserAdmin)
