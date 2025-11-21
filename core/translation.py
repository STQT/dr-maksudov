"""
Modeltranslation configuration for urologist website
Languages: Russian, Uzbek (Latin)
"""
from modeltranslation.translator import translator, TranslationOptions
from .models import (
    Profile, Service, ServiceImage, ServiceReview, Publication, Project, BlogPost,
    Achievement, Testimonial, Book
)


class ProfileTranslationOptions(TranslationOptions):
    fields = ('full_name', 'education', 'bio', 'specialization', 'address', 'clinic_name', 'clinic_address', 'working_hours')
    required_languages = ('ru',)


class ServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    required_languages = ('ru',)


class PublicationTranslationOptions(TranslationOptions):
    fields = ('title', 'authors', 'abstract', 'keywords')
    required_languages = ('ru',)


class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'role', 'organization', 'funding', 'results')
    required_languages = ('ru',)


class BlogPostTranslationOptions(TranslationOptions):
    fields = ('title', 'excerpt', 'content', 'category', 'tags')
    required_languages = ('ru',)


class AchievementTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'organization')
    required_languages = ('ru',)


class TestimonialTranslationOptions(TranslationOptions):
    fields = ('patient_name', 'text')
    required_languages = ('ru',)


class BookTranslationOptions(TranslationOptions):
    fields = ('title', 'author', 'description', 'short_description')
    required_languages = ('ru',)


class ServiceReviewTranslationOptions(TranslationOptions):
    fields = ('patient_name', 'text')
    required_languages = ('ru',)


class ServiceImageTranslationOptions(TranslationOptions):
    fields = ('alt_text',)
    required_languages = ('ru',)


# Register translations
translator.register(Profile, ProfileTranslationOptions)
translator.register(Service, ServiceTranslationOptions)
translator.register(ServiceReview, ServiceReviewTranslationOptions)
translator.register(ServiceImage, ServiceImageTranslationOptions)
translator.register(Publication, PublicationTranslationOptions)
translator.register(Project, ProjectTranslationOptions)
translator.register(BlogPost, BlogPostTranslationOptions)
translator.register(Achievement, AchievementTranslationOptions)
translator.register(Testimonial, TestimonialTranslationOptions)
translator.register(Book, BookTranslationOptions)

