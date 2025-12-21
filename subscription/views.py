from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from .models import Plan
from .stripe_checkout import create_checkout_session


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