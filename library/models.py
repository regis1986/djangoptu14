from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from datetime import  date
import uuid
from tinymce.models import HTMLField
from PIL import Image

class Author(models.Model):
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavarde', max_length=100)
    # description = models.TextField('Aprašymas', max_length=2000, default='Labai geras autorius')
    description = HTMLField()

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name}  {self.first_name}'

    def display_books(self):
        return ', '.join(book.title for book in self.books.all()[:3])

    display_books.short_Description = 'Knygos'

    def get_absolute_url(self):
        return reverse('author-one', args=[str(self.id)])


class Book(models.Model):
    title = models.CharField('Pavadinimas', max_length=200)
    summary = models.TextField('Aprašymas', max_length=1000)
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Simbolių <a href="https://lt.wikipedia.org/wiki/ISBN"> ISBN kodas</a>')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, related_name='books')
    genre = models.ManyToManyField('Genre', help_text='Išsirinkite žanrą(us)')
    cover = models.ImageField('Viršelis', upload_to='covers', null=True, blank=True)

    def __str__(self):
        return self.title

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:2])

    display_genre.short_description = 'Žanras'

    def get_absolute_url(self):
        return reverse('book-one', args=[str(self.id)])


class Genre(models.Model):
    name = models.CharField('Pavadinimas', max_length=25, help_text='Sukurkite žanrą')

    class Meta:
        verbose_name = 'Žanras'
        verbose_name_plural = 'Žanrai'

    def __str__(self):
        return self.name

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='bookinstance_set')
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
    reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        else:
            return False
    class Meta:
        ordering = ['due_back']

    def __str__(self):
        # return f'{self.id} {self.book.title} {self.book.author}'
        return f'{self.id}'


class BookReview(models.Model):
    content = models.TextField('Atsiliepimas', max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='bookreview_set', blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.content


class Profilis(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, blank=True)
    nuotrauka = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} profilis'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if (img.height > 300) or (img.width > 300):
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)


