from django.utils import timezone
from django.contrib.auth.models import User

from subscription.models import UserSubscription, Plan


def handle_checkout_completed(session):
    email = session["customer_details"]["email"]
    customer_id = session["customer"]
    subscription_id = session["subscription"]

    user = User.objects.get(email=email)

    user_sub, _ = UserSubscription.objects.get_or_create(user=user)
    user_sub.stripe_customer_id = customer_id
    user_sub.stripe_subscription_id = subscription_id
    user_sub.is_active = True
    user_sub.save()


def handle_subscription_updated(subscription):
    customer_id = subscription["customer"]
    price_id = subscription["items"]["data"][0]["price"]["id"]
    period_end = subscription["current_period_end"]

    user_sub = UserSubscription.objects.get(
        stripe_customer_id=customer_id
    )

    plan = Plan.objects.get(stripe_pid=price_id)

    user_sub.plan = plan
    user_sub.active_until = timezone.datetime.fromtimestamp(
        period_end, tz=timezone.utc
    )
    user_sub.is_active = subscription["status"] == "active"
    user_sub.save()


def handle_subscription_deleted(subscription):
    customer_id = subscription["customer"]

    user_sub = UserSubscription.objects.get(
        stripe_customer_id=customer_id
    )

    user_sub.is_active = False
    user_sub.active_until = None
    user_sub.save()
