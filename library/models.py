from django.db import models

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
    isbn = models.CharField('ISBN', max_length=13)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField('Genre')

    def __str__(self):
        return  self.title

class Genre(models.Model):
    name = models.CharField('Pavadinimas', max_length=25)

    def __str__(self):
        return self.name