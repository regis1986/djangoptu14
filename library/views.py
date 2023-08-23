from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Author, Genre, BookInstance


def index(request):
    num_boks = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    context_t = {
        'num_books_t': num_boks,
        'num_instances_t': num_instances
    }

    return render(request, 'index.html', context=context_t)

