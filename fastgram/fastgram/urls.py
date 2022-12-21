from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('homepage.urls', namespace='homepage')),
    path('admin/', admin.site.urls),
    path('delivery/', include('delivery.urls', namespace='delivery')),
    path('users/', include('users.urls', namespace='users')),
    path('feedback/', include('feedback.urls', namespace='feedback')),
    path('response/', include('response.urls', namespace='response')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__', include(debug_toolbar.urls))
    ]
