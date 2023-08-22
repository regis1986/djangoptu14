from django.db import models

import uuid

class Author(models.Model):
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavarde', max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name}  {self.first_name}'

class Book(models.Model):
    title = models.CharField('Pavadinimas', max_length=200)
    summary = models.TextField('Aprašymas', max_length=1000)
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Simbolių <a href="https://lt.wikipedia.org/wiki/ISBN"> ISBN kodas</a>')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField('Genre', help_text='Išsirinkite žanrą(us)')

    def __str__(self):
        return self.title

class Genre(models.Model):
    name = models.CharField('Pavadinimas', max_length=25, help_text='Sukurkite žanrą')

    def __str__(self):
        return self.name

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    due_back = models.DateField('Bus prieinama', null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota')
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Kopijos statusas'
    )
    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} {self.book.title} {self.book.author}'

