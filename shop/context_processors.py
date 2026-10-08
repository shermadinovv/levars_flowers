from .models import Category, SiteSettings, Store


def site_context(request):
    """Данные, доступные во всех шаблонах: настройки сайта и категории для меню."""
    return {
        'site': SiteSettings.load(),
        'nav_categories': Category.objects.all(),
    }


def site_context(request):
    """Данные, доступные во всех шаблонах: настройки сайта, категории для меню и магазины для футера."""
    return {
        'site': SiteSettings.load(),
        'nav_categories': Category.objects.all(),
        'stores': Store.objects.filter(is_active=True),
    }