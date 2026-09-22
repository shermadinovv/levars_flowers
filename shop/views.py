from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Banner, Category, Product

PER_PAGE = 4

SORTS = {
    'new': ('-created_at',),
    'price_asc': ('price', 'pk'),
    'price_desc': ('-price', 'pk'),
}


def home(request):
    context = {
        'banners': Banner.objects.filter(is_active=True),
        'categories': Category.objects.all(),
        'products': Product.objects.select_related('category').order_by('-is_new', '-created_at')[:6],
    }
    return render(request, 'shop/index.html', context)


def catalog(request):
    products = Product.objects.select_related('category')
    top_sellers = Product.objects.filter(is_bestseller=True).select_related('category')[:3]

    current_category = None
    slug = request.GET.get('category', '').strip()
    if slug:
        current_category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=current_category)

    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    sort = request.GET.get('sort', '')
    if sort in SORTS:
        products = products.order_by(*SORTS[sort])

    page_obj = Paginator(products, PER_PAGE).get_page(request.GET.get('page'))

    params = request.GET.copy()
    params.pop('page', None)

    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'current_category': current_category,
        'query': query,
        'sort': sort,
        'querystring': params.urlencode(),
        'top_sellers': top_sellers,
    }
    return render(request, 'shop/catalog.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related('category'), slug=slug)
    related = (
        Product.objects.filter(category=product.category)
        .exclude(pk=product.pk)[:3]
    )
    return render(request, 'shop/product_detail.html', {'product': product, 'related': related})
