from django.urls import path
from .views import (
    UserLoginView,
    UserSignupView,
    IndexView,
    UserLogoutView,
    ShipmentListView,
    AddressView,
    UserAddressListView,
    AddressDeleteView,
    ShipmentCreateView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("login", UserLoginView.as_view(), name="login"),
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("logout", UserLogoutView.as_view(), name="logout"),
    path("freight/", ShipmentListView.as_view(), name="freight"),
    path("freightcreate/", ShipmentCreateView.as_view(), name="freight_create"),
    path("addresscreate/", AddressView.as_view(), name="address_create"),
    path("addresslist/", UserAddressListView.as_view(), name="address_list"),
    path(
        "address/delete/<int:pk>/", AddressDeleteView.as_view(), name="delete_address"
    ),
]
