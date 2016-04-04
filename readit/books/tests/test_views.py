import django
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from books.factories import AuthorFactory, BookFactory, ReviewFactory, UserFactory
from books.models import Book
from books.views import list_books, ReviewList

# Functional view test
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

# Class view test
class ReviewListTest(TestCase):
    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        django.setup()
        super(ReviewListTest, cls).setUpClass()

    def setUp(self):
        self.user = UserFactory(username="test")
        self.author = AuthorFactory()

    def test_reviews_url(self):
        url = resolve('/review/')
        self.assertEqual(url.func.__name__, ReviewList.__name__)

    def test_authentication_control(self):
        # check unauthenticated users cannot view page
        response = self.client.get(reverse('review-books'))
        self.assertEqual(response.status_code, 302)
        # check authenticated users can view page
        self.client.login(username="test", password="test")
        response = self.client.get(reverse('review-books'))
        self.assertEqual(response.status_code, 200)
        # while we're here, confirm we're using the correct template
        self.assertTemplateUsed(response, 'list-to-review.html')

    def test_review_list_returns_books_to_review(self):
        books_without_reviews = BookFactory.create_batch(2, authors=[self.author,])
        self.client.login(username="test", password="test")
        response = self.client.get(reverse('review-books'))
        books = list(response.context['books'])
        self.assertEqual(books, books_without_reviews)

    def test_can_create_new_book(self):
        self.client.login(username="test", password="test")
        response = self.client.post(
            reverse('review-books'),
            data={
                'title': 'My Brand New Book',
                'authors': [self.author.pk,],
                'reviewed_by': self.user.pk,
            }
        )

        self.assertIsNotNone(Book.objects.get(title="My Brand New Book"))
