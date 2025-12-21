from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Plan(models.Model):
    """
    Model to store different subscription plan options
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    max_backtests_per_day = models.IntegerField(null=True, blank=True)
    stripe_price_id = models.CharField(max_length=254, null=True, blank=True,)
    stripe_product_id = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    active_until = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def refresh_status(self):
        """
        Auto-update is_active based on active_until.
        """
        current_time = timezone.now()
        self.is_active = (
        self.active_until is not None and self.active_until > current_time)
        self.save(update_fields=["is_active"])