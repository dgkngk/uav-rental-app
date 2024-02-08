from django.contrib import admin
from .models import UAV, Rental


class UAVAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'weight', 'category')
    search_fields = ['brand', 'model', 'weight', 'category']
    list_filter = ['is_rented']


class RentalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'uav', 'rental_start', 'rental_end')
    list_filter = ('user', 'uav', 'rental_start', 'rental_end')
    search_fields = ('user__username', 'uav__brand', 'uav__model')


admin.site.register(Rental, RentalAdmin)
admin.site.register(UAV, UAVAdmin)
