from django.urls import path
from . import views
from .views import stripe_webhook

app_name = "subscription"

urlpatterns = [
    path("checkout/<slug:slug>/", views.start_checkout, name="checkout"),
    path("success/", views.checkout_success, name="success"),
    path("cancel/", views.checkout_cancel, name="cancel"),
    path("webhook/", stripe_webhook, name="stripe-webhook")
]
