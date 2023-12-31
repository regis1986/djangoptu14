from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors-all'),
    path('authors/<int:author_id>', views.author, name='author-one'),
    path('books/', views.BookListView.as_view(), name='books-all'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-one'),
    path('search/', views.search, name='search-name'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('register/', views.register, name='register-url'),
    path('profilis/', views.profilis, name='profilis-url'),
    path('mybooks/new', views.BookbyUserCreateView.as_view(), name='my-borrowed-new'),
    path('mybooks/<uuid:pk>/update',views.BookByUserUpdateView.as_view(), name='my-borrowed-update'),
    path('mybooks/<uuid:pk>/delete', views.BookByUserDeleteView.as_view(), name='my-borrowed-delete')


    ]