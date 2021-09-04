from django.shortcuts import render
from mainapp.models import Product


def products(request, pk=None):
    title = 'продукты/каталог'

    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'}
    ]

    products = Product.objects.all()[:4]

    products_similar = Product.objects.all()[:3]

    context = {
        'title': title,
        'links_menu': links_menu,
        'products': products,
        'products_similar': products_similar
    }

    return render(request=request, template_name='products.html', context=context)
