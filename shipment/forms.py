from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Address, Shipment


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["city", "street", "postal_code"]


class SignupForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["city", "street", "postal_code"]


class ShipmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["sender_address"].queryset = Address.objects.filter(user=user)
        self.fields["receiver_address"].queryset = Address.objects.filter(user=user)

    class Meta:
        model = Shipment
        fields = [
            "sender_address",
            "receiver_name",
            "receiver_familyname",
            "receiver_address",
            "package",
        ]
