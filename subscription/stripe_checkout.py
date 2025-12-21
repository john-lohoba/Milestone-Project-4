import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(*, user, plan):
    """
    Creates a Stripe Checkout Session for a subscription plan.
    """

    if not plan.stripe_price_id:
        raise ValueError("Plan does not have a Stripe Price ID")

    # Reuse Stripe customer if it exists
    customer_id = None
    if hasattr(user, "usersubscription") and user.usersubscription.stripe_customer_id:
        customer_id = user.usersubscription.stripe_customer_id

    session = stripe.checkout.Session.create(
        mode="subscription",
        customer=customer_id,
        payment_method_types=["card"],
        line_items=[
            {
                "price": plan.stripe_price_id,
                "quantity": 1,
            }
        ],
        success_url=f"{settings.DOMAIN}/subscription/success/",
        cancel_url=f"{settings.DOMAIN}/subscription/cancel/",
        allow_promotion_codes=True,
        metadata={
            "user_id": user.id,
            "plan_id": plan.id,
        }
    )

    return session
