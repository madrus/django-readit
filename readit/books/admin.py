from django.contrib import admin
from .models import Author, Book

@admin.register(Book) # register decorator
class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Book Details", {"fields": ["title", "authors"]}),
        ("Review", {"fields": ["is_favourite", "review", "reviewed_by", "date_reviewed"]}),
    ]

    readonly_fields = ("date_reviewed", )

    # create a function for a custom field
    def book_authors(self, book):
        return book.list_authors()

    book_authors.short_description = "Author(s)"

    list_display = ("title", "book_authors", "date_reviewed", "is_favourite", ) # displayed columns
    list_editable = ("is_favourite", ) # boolean becomes a checkbox
    list_display_links = ("title", "date_reviewed", ) # sort columns
    list_filter = ("is_favourite", ) # selection filter
    search_fields = ("title", "authors__name", ) # extra selection filter

# Register your models here.
admin.site.register(Author)
