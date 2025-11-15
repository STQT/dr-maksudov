from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Profile(models.Model):
    """Профиль уролога"""
    full_name = models.CharField('ФИО', max_length=255)
    photo = models.ImageField('Фото профиля', upload_to='profile/', blank=True, null=True)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    education = models.TextField('Образование')
    academic_degree = models.CharField('Ученая степень', max_length=255, blank=True)
    academic_title = models.CharField('Ученое звание', max_length=255, blank=True)
    bio = models.TextField('Биография')
    specialization = models.TextField('Специализация')
    experience_years = models.IntegerField('Лет опыта', default=0)
    languages = models.CharField('Языки', max_length=255, help_text='Через запятую')
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=50)
    address = models.TextField('Адрес', blank=True)
    clinic_name = models.CharField('Название клиники', max_length=255, blank=True)
    clinic_address = models.TextField('Адрес клиники', blank=True)
    working_hours = models.TextField('Часы работы', blank=True)
    linkedin = models.URLField('LinkedIn', blank=True)
    facebook = models.URLField('Facebook', blank=True)
    instagram = models.URLField('Instagram', blank=True)
    telegram = models.URLField('Telegram', blank=True)
    researchgate = models.URLField('ResearchGate', blank=True)
    orcid = models.CharField('ORCID', max_length=19, blank=True, help_text='ORCID ID (например: 0000-0000-0000-0000)')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    
    def __str__(self):
        return self.full_name


class Service(models.Model):
    """Услуги уролога"""
    title = models.CharField('Название услуги', max_length=255)
    description = RichTextUploadingField('Описание', blank=True)
    duration = models.CharField('Длительность', max_length=100, blank=True)
    icon = models.CharField('CSS класс иконки', max_length=100, default='fas fa-user-doctor')
    is_active = models.BooleanField('Активна', default=True)
    order = models.IntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'pk': self.pk})


class ServiceImage(models.Model):
    """Изображения для услуг (галерея)"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images', verbose_name='Услуга')
    image = models.ImageField('Изображение', upload_to='services/gallery/')
    alt_text = models.CharField('Альтернативный текст', max_length=255, blank=True)
    order = models.IntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Изображение услуги'
        verbose_name_plural = 'Изображения услуг'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.service.title} - Изображение {self.order}"


class ServiceReview(models.Model):
    """Отзывы по услугам"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews', verbose_name='Услуга')
    patient_name = models.CharField('Имя пациента', max_length=255)
    patient_age = models.IntegerField('Возраст пациента', blank=True, null=True)
    text = models.TextField('Текст отзыва')
    rating = models.IntegerField('Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    is_approved = models.BooleanField('Одобрен', default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Отзыв по услуге'
        verbose_name_plural = 'Отзывы по услугам'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.service.title} - {self.patient_name}"


class Publication(models.Model):
    """Публикации"""
    PUBLICATION_TYPES = [
        ('article', 'Статья'),
        ('book', 'Книга'),
        ('chapter', 'Глава в книге'),
        ('conference', 'Конференция'),
        ('thesis', 'Диссертация'),
    ]
    
    title = models.CharField('Название', max_length=500)
    publication_type = models.CharField('Тип публикации', max_length=20, choices=PUBLICATION_TYPES, default='article')
    authors = models.TextField('Авторы', help_text='ФИО авторов через запятую')
    year = models.IntegerField('Год публикации')
    publisher = models.CharField('Издатель', max_length=255, blank=True)
    journal = models.CharField('Журнал', max_length=255, blank=True)
    volume = models.CharField('Том', max_length=50, blank=True)
    pages = models.CharField('Страницы', max_length=50, blank=True)
    doi = models.CharField('DOI', max_length=255, blank=True)
    isbn = models.CharField('ISBN', max_length=50, blank=True)
    link = models.URLField('Ссылка', blank=True)
    abstract = models.TextField('Аннотация', blank=True)
    keywords = models.CharField('Ключевые слова', max_length=500, blank=True, help_text='Через запятую')
    citation_count = models.IntegerField('Цитирования', default=0)
    pdf_file = models.FileField('PDF файл', upload_to='publications/', blank=True, null=True)
    is_featured = models.BooleanField('Избранная', default=False)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-year', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.year})"
    
    def get_absolute_url(self):
        return reverse('publication_detail', kwargs={'pk': self.pk})


class Project(models.Model):
    """Проекты и исследования"""
    title = models.CharField('Название проекта', max_length=500)
    description = models.TextField('Описание')
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания', blank=True, null=True)
    role = models.CharField('Роль в проекте', max_length=255)
    organization = models.CharField('Организация', max_length=255)
    funding = models.CharField('Финансирование', max_length=255, blank=True)
    results = models.TextField('Результаты', blank=True)
    image = models.ImageField('Изображение', upload_to='projects/', blank=True, null=True)
    is_active = models.BooleanField('Активный', default=True)
    order = models.IntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-start_date', 'order']
    
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.end_date is None


class BlogPost(models.Model):
    """Блог/Статьи"""
    title = models.CharField('Заголовок', max_length=500)
    slug = models.SlugField('URL slug', max_length=500, unique=True, blank=True)
    content = RichTextUploadingField('Содержание', config_name='default')
    excerpt = models.TextField('Краткое описание', max_length=500, blank=True)
    featured_image = models.ImageField('Изображение', upload_to='blog/', blank=True, null=True)
    category = models.CharField('Категория', max_length=100, blank=True)
    tags = models.CharField('Теги', max_length=500, blank=True, help_text='Через запятую')
    views_count = models.IntegerField('Просмотры', default=0)
    is_published = models.BooleanField('Опубликовано', default=True)
    published_at = models.DateTimeField('Дата публикации', blank=True, null=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Статья блога'
        verbose_name_plural = 'Статьи блога'
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])


class ServiceOrder(models.Model):
    """Заказ услуги"""
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')
    full_name = models.CharField('Имя пациента', max_length=255)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=50)
    age = models.IntegerField('Возраст', validators=[MinValueValidator(1), MaxValueValidator(150)], default=30, help_text='Обязательное поле')
    message = models.TextField('Описание проблемы', blank=True)
    preferred_date = models.DateField('Предпочтительная дата', default='2024-01-01')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    admin_notes = models.TextField('Заметки администратора', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Заказ услуги'
        verbose_name_plural = 'Заказы услуг'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.service.title} - {self.full_name} ({self.get_status_display()})"


class Achievement(models.Model):
    """Достижения и награды"""
    title = models.CharField('Название', max_length=500)
    description = models.TextField('Описание')
    date = models.DateField('Дата')
    organization = models.CharField('Организация', max_length=255)
    certificate_image = models.ImageField('Изображение сертификата', upload_to='achievements/', blank=True, null=True)
    order = models.IntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'
        ordering = ['-date', 'order']
    
    def __str__(self):
        return f"{self.title} ({self.date.year})"


class Testimonial(models.Model):
    """Отзывы пациентов"""
    patient_name = models.CharField('Имя пациента', max_length=255)
    patient_age = models.IntegerField('Возраст', blank=True, null=True)
    patient_photo = models.ImageField('Фото пациента', upload_to='testimonials/', blank=True, null=True)
    text = models.TextField('Текст отзыва')
    rating = models.IntegerField('Рейтинг', validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    is_approved = models.BooleanField('Одобрен', default=False)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.patient_name} - {self.rating}/5"


class ContactMessage(models.Model):
    """Сообщения из контактной формы"""
    name = models.CharField('Имя', max_length=255)
    email = models.EmailField('Email')
    subject = models.CharField('Тема', max_length=255)
    message = models.TextField('Сообщение')
    is_read = models.BooleanField('Прочитано', default=False)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class Book(models.Model):
    """Книги"""
    title = models.CharField('Название книги', max_length=500)
    slug = models.SlugField('URL slug', max_length=500, unique=True, blank=True)
    author = models.CharField('Автор(ы)', max_length=500, default='Максудов А.А.')
    description = RichTextUploadingField('Описание', config_name='default')
    short_description = models.TextField('Краткое описание', max_length=500, blank=True)
    cover_image = models.ImageField('Обложка', upload_to='books/covers/')
    pdf_file = models.FileField('PDF файл', upload_to='books/pdfs/', blank=True, null=True, help_text='PDF файл книги для просмотра')
    
    publisher = models.CharField('Издательство', max_length=255, blank=True)
    publication_year = models.IntegerField('Год издания')
    isbn = models.CharField('ISBN', max_length=50, blank=True)
    pages = models.IntegerField('Количество страниц', blank=True, null=True)
    language = models.CharField('Язык', max_length=50, default='Русский')
    
    price = models.CharField(
        'Цена', 
        max_length=100, 
        blank=True,
        default='',
        help_text='Укажите цену в сумах (например, "100000") или "Договорная"'
    )
    is_available = models.BooleanField('Доступна для заказа', default=True)
    
    views_count = models.IntegerField('Просмотры', default=0)
    is_featured = models.BooleanField('Избранная', default=False)
    order = models.IntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-is_featured', 'order', '-publication_year']
    
    def __str__(self):
        return f"{self.title} ({self.publication_year})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])


class BookOrder(models.Model):
    """Заказ книги"""
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    full_name = models.CharField('Имя клиента', max_length=255)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=50)
    address = models.TextField('Адрес доставки')
    quantity = models.IntegerField('Количество', default=1, validators=[MinValueValidator(1)])
    message = models.TextField('Дополнительные пожелания', blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    admin_notes = models.TextField('Заметки администратора', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Заказ книги'
        verbose_name_plural = 'Заказы книг'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.book.title} - {self.full_name} ({self.get_status_display()})"
    
    def get_total_price(self):
        if self.book.price and self.book.price.isdigit():
            return int(self.book.price) * self.quantity
        return None

