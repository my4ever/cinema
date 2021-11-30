from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('movies.urls')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('bot/', include('telegram_bot.urls')),
]
