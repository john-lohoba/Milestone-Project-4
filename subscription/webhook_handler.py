from django.utils import timezone
from django.contrib.auth.models import User

from subscription.models import UserSubscription, Plan


def handle_checkout_completed(session):
    metadata = session.get("metadata", {})

    user_id = metadata.get("user_id")
    plan_id = metadata.get("plan_id")

    if not user_id or not plan_id:
        return

    user = User.objects.get(id=user_id)
    plan = Plan.objects.get(id=plan_id)

    UserSubscription.objects.update_or_create(
        user=user,
        defaults={
            "plan": plan,
            "stripe_customer_id": session["customer"],
            "stripe_subscription_id": session["subscription"],
            "is_active": True,
            "active_until": None,
        },
    )



def handle_subscription_updated(subscription):
    subscription_id = subscription["id"]
    status = subscription["status"]

    try:
        user_sub = UserSubscription.objects.get(
            stripe_subscription_id=subscription_id
        )
    except UserSubscription.DoesNotExist:
        return

    user_sub.is_active = status == "active"
    user_sub.save(update_fields=["is_active"])



def handle_subscription_deleted(subscription):
    customer_id = subscription["customer"]

    user_sub = UserSubscription.objects.get(
        stripe_customer_id=customer_id
    )

    user_sub.is_active = False
    user_sub.active_until = None
    user_sub.save()
