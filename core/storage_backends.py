"""
Custom storage backends for Cloudflare R2 с правильным кешированием
"""

from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """
    Storage for static files on Cloudflare R2
    Статические файлы кешируются на 1 год (они версионируются через collectstatic)
    """
    location = 'static'
    default_acl = None
    file_overwrite = True
    
    object_parameters = {
        'CacheControl': 'public, max-age=31536000, immutable',
        'ContentDisposition': 'inline',
    }
    
    gzip = True
    gzip_content_types = (
        'text/css',
        'text/javascript',
        'application/javascript',
        'application/x-javascript',
        'image/svg+xml',
        'application/json',
    )


class MediaStorage(S3Boto3Storage):
    """
    Storage for media files on Cloudflare R2
    Медиа файлы кешируются на 30 дней (могут обновляться)
    """
    location = 'media'
    default_acl = None
    file_overwrite = False
    
    object_parameters = {
        'CacheControl': 'public, max-age=2592000',
        'ContentDisposition': 'inline',
    }
    
    gzip = True
    gzip_content_types = (
        'text/css',
        'text/javascript',
        'application/javascript',
        'application/pdf',
        'image/svg+xml',
    )

