"""
URL configuration for maksudov_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from core.sitemaps import StaticViewSitemap, BlogPostSitemap, PublicationSitemap, BookSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogPostSitemap,
    'publications': PublicationSitemap,
    'books': BookSitemap,
}

# URLs that should not be localized
urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
]

# Add language prefix to all URLs
urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    prefix_default_language=False,
)

# Serve media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Customize admin site
admin.site.site_header = "Максудов Абдурахман - Администрирование"
admin.site.site_title = "Админ-панель"
admin.site.index_title = "Управление сайтом уролога"

# Custom error handlers
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'

