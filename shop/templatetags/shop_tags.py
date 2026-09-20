from urllib.parse import quote

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def whatsapp_url(context, product=None):
    """Ссылка на чат в WhatsApp. С товаром: в сообщение подставляются название, цена и ссылка."""
    site = context.get('site')
    number = ''.join(ch for ch in (site.whatsapp if site else '') if ch.isdigit())
    if not number:
        return '#'

    if product is None:
        text = 'Здравствуйте! Хочу сделать заказ.'
    else:
        request = context.get('request')
        link = request.build_absolute_uri(product.get_absolute_url()) if request else ''
        price = f'{product.price} {site.currency}'.strip()
        text = f'Здравствуйте! Хочу заказать: {product.name} — {price}\n{link}'.strip()

    return f'https://wa.me/{number}?text={quote(text)}'
