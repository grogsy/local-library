from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Author, Genre, Book, BookInstance, Language

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

class BookInline(admin.TabularInline):
    model = Book

# Register your models here.
# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(Genre)
# admin.site.register(BookInstance)
# admin.site.register(Language)

admin.site.register(Permission)

# another way to register models to admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'display_genre')
    inlines = [BookInstanceInline]
    search_fields = ['title']

    fieldsets = (
        ('Book Info', {
            'fields': ('title', 'author', 'summary')
        }),
        ('Meta Info', {
            'fields': ('isbn', 'genre', 'image_url')
        })
    )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death', 'age')
    fields = ['first_name', 'last_name', 'bio', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]
    search_fields = ['first_name', 'last_name']

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back', 'language')
    list_display = ('book', 'id', 'language', 'status', 'borrower')
    search_fields = ['id', 'book__title', 'borrower__username']

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id', 'language')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # automatically generate the slug when creating a new genre model object
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass