"""
Context processors for making data available in all templates
"""
from .models import Profile


def site_context(request):
    """
    Добавляет профиль и другую общую информацию во все шаблоны
    """
    profile = Profile.objects.first()
    
    return {
        'profile': profile,
        'site_name': 'Максудов Абдурахман',
        'site_description': 'Врач-уролог высшей категории',
    }

