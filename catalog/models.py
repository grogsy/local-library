import uuid
from datetime import date

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

# https://media.prod.mdn.mozit.cloud/attachments/2019/02/09/16479/e26dc9174dd40f177acaca19a33b4667/local_library_model_uml.png

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(default="No bio given yet.")
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        return reverse('catalog:author-detail', args=[str(self.id)])

    def age(self):
        try:
            td = self.date_of_death - self.date_of_birth
            age_in_days = td.days
            return int(age_in_days // 365.25)
        except:
            return None


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Enter a book genre(e.g. Science Fiction)"
    )
    slug = models.SlugField(max_length=40)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Language(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Written Language"
    )

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200, default="http://www.newdesignfile.com/postpic/2015/02/funny-no-image-available-icon_68017.jpg")

    author = models.ForeignKey(
        Author, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='books'
    )

    summary = models.TextField(
        help_text="Enter a brief description about the book"
    )

    isbn = models.CharField(
        'ISBN',
        max_length=13,
        help_text="13 Character <a href='https://www.isbn-international.org/content/what-isbn'>ISBN number</a>"
    )

    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

class BookInstance(models.Model):
    """The BookInstance represents a specific copy of a book that someone might borrow, 
     and includes information about whether the copy is available or on what date it is expected back, 
     "imprint" or version details, and a unique id for the book in the library."""

    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned', "Set book as returned"),)

    id = models.UUIDField(
         primary_key=True,
         default=uuid.uuid4,
         help_text='Unique ID for this particular copy across the whole library'
     )

    book = models.ForeignKey(
         Book,
         on_delete=models.SET_NULL,
         null=True,
         related_name='copies'
    )

    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    language = models.ForeignKey(
        Language, 
        help_text="Select language this book is written in", 
        on_delete=models.SET_NULL,
        null=True
    )

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability'
    )

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='loaned_books')


    def __str__(self):
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        return True if (self.due_back and date.today() > self.due_back) else False