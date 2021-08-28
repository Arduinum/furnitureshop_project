from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def contacts(request):
    return render(request, 'contacts.html')







