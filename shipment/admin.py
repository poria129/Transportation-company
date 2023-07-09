from django.contrib import admin
from .models import City, Package, Address, Shipment


class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "sender_address",
        "receiver_name",
        "receiver_address",
        "package",
        "price",
        "sending_date",
        "receiving_date",
    )
    exclude = ["price", "sending_date", "receiving_date"]
    list_filter = (
        "user",
        "sending_date",
        "receiving_date",
        "package__size",
        "package__weight",
    )
    search_fields = (
        "user__username",
        "sender_address__city__name",
        "receiver_name",
        "receiver_address__city__name",
    )

    def sender_address(self, obj):
        return obj.sender_address.__str__()

    def receiver_address(self, obj):
        return obj.receiver_address.__str__()


admin.site.register(City)
admin.site.register(Package)
admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(Address)
