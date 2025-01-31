from django.contrib import admin

from restaurants.models import Reserve, Restaurant, Table


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "description")


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "seats")


@admin.register(Reserve)
class ReserveAdmin(admin.ModelAdmin):
    list_display = ("client",)
