from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from main.views import NewsItemListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', NewsItemListView.as_view(), name="news_item_list")
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
