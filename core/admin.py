from django.contrib import admin
from django.contrib.auth.admin import  UserAdmin as DjangoUserAdmin
from .models import *

# Register your models here.
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None,{"fields":("email","password")}),
        ("Personal info",{"fields":("first_name","last_name","usertype")}),
        ("Permission",{"fields":("is_active","is_staff","is_superuser","groups","user_permissions")}),
        ("Important dates",{"fields":("last_login","date_joined")}),
    )
    add_fieldsets = ( (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),)

    list_display = ("email","is_active","is_staff","is_superuser")
    search_fields = ("email",)
    ordering = ("email",)
    actions = ("make_active","make_inactive")
    def make_active(self,request,queryset):
        queryset.update(is_active = True)
    def make_inactive(self,request,queryset):
        queryset.update(is_active = False)
    make_active.short_description = 'Make Selected Users Active'
    make_inactive.short_description = 'Make Selected Users Inactive'


admin.site.register(Deposit)
admin.site.register(Withdraw)
admin.site.register(User, UserAdmin)
admin.site.register(Transfer)
admin.site.register(Notification)
admin.site.register(Feedback)
admin.site.register(Account)
admin.site.register(Branch)
