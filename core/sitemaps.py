from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import BlogPost, Publication, Book


class StaticViewSitemap(Sitemap):
    """Sitemap для статических страниц"""
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['index', 'about', 'services', 'portfolio', 'publications', 'books', 'blog', 'contact']

    def location(self, item):
        return reverse(item)


class BlogPostSitemap(Sitemap):
    """Sitemap для статей блога"""
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class PublicationSitemap(Sitemap):
    """Sitemap для публикаций"""
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Publication.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class BookSitemap(Sitemap):
    """Sitemap для книг"""
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Book.objects.filter(is_available=True)

    def lastmod(self, obj):
        return obj.updated_at

