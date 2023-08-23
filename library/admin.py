from django.contrib import admin

from . models import Author, Book, Genre, BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'id', 'status', 'due_back')
    list_filter = ('status', 'due_back')

    fieldsets = (
        ('General', {'fields': ('id', 'book')}),
        ('Availability', {'fields': ('status', 'due_back')}),
    )

admin.site.register(Author)
admin.site.register(Genre)
