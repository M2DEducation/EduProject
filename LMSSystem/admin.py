from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, ClassList, Assignments, ClassListGroupCode, ClassListGroup

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

@admin.register(ClassList)
class ClassList(admin.ModelAdmin):
    pass

@admin.register(Assignments)
class Assignments(admin.ModelAdmin):
    pass

@admin.register(ClassListGroupCode)
class ClassListGroupCode(admin.ModelAdmin):
    pass

@admin.register(ClassListGroup)
class ClassListGroup(admin.ModelAdmin):
    pass

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)