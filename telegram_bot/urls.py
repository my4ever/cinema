from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('yougotmsg/', csrf_exempt(views.telegram_data), name='message_from_telegram')
]
