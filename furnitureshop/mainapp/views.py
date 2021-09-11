from django.shortcuts import render, get_object_or_404
from mainapp.models import Product, ProductCategory


def products(request, pk=None):
    title = 'продукты/каталог'

    links_menu = ProductCategory.objects.all()
    products = Product.objects.all().order_by('price')[:4]

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')[:4]
            category = {'name': 'все'}
        else:
            category = get_object_or_404().order_by('price')
            products = Product.objects.filter(category__pk=pk).order_by('price')[:4]

        context = {
            'title': title,
            'links_menu': links_menu,
            'products': products,
            'category': category
        }

        return render(request=request, template_name='products.html', context=context)

    context = {
        'title': title,
        'links_menu': links_menu,
        'products': products,
        'same_products': Product.objects.all()[3:6]
    }

    return render(request=request, template_name='products.html', context=context)


def product(request, pk):

    context = {
        'title': 'продукты',
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk)
    }

    return render(request=request, template_name='product.html', context=context)