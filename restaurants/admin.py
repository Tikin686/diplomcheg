from django.contrib import admin
from restaurants.models import Restaurant, Reserve, Table


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'description')
    list_filter = ('name', )
    search_fields = ('name', 'address')


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'size')
    list_filter = ('number', )


@admin.register(Reserve)
class ReserveAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'start_reserve', 'end_reserve')
    list_filter = ('name', )