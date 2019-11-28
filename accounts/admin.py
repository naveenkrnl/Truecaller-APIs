from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import MyUser
from .forms import UserChangeForm, UserCreationForm



class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('name', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('name', 'phone_number', 'password')}),
        ('Personal info', {'fields': ('email','spam_count')}),
        ('Permissions', {'fields': ('is_admin','is_staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'phone_number', 'email','password1', 'password2')}
        ),
    )
    search_fields = ('phone_number', 'phone_number',)
    ordering = ('name', 'phone_number',)
    filter_horizontal = ()





admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)