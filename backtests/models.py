from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from strategies.models import Strategy

# Create your models here.


class BacktestRun(models.Model):
    STATUS_QUEUED = "queued"
    STATUS_RUNNING = "running"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_QUEUED, "Queued"),
        (STATUS_RUNNING, "Running"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_FAILED, "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="backtests")
    strategy = models.ForeignKey(
        Strategy, on_delete=models.PROTECT, related_name="backtests"
    )
    parameters = models.JSONField()
    symbol = models.CharField(max_length=20)
    timeframe = models.CharField(max_length=10, default="1d")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_QUEUED
    )
    error_message = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    started_on = models.DateTimeField(blank=True, null=True)
    finished_on = models.DateTimeField(blank=True, null=True)

    def mark_running(self):
        self.status = self.STATUS_RUNNING
        self.started_on = now()
        self.save(update_fields=["status", "started_on"])

    def mark_completed(self):
        self.status = self.STATUS_COMPLETED
        self.finished_on = now()
        self.save(update_fields=["status", "finished_on"])

    def mark_failed(self, message=""):
        self.status = self.STATUS_FAILED
        self.error_message = message
        self.finished_on = now()
        self.save(update_fields=["status", "error_message", "finished_on"])

    def __str__(self):
        return f"{self.user} - {self.strategy.name} ({self.pk})"
