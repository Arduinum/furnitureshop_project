import random
from django.shortcuts import render, get_object_or_404
from mainapp.models import Product, ProductCategory
from basketapp.models import Basket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product(category_name):
    if category_name == 'все':
        products = Product.objects.filter(is_deleted=False, category__is_active=True)
    else:
        products = Product.objects.filter(is_deleted=False, category=category_name, category__is_active=True)
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category, is_deleted=False, category__is_active=True)\
        .exclude(pk=hot_product.pk)

    return same_products


def products(request, pk=None, page=1):
    title = 'продукты/каталог'

    links_menu = ProductCategory.objects.filter(is_active=True)
    products = Product.objects.filter(is_deleted=False).order_by('price')

    if pk is not None:
        if pk == 0:
            products = Product.objects.filter(is_deleted=False).order_by('price')
            category = {'pk': 0, 'name': 'все'}
            hot_product = get_hot_product(category['name'])
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(is_deleted=False, category__pk=pk).order_by('price')
            hot_product = get_hot_product(category)

        paginator = Paginator(products, 2)

        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        same_products = get_same_products(hot_product)

        context = {
            'title': title,
            'links_menu': links_menu,
            'products': products_paginator,
            'category': category,
            'same_products': same_products,
            'hot_product': hot_product

        }

        return render(request=request, template_name='mainapp/products.html', context=context)
    else:
        hot_product = get_hot_product('все')
        same_products = get_same_products(hot_product)

        context = {
            'title': title,
            'links_menu': links_menu,
            'products': products.filter(category__is_active=True)[:4],
            'same_products': same_products[:3],
            'hot_product': hot_product
        }
        print(products)
        return render(request=request, template_name='mainapp/products.html', context=context)


def product(request, pk):

    context = {
        'title': 'продукты',
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user)
    }

    return render(request=request, template_name='mainapp/product.html', context=context)
