from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Plan
from subscription.webhooks import dispatch_stripe_event
from .stripe_checkout import create_checkout_session
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def start_checkout(request, slug):
    """
    Starts Stripe Checkout for a selected plan.
    """
    plan = get_object_or_404(Plan, slug=slug)

    if plan.price == 0:
        messages.error(request, "Free plan does not require checkout.")
        return redirect("/")

    try:
        session = create_checkout_session(user=request.user, plan=plan)
        return redirect(session.url)

    except Exception as exc:
        error = messages.error(request, str(exc))
        print(error)
        return redirect("/")



def checkout_success(request):
    return render(request, "subscription/success.html")


def checkout_cancel(request):
    return render(request, "subscription/cancel.html")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except Exception:
        return HttpResponse(status=400)

    dispatch_stripe_event(event)
    print(f"Stripe Event: {event['type']}")
    return HttpResponse(status=200)


@login_required
def pricing_view(request):
    plans = Plan.objects.all().order_by("price")

    subscription = getattr(request.user, "usersubscription", None)
    current_plan = subscription.plan if subscription else None

    context = {
        "plans": plans,
        "current_plan": current_plan,
    }

    return render(request, "subscription/pricing.html", context)