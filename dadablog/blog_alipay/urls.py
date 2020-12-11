from django.urls import path
from . import views


urlpatterns = [
    path('payment/url', views.OrderView.as_view()),
    path('payment/result', views.ResultView.as_view()),
]
