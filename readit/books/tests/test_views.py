import django
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from books.factories import AuthorFactory, BookFactory, ReviewFactory
from books.views import list_books

class ListBooksTest(TestCase):
    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        django.setup()
        super(ListBooksTest, cls).setUpClass()

    def test_list_books_url(self):
        url = resolve('/')
        self.assertEqual(url.func, list_books)

    def test_list_books_template(self):
        response = self.client.get(reverse(list_books))
        self.assertTemplateUsed(response, 'list.html')

    def test_list_books_returns_books_with_reviews(self):
        # Arrange
        author = AuthorFactory()
        books_with_reviews = ReviewFactory.create_batch(2, authors=[author,]) # with reviews
        books_without_reviews = BookFactory.create_batch(4, authors=[author,]) # without reviews
        # Act
        response = self.client.get(reverse(list_books))
        books = list(response.context['books'])
        # Assert
        self.assertEqual(books_with_reviews, books)
        self.assertNotEqual(books_without_reviews, books)