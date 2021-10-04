from django.shortcuts import render
from mainapp.models import Product


def index(request):
    title = 'магазин'
    products = Product.objects.filter(category__is_active=True, is_deleted=False)[:4]
    context = {
        'title': title,
        'products': products
    }

    return render(request=request, template_name='furnitureshop/index.html', context=context)


def contacts(request):
    title = 'контакты'
    context = {
        'title': title
    }

    return render(request=request, template_name='furnitureshop/contacts.html', context=context)
