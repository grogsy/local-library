from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name="author-detail"),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
    path('loaned/', views.LoanedBooksListView.as_view(), name='all-loaned'),
    path('books/category/<str:category>', views.FilteredByGenreBookListView.as_view(), name='books-by-genre')
]