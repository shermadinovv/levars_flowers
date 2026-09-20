from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Адрес (slug)', unique=True)
    image = models.ImageField('Иконка (для главной страницы)', upload_to='categories/', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Адрес (slug)', unique=True)
    description = models.TextField('Описание', blank=True)
    price = models.PositiveIntegerField('Цена')
    old_price = models.PositiveIntegerField('Старая цена', null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT,
        related_name='products', verbose_name='Категория',
    )
    image = models.ImageField('Фото', upload_to='products/')
    in_stock = models.BooleanField('В наличии', default=True)
    is_new = models.BooleanField('Новинка', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])


class Banner(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    subtitle = models.CharField('Подзаголовок', max_length=300, blank=True)
    image = models.ImageField('Картинка', upload_to='banners/')
    button_text = models.CharField('Текст кнопки', max_length=50, blank=True)
    link = models.CharField('Ссылка кнопки', max_length=300, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Показывать', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    whatsapp = models.CharField(
        'Номер WhatsApp', max_length=20,
        help_text='Только цифры, с кодом страны, без "+" и пробелов',
    )
    currency = models.CharField(
        'Валюта', max_length=10, blank=True,
        help_text='Показывается после цены, например: сом, ₽, $',
    )
    phone = models.CharField('Телефон для показа', max_length=30, blank=True)
    address = models.CharField('Адрес', max_length=300, blank=True)
    working_hours = models.CharField('Часы работы', max_length=100, blank=True)
    instagram = models.URLField('Instagram', blank=True)

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def save(self, *args, **kwargs):
        self.pk = 1  # всегда одна запись
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'Настройки сайта'
