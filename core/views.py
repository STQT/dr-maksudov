from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, HttpResponseServerError
from .models import (
    Profile, Service, ServiceImage, ServiceReview, Publication, Project, BlogPost,
    Achievement, Testimonial, Book, BookOrder
)
from .forms import ServiceOrderForm, ContactForm, BookOrderForm


def index(request):
    """Главная страница"""
    profile = Profile.objects.first()
    services = Service.objects.filter(is_active=True)[:6]
    publications = Publication.objects.filter(is_featured=True)[:3]
    testimonials = Testimonial.objects.filter(is_approved=True)[:3]
    blog_posts = BlogPost.objects.filter(is_published=True)[:3]
    books = Book.objects.filter(is_featured=True, is_available=True)[:3]
    
    context = {
        'profile': profile,
        'services': services,
        'publications': publications,
        'testimonials': testimonials,
        'blog_posts': blog_posts,
        'books': books,
    }
    return render(request, 'index.html', context)


def about(request):
    """О враче"""
    profile = Profile.objects.first()
    achievements = Achievement.objects.all()[:10]
    
    context = {
        'profile': profile,
        'achievements': achievements,
    }
    return render(request, 'about.html', context)


def services(request):
    """Услуги"""
    services_list = Service.objects.filter(is_active=True)
    
    context = {
        'services': services_list,
    }
    return render(request, 'services.html', context)


def service_detail(request, pk):
    """Детальная страница услуги"""
    service = get_object_or_404(Service, pk=pk, is_active=True)
    images = ServiceImage.objects.filter(service=service).order_by('order')
    reviews = ServiceReview.objects.filter(service=service, is_approved=True).order_by('-created_at')[:10]
    
    # Форма заказа
    if request.method == 'POST':
        form = ServiceOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.service = service
            order.save()
            
            # Отправка email
            try:
                send_mail(
                    f'Новый заказ услуги: {service.title}',
                    f'Получен новый заказ услуги "{service.title}"\n\n'
                    f'Пациент: {order.full_name}\n'
                    f'Email: {order.email}\n'
                    f'Телефон: {order.phone}\n'
                    f'Возраст: {order.age}\n'
                    f'Желаемая дата: {order.preferred_date}\n'
                    f'Сообщение: {order.message}',
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
            except:
                pass
            
            messages.success(request, 'Ваш заказ успешно отправлен! Мы свяжемся с вами в ближайшее время.')
            return redirect('service_detail', pk=pk)
    else:
        initial_data = {'service': service.id}
        form = ServiceOrderForm(initial=initial_data)
    
    context = {
        'service': service,
        'images': images,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'service_detail.html', context)


def portfolio(request):
    """Портфолио - проекты"""
    projects_list = Project.objects.filter(is_active=True)
    
    # Фильтрация
    status = request.GET.get('status')
    if status == 'ongoing':
        projects_list = projects_list.filter(end_date__isnull=True)
    elif status == 'completed':
        projects_list = projects_list.filter(end_date__isnull=False)
    
    context = {
        'projects': projects_list,
    }
    return render(request, 'portfolio.html', context)


def publications(request):
    """Публикации"""
    publications_list = Publication.objects.all()
    
    # Фильтрация
    pub_type = request.GET.get('type')
    if pub_type:
        publications_list = publications_list.filter(publication_type=pub_type)
    
    year = request.GET.get('year')
    if year:
        publications_list = publications_list.filter(year=year)
    
    # Поиск
    search = request.GET.get('search')
    if search:
        publications_list = publications_list.filter(
            Q(title__icontains=search) |
            Q(authors__icontains=search) |
            Q(keywords__icontains=search)
        )
    
    # Пагинация
    paginator = Paginator(publications_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Получаем уникальные годы для фильтра
    years = Publication.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    context = {
        'page_obj': page_obj,
        'years': years,
        'current_type': pub_type,
        'current_year': year,
        'search_query': search,
    }
    return render(request, 'publications.html', context)


def publication_detail(request, pk):
    """Детальная страница публикации"""
    publication = get_object_or_404(Publication, pk=pk)
    
    context = {
        'publication': publication,
    }
    return render(request, 'publication_detail.html', context)


def blog(request):
    """Блог"""
    posts_list = BlogPost.objects.filter(is_published=True)
    
    # Фильтрация по категории
    category = request.GET.get('category')
    if category:
        posts_list = posts_list.filter(category=category)
    
    # Фильтрация по тегу
    tag = request.GET.get('tag')
    if tag:
        posts_list = posts_list.filter(tags__icontains=tag)
    
    # Пагинация
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Получаем уникальные категории
    categories = BlogPost.objects.filter(is_published=True).values_list('category', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category,
    }
    return render(request, 'blog.html', context)


def blog_detail(request, slug):
    """Детальная страница статьи блога"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    post.increment_views()
    
    # Похожие статьи
    related_posts = BlogPost.objects.filter(
        is_published=True,
        category=post.category
    ).exclude(pk=post.pk)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog_detail.html', context)


def contact(request):
    """Контакты"""
    profile = Profile.objects.first()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Отправка email администратору
            try:
                send_mail(
                    subject=f'Новое сообщение: {contact_message.subject}',
                    message=f'От: {contact_message.name} ({contact_message.email})\n\n{contact_message.message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email error: {e}")
            
            messages.success(request, 'Спасибо! Ваше сообщение успешно отправлено.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'contact.html', context)


def order_service(request, service_id=None):
    """Заказ услуги"""
    initial_data = {}
    if service_id:
        service = get_object_or_404(Service, pk=service_id, is_active=True)
        initial_data['service'] = service
    
    if request.method == 'POST':
        form = ServiceOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            
            # Отправка email администратору
            try:
                age_info = f"Возраст: {order.age} лет\n" if order.age else ""
                send_mail(
                    subject=f'Новый заказ услуги: {order.service.title}',
                    message=f'Пациент: {order.full_name}\nEmail: {order.email}\nТелефон: {order.phone}\n{age_info}\nОписание проблемы: {order.message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
                
                # Отправка подтверждения пациенту
                send_mail(
                    subject='Подтверждение записи на прием',
                    message=f'Здравствуйте, {order.full_name}!\n\nВаша заявка на услугу "{order.service.title}" принята. Мы свяжемся с вами в ближайшее время для подтверждения записи.\n\nС уважением,\nД-р Максудов Абдурахман',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[order.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email error: {e}")
            
            messages.success(request, 'Спасибо! Ваша заявка успешно отправлена. Мы свяжемся с вами в ближайшее время.')
            return redirect('services')
    else:
        form = ServiceOrderForm(initial=initial_data)
    
    context = {
        'form': form,
    }
    return render(request, 'order_service.html', context)


def custom_404(request, exception):
    """Custom 404 error page"""
    return HttpResponseNotFound(render(request, '404.html', status=404))


def custom_500(request):
    """Custom 500 error page"""
    return HttpResponseServerError(render(request, '500.html', status=500))


def books(request):
    """Список книг"""
    books_list = Book.objects.filter(is_available=True)
    
    # Фильтрация по году
    year = request.GET.get('year')
    if year:
        books_list = books_list.filter(publication_year=year)
    
    # Пагинация
    paginator = Paginator(books_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Получаем уникальные годы для фильтра
    years = Book.objects.values_list('publication_year', flat=True).distinct().order_by('-publication_year')
    
    context = {
        'page_obj': page_obj,
        'years': years,
        'current_year': year,
    }
    return render(request, 'books.html', context)


def book_detail(request, slug):
    """Детальная страница книги"""
    book = get_object_or_404(Book, slug=slug, is_available=True)
    book.increment_views()
    
    # Похожие книги (по автору или году)
    related_books = Book.objects.filter(
        is_available=True
    ).filter(
        models.Q(author=book.author) | models.Q(publication_year=book.publication_year)
    ).exclude(pk=book.pk)[:3]
    
    context = {
        'book': book,
        'related_books': related_books,
    }
    return render(request, 'book_detail.html', context)


def order_book(request, book_id=None):
    """Заказ книги"""
    initial_data = {}
    if book_id:
        book = get_object_or_404(Book, pk=book_id, is_available=True)
        initial_data['book'] = book
    
    if request.method == 'POST':
        form = BookOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            
            # Отправка email администратору
            try:
                total_price = order.get_total_price()
                price_info = f"Общая стоимость: {total_price} ₽" if total_price else "Цена не указана"
                
                send_mail(
                    subject=f'Новый заказ книги: {order.book.title}',
                    message=f'Клиент: {order.full_name}\nEmail: {order.email}\nТелефон: {order.phone}\nАдрес: {order.address}\nКоличество: {order.quantity}\n{price_info}\n\nДополнительно: {order.message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
                
                # Отправка подтверждения клиенту
                send_mail(
                    subject='Подтверждение заказа книги',
                    message=f'Здравствуйте, {order.full_name}!\n\nВаш заказ книги "{order.book.title}" (количество: {order.quantity}) принят. Мы свяжемся с вами в ближайшее время для уточнения деталей доставки.\n\n{price_info}\n\nС уважением,\nД-р Максудов Абдурахман',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[order.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email error: {e}")
            
            messages.success(request, f'Спасибо! Ваш заказ книги "{order.book.title}" успешно оформлен. Мы свяжемся с вами в ближайшее время.')
            return redirect('books')
    else:
        form = BookOrderForm(initial=initial_data)
    
    context = {
        'form': form,
    }
    return render(request, 'order_book.html', context)

