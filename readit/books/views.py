# from django.http import HttpResponse
from django.shortcuts import render
from .models import Book

# Create your views here.
def list_books(request):
    # return HttpResponse("We could put anything here")
    # return HttpResponse(request.user.username)
    """
    List the books that have reviews
    """

    books = Book.objects.exclude(date_reviewed__isnull=True).prefetch_related("authors")

    # context to pass to the render method
    context = {
        'books': books,
    }

    return render(request, "list.html", context)
