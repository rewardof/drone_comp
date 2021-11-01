from django.contrib import admin
from .models import Drone, DroneCategory, Pilot, Competition


class DroneAdmin(admin.ModelAdmin):
    model = Drone
    read_only_fields = ('id',)
    list_display = ('id', 'name')


admin.site.register(Drone, DroneAdmin)
admin.site.register(DroneCategory)
admin.site.register(Pilot)
admin.site.register(Competition)

