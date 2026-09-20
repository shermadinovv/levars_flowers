from .models import Category, SiteSettings


def site_context(request):
    """Данные, доступные во всех шаблонах: настройки сайта и категории для меню."""
    return {
        'site': SiteSettings.load(),
        'nav_categories': Category.objects.all(),
    }
