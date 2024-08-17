from django.contrib import admin

from airport.models import Airport, Airplane, AirplaneType, Route

admin.site.register(Airplane)
admin.site.register(AirplaneType)
admin.site.register(Airport)
