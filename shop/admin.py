from django.contrib import admin

from .models import Banner, Category, Product, SiteSettings


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'in_stock', 'is_new', 'is_bestseller', 'order')
    list_editable = ('category', 'price', 'in_stock', 'is_new', 'is_bestseller', 'order')
    list_filter = ('category', 'in_stock', 'is_new')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_editable = ('is_active', 'order')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False