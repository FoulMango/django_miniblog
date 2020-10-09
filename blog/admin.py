from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import BlogPost, Comment, Biography


class BioInline(admin.StackedInline):
    model = Biography
    can_delete = False
    verbose_name_plural = 'biographies'


class UserAdmin(BaseUserAdmin):
    inlines = (BioInline,)


admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
