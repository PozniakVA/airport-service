from django.contrib import admin

from airport.models import (
    Airport,
    Airplane,
    AirplaneType,
    Route,
    Flight,
    Crew,
    Ticket,
    Order,
)

@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ("name", "airplane_type")

@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    pass

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    pass

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    pass

@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    pass

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass

class TicketLine(admin.TabularInline):
    model = Ticket
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketLine,)
