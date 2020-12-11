from django.urls import path
from . import views

urlpatterns = [
    path('sms', views.sms_views),
    path('<str:username>', views.UserViews.as_view()),
    path('<str:username>/avatar', views.user_views),


]