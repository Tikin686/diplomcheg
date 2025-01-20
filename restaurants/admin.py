from django.contrib import admin
from restaurants.models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'description')
    list_filter = ('name', )
    search_fields = ('name', 'address')