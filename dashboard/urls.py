from django.urls import path
from . import views

urlpatterns = [
    path("backtest_view/", views.backtest_view, name="backtest-view"),
    path("backtest_post/", views.backtest_post, name="backtest-post"),
    path("backtest_detail/<int:run_id>/", views.backtest_detail, name="backtest-detail"),
]