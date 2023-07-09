from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, ListView, CreateView, DeleteView
from django.urls import reverse_lazy

from .forms import SignupForm, AddressForm, ShipmentForm
from .models import Shipment, Address


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    login_url = reverse_lazy("login")


class UserSignupView(FormView):
    template_name = "signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy("index")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index")


class ShipmentListView(LoginRequiredMixin, ListView):
    model = Shipment
    template_name = "shipment_list.html"
    context_object_name = "shipments"

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset


class AddressView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = "create_address.html"
    success_url = reverse_lazy("address_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserAddressListView(LoginRequiredMixin, ListView):
    model = Address
    template_name = "user_address_list.html"
    context_object_name = "addresses"

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    template_name = "address_confirm_delete.html"
    success_url = reverse_lazy("address_list")


class ShipmentCreateView(LoginRequiredMixin, CreateView):
    model = Shipment
    form_class = ShipmentForm
    template_name = "create_shipment.html"
    success_url = reverse_lazy("freight")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
