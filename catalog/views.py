import datetime

from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from catalog.models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm

# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'catalog/index.html', context=context)

class BookListView(ListView):
    model = Book
    template_name = 'catalog/book_list.html'
    paginate_by = 10

class FilteredByGenreBookListView(ListView):
    model = Book
    template_name = 'catalog/book_list.html'

    def get_queryset(self):
        category = self.kwargs.get('category')
        books = Book.objects.filter(genre__slug=category)
        print(books)
        return books

    # queryset = Book.objects.filter(genre__name=self.kwargs.get('category').title())

class BookDetailView(DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'

class AuthorListView(ListView):
    model = Author
    template_name = 'catalog/author_list.html'

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    context_object_name = 'copies'
    template_name = 'catalog/loaned_books_by_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user
        ).filter(
            status__exact='o'
        ).order_by('due_back')

class LoanedBooksListView(PermissionRequiredMixin, ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    context_object_name = 'copies'
    template_name = 'catalog/loaned_books.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date =  datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance
    }

    return render(request, 'catalog/book_renew_librarian.html', context=context)