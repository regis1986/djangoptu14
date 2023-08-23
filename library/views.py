from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Author, Genre, BookInstance


def index(request):
    num_boks = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()
    num_authors = Author.objects.count()

    context_t = {
        'num_books_t': num_boks,
        'num_instances_t': num_instances,
        'num_instances_available_t': num_instances_available,
        'num_authors_t': num_authors
    }

    return render(request, 'index.html', context=context_t)

