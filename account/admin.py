from django.contrib import admin
from .models import User, Otp


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'email']


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'code', 'created']


