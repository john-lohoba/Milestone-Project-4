from django.contrib import admin
from .models import Plan, UserSubscription

# Register your models here.
admin.site.register(Plan)
admin.site.register(UserSubscription)