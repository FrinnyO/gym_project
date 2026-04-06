from django.contrib import admin
from .models import Client, Service, Subscription

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'created_at')
    search_fields = ('full_name', 'phone')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'start_date', 'is_active')
    list_filter = ('is_active', 'service')