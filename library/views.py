from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from django.views import generic
from django.db.models import Q
from django.core.paginator import Paginator
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
    paginator = Paginator(Author.objects.all(), 2)
    page_number = request.GET.get('page')
    page_authors = paginator.get_page(page_number)
    # authors = Author.objects.all()
    # print(authors)
    context_t = {
        'authors_t': page_authors
    }
    return render(request, 'authors.html', context=context_t)


def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)
    context_t = {
        'author_t': single_author
    }
    return render(request, 'author.html', context=context_t)

class BookListView(generic.ListView):
    model = Book # modelioklase_list  -> taip atsiranda pavadinimas book_list
    context_object_name = 'book_list'
    template_name = 'book_list.html'
    paginate_by = 4  # supuslapiuoja po tris eilutes ir i sablona paduodamas page_obj


class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'book_detail.html'

def search(request):
    query = request.GET.get('search_text')
    search_results = Book.objects.filter(
        Q(title__icontains=query) |
        Q(summary__icontains=query)
    )
    context_t = {
        'query_t': query,
        'search_results_t': search_results
    }
    return render(request, 'search.html', context=context_t)
