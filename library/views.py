from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import generic
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Book, Author, Genre, BookInstance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()
    num_authors = Author.objects.count()

    username = request.user

    # kaupiam apsilankymų skaičių
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context_t = {
        'num_books_t': num_books,
        'num_instances_t': num_instances,
        'num_instances_available_t': num_instances_available,
        'num_authors_t': num_authors,
        'username_t': username,
        'num_visits_t': num_visits
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

# mano knygos vievsas
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'user_books.html'
    context_object_name = 'bookinstance_list'

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user).order_by('due_back')

@csrf_protect
def register(request):
    if request.method == "POST":
        # paimami duomenys iš formos
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f"Vartotojo vardas {username} užimtas!")
                return redirect('register-url') # jei uzimtas is naujo nukreipoiam i registracija

            else: # tikrinama email, kai praejo password ir ussername patikrinimai
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"Vartotojas su email adresu {email} egzistuoja!")
                    return redirect('register-url') # jei uzimtas is naujo nukreipoiam i registracija
                ####### patikrinimai praeiti
                else:
                    ### sukuriam nauja useri
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.success(request, f'Vartotojas {username} sėkmingai sukurtas')
                    return redirect('login')





    else:
        return render(request, "registration/registration.html")
