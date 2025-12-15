from django.contrib import admin
from .models import BacktestRun, BacktestResult

# Register your models here.
admin.site.register(BacktestRun)
admin.site.register(BacktestResult)
