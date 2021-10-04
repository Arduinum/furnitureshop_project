from django.http import HttpResponseRedirect
from django.urls import reverse
from adminapp.forms import ShopUserAdminEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from adminapp.forms import ProductCategoryEditForm, ProductEditForm
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@user_passes_test(lambda u: u.is_superuser)
def users(request, page=1):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    paginator = Paginator(users_list, 2)

    try:
        users_paginator = paginator.page(page)
    except PageNotAnInteger:
        users_paginator = paginator.page(1)
    except EmptyPage:
        users_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'users': users_paginator,
        'users_page': users_paginator
    }

    return render(request=request, template_name='adminapp/users.html', context=context)


def user_create(request):
    title = 'пользователи/создать'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()

            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        user_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'user_form': user_form
    }

    return render(request=request, template_name='adminapp/user_create.html', context=context)


def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)

    http_old = request.META.get('HTTP_REFERER')

    page_number = 1

    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()

            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    if 'page' in http_old:
        page_number = http_old.split('/')[-2]

    context = {
        'title': title,
        'user_form': edit_form,
        'page_number': page_number
    }

    return render(request=request, template_name='adminapp/user_update.html', context=context)


def user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_deleted = True
        user.is_active = False
        user.save()

        return HttpResponseRedirect(reverse('admin_staff:users'))

    context = {
        'title': title,
        'user_to_delete': user
    }

    return render(request=request, template_name='adminapp/user_delete.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request, page=1):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    paginator = Paginator(categories_list, 2)

    try:
        categories_paginator = paginator.page(page)
    except PageNotAnInteger:
        categories_paginator = paginator.page(1)
    except EmptyPage:
        categories_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'categories': categories_paginator,
        'categories_page': categories_paginator
    }

    return render(request=request, template_name='adminapp/categories.html', context=context)


def category_create(request):
    title = 'категории/создать'

    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES)

        if category_form.is_valid():
            category_form.save()

            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        category_form = ProductCategoryEditForm()

    context = {
        'title': title,
        'category_form': category_form
    }

    return render(request=request, template_name='adminapp/category_create.html', context=context)


def category_update(request, pk, page=1):
    title = 'категории/редактирование'

    category = get_object_or_404(ProductCategory, pk=pk)

    http_old = request.META.get('HTTP_REFERER')

    page_number = 1

    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES, instance=category)
        if category_form.is_valid():
            category_form.save()

            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        category_form = ProductCategoryEditForm(instance=category)

    if 'page' in http_old:
        page_number = http_old.split('/')[-2]

    context = {
        'title': title,
        'category_form': category_form,
        'page_number': page_number
    }

    return render(request=request, template_name='adminapp/category_update.html', context=context)


def category_delete(request, pk):
    title = 'категории/удаление'

    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        category.is_deleted = True
        category.is_active = False
        category.save()

        return HttpResponseRedirect(reverse('admin_staff:categories'))

    context = {
        'title': title,
        'category_to_delete': category
    }

    return render(request=request, template_name='adminapp/category_delete.html', context=context)


def products(request, pk, page=1):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)

    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    paginator = Paginator(products_list, 2)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'category': category,
        'products': products_paginator,
        'products_page': products_paginator
    }

    return render(request=request, template_name='adminapp/products.html', context=context)


def product_create(request, pk):
    title = 'продукты/создать'

    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()

            return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    context = {
        'title': title,
        'product_form': product_form,
        'category': category
    }

    return render(request=request, template_name='adminapp/product_create.html', context=context)


def product_read(request, pk):
    title = 'продукты/подробнее'

    product = get_object_or_404(Product, pk=pk)

    context = {
        'title': title,
        'product': product
    }

    return render(request=request, template_name='adminapp/product_read.html', context=context)


def product_update(request, pk, page=1):
    title = 'продукты/редактирование'

    product = get_object_or_404(Product, pk=pk)

    http_old = request.META.get('HTTP_REFERER')

    page_number = 1

    category_pk = None

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()

            return HttpResponseRedirect(reverse('admin_staff:product_update', args=[product.pk]))
    else:
        product_form = ProductEditForm(instance=product)

    if 'page' in http_old:
        page_number = http_old.split('/')[-2]
        category_pk = http_old.split('/')[-4]
    else:
        category_pk = http_old.split('/')[-2]

    context = {
        'title': title,
        'product_form': product_form,
        'product': product,
        'page_number': page_number,
        'category_pk': category_pk
    }

    return render(request=request, template_name='adminapp/product_update.html', context=context)


def product_delete(request, pk):
    title = 'продукт/удаление'

    product_to_delete = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_to_delete.is_deleted = True
        product_to_delete.save()

        return HttpResponseRedirect(reverse('admin_staff:products', args=[product_to_delete.category.pk]))

    context = {
        'title': title,
        'product_to_delete': product_to_delete
    }

    return render(request=request, template_name='adminapp/product_delete.html', context=context)
