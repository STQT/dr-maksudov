from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('publications/', views.publications, name='publications'),
    path('publications/<int:pk>/', views.publication_detail, name='publication_detail'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('books/', views.books, name='books'),
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path('contact/', views.contact, name='contact'),
    path('order/', views.order_service, name='order_service'),
    path('order/<int:service_id>/', views.order_service, name='order_service_direct'),
    path('order-book/', views.order_book, name='order_book'),
    path('order-book/<int:book_id>/', views.order_book, name='order_book_direct'),
]

