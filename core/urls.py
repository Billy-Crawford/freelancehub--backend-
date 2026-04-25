# core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/missions/', include('missions.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/', include('reviews.urls')),
    path("api/chat/", include("chat.urls")),
    path("api/payments/", include("payments.urls")),
    path("api/reviews/", include("reviews.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

