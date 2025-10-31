from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Profile, Service, ServiceImage, ServiceReview, Publication, Project, BlogPost,
    ServiceOrder, Achievement, Testimonial, ContactMessage,
    Book, BookOrder
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'experience_years', 'updated_at']
    search_fields = ['full_name', 'email', 'specialization']
    list_filter = ['academic_degree', 'created_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('full_name', 'photo', 'birth_date', 'email', 'phone', 'address')
        }),
        ('Клиника', {
            'fields': ('clinic_name', 'clinic_address', 'working_hours')
        }),
        ('Образование и квалификация', {
            'fields': ('education', 'academic_degree', 'academic_title', 'specialization', 'experience_years', 'languages')
        }),
        ('Биография', {
            'fields': ('bio',)
        }),
        ('Социальные сети', {
            'fields': ('linkedin', 'facebook', 'instagram', 'telegram'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'order']
    ordering = ['order', 'title']


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'publication_type', 'year', 'citation_count', 'is_featured', 'created_at']
    list_filter = ['publication_type', 'year', 'is_featured']
    search_fields = ['title', 'authors', 'keywords', 'abstract']
    list_editable = ['is_featured']
    ordering = ['-year', 'title']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'publication_type', 'authors', 'year')
        }),
        ('Детали публикации', {
            'fields': ('publisher', 'journal', 'volume', 'pages', 'doi', 'isbn')
        }),
        ('Дополнительная информация', {
            'fields': ('abstract', 'keywords', 'citation_count', 'link', 'pdf_file', 'is_featured')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'start_date', 'end_date', 'is_ongoing_display', 'is_active', 'order']
    list_filter = ['is_active', 'start_date', 'organization']
    search_fields = ['title', 'description', 'organization', 'role']
    list_editable = ['is_active', 'order']
    ordering = ['-start_date', 'order']
    date_hierarchy = 'start_date'
    
    def is_ongoing_display(self, obj):
        if obj.is_ongoing:
            return format_html('<span style="color: green;">✓ В процессе</span>')
        return format_html('<span style="color: gray;">Завершен</span>')
    is_ongoing_display.short_description = 'Статус'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'views_count', 'published_at']
    list_filter = ['is_published', 'category', 'created_at']
    search_fields = ['title', 'excerpt', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
    date_hierarchy = 'published_at'
    ordering = ['-published_at', '-created_at']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'tags', 'featured_image')
        }),
        ('Содержание', {
            'fields': ('excerpt', 'content'),
            'description': 'Используйте редактор для форматирования текста'
        }),
        ('Настройки публикации', {
            'fields': ('is_published', 'published_at', 'views_count'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['views_count']
    
    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.css',)
        }


@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ['service', 'full_name', 'email', 'phone', 'age', 'status', 'preferred_date', 'created_at']
    list_filter = ['status', 'service', 'created_at']
    search_fields = ['full_name', 'email', 'phone', 'message']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Услуга', {
            'fields': ('service', 'status', 'preferred_date')
        }),
        ('Информация о пациенте', {
            'fields': ('full_name', 'email', 'phone', 'age')
        }),
        ('Запрос', {
            'fields': ('message',)
        }),
        ('Административная информация', {
            'fields': ('admin_notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('service')


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'date', 'order', 'created_at']
    list_filter = ['date', 'organization']
    search_fields = ['title', 'description', 'organization']
    list_editable = ['order']
    ordering = ['-date', 'order']
    date_hierarchy = 'date'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'patient_age', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['patient_name', 'text']
    list_editable = ['is_approved']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Информация о пациенте', {
            'fields': ('patient_name', 'patient_age', 'patient_photo')
        }),
        ('Отзыв', {
            'fields': ('text', 'rating', 'is_approved')
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Отправитель', {
            'fields': ('name', 'email', 'subject')
        }),
        ('Сообщение', {
            'fields': ('message',)
        }),
        ('Статус', {
            'fields': ('is_read', 'created_at')
        }),
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_year', 'price', 'is_available', 'is_featured', 'views_count']
    list_filter = ['is_available', 'is_featured', 'publication_year', 'language']
    search_fields = ['title', 'author', 'description', 'isbn']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_available', 'is_featured', 'price']
    ordering = ['-is_featured', 'order', '-publication_year']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'cover_image', 'pdf_file')
        }),
        ('Описание', {
            'fields': ('short_description', 'description'),
        }),
        ('Издательская информация', {
            'fields': ('publisher', 'publication_year', 'isbn', 'pages', 'language'),
        }),
        ('Цена и доступность', {
            'fields': ('price', 'is_available'),
        }),
        ('Настройки отображения', {
            'fields': ('is_featured', 'order', 'views_count'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs


@admin.register(BookOrder)
class BookOrderAdmin(admin.ModelAdmin):
    list_display = ['book', 'full_name', 'email', 'phone', 'quantity', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['book__title', 'full_name', 'email', 'phone', 'address']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at', 'get_total_price']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Книга', {
            'fields': ('book', 'quantity', 'get_total_price')
        }),
        ('Информация о клиенте', {
            'fields': ('full_name', 'email', 'phone', 'address')
        }),
        ('Запрос', {
            'fields': ('message',)
        }),
        ('Административная информация', {
            'fields': ('status', 'admin_notes', 'created_at', 'updated_at'),
        }),
    )
    
    def get_total_price(self, obj):
        """Отображение общей стоимости"""
        total = obj.get_total_price()
        if total:
            return f"{total} сум"
        return "Цена не указана"
    get_total_price.short_description = 'Общая стоимость'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('book')


@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ['service', 'order', 'alt_text', 'created_at']
    list_filter = ['created_at']
    search_fields = ['service__title', 'alt_text']
    list_editable = ['order']
    ordering = ['service', 'order']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('service', 'image', 'alt_text', 'order')
        }),
    )


@admin.register(ServiceReview)
class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ['service', 'patient_name', 'patient_age', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['service__title', 'patient_name', 'text']
    list_editable = ['is_approved']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Информация о пациенте', {
            'fields': ('service', 'patient_name', 'patient_age')
        }),
        ('Отзыв', {
            'fields': ('text', 'rating', 'is_approved')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('service')

