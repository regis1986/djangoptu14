from django.shortcuts import render, get_object_or_404
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

def authors(request):
    authors = Author.objects.all()
    # print(authors)
    context_t = {
        'authors_t': authors
    }
    return render(request, 'authors.html', context=context_t)


def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)
    context_t = {
        'author_t': single_author
    }
    return render(request, 'author.html', context=context_t)