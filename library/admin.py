from django.contrib import admin

from . models import Author, Book, Genre, BookInstance


class BooksInstanceInLine(admin.TabularInline):
    model = BookInstance
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    search_fields = ('title', 'author__last_name')
    inlines = [BooksInstanceInLine]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'id', 'status', 'due_back', 'reader')
    list_editable = ('status', 'due_back', 'reader') # redaguojami laukai
    list_filter = ('status', 'due_back')
    search_fields = ('id', 'book__title')

    fieldsets = (
        ('General', {'fields': ('id', 'book')}),
        ('Availability', {'fields': ('status', 'due_back', 'reader')}),
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'display_books')


admin.site.register(Genre)
