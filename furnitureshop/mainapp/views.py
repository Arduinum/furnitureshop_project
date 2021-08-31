from django.shortcuts import render


def products(request):
    title = 'продукты'
    context = {
        'title': title
    }

    return render(request, 'products.html', context=context)
