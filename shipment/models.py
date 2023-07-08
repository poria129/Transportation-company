from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Package(models.Model):
    SIZE_CHOICES = (
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
    )

    WEIGHT_CHOICES = (
        ("L", "Light"),
        ("M", "Medium"),
        ("H", "Heavy"),
    )

    size = models.CharField(max_length=1, choices=SIZE_CHOICES)
    weight = models.CharField(max_length=1, choices=WEIGHT_CHOICES)

    def __str__(self):
        return f"Package (Size: {self.get_size_display()}, Weight: {self.get_weight_display()})"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.postal_code}"


class Shipment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shipments")
    sender_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="sent_shipments"
    )
    receiver_name = models.CharField(max_length=250)
    receiver_familyname = models.CharField(max_length=250)
    receiver_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="received_shipments"
    )
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    sending_date = models.DateTimeField(blank=True, null=True)
    receiving_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Shipment from {self.sender_address} to {self.receiver_address}"

    def get_location_code(self):
        if self.sender_address.city == self.receiver_address.city:
            return 1
        elif self.sender_address.city.country == self.receiver_address.city.country:
            return 2
        else:
            return 3

    def calculate_price(self):
        location_code = self.get_location_code()
        size_factor = 1.0  # Default size factor
        weight_factor = 1.0  # Default weight factor

        if self.package.size == "M":
            size_factor = 1.2
        elif self.package.size == "L":
            size_factor = 1.5

        if self.package.weight == "M":
            weight_factor = 1.2
        elif self.package.weight == "H":
            weight_factor = 1.5

        if location_code == 1:
            return 10.0 * size_factor * weight_factor
        elif location_code == 2:
            return 20.0 * size_factor * weight_factor
        elif location_code == 3:
            return 30.0 * size_factor * weight_factor

    def save(self, *args, **kwargs):
        if not self.sending_date or not self.receiving_date:
            location_code = self.get_location_code()
            if location_code == 1:
                self.sending_date = timezone.now() + timezone.timedelta(days=1)
                self.receiving_date = timezone.now() + timezone.timedelta(days=2)
            elif location_code == 2:
                self.sending_date = timezone.now() + timezone.timedelta(days=1)
                self.receiving_date = timezone.now() + timezone.timedelta(days=5)
            elif location_code == 3:
                self.sending_date = timezone.now() + timezone.timedelta(days=1)
                self.receiving_date = timezone.now() + timezone.timedelta(days=15)

        if not self.price:
            self.price = self.calculate_price()

        super().save(*args, **kwargs)

    def clean(self):
        location_code = self.get_location_code()
        sending_city_shipments = (
            Shipment.objects.filter(
                sending_address__city=self.sending_address.city,
                sending_date__date=timezone.now().date(),
            )
            .exclude(pk=self.pk)
            .count()
        )

        if location_code != 1 and sending_city_shipments >= 10:
            raise ValidationError(
                "Maximum number of shipments exceeded for the sending city."
            )
