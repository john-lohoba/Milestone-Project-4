from django.conf import settings
from django.http import HttpResponse
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

from subscription.webhook_handler import (
    handle_checkout_completed,
    handle_subscription_updated,
    handle_subscription_deleted,
)


def dispatch_stripe_event(event):
    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        handle_checkout_completed(data)

    elif event_type in (
        "customer.subscription.updated",
        "customer.subscription.deleted",
    ):
        handle_subscription_updated(data)
