import django
from django.test import TestCase
from books.models import Book
from books.factories import AuthorFactory

class BookTest(TestCase):
    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        django.setup()
        super(BookTest, cls).setUpClass()

    # setUp will run before each test
    def setUp(self):
        self.author1 = AuthorFactory(name="Author 1")
        self.author2 = AuthorFactory(name="Author 2")

        self.book = Book(title="MyBook")
        self.book.save()
        self.book.authors.add(self.author1.pk, self.author2.pk)

    # tearDown will run after each test
    def tearDown(self):
        self.author1.delete()
        self.author2.delete()
        self.book.delete()

    # UNIT TESTS
    def test_can_list_authors(self):
        self.assertEqual("Author 1, Author 2", self.book.list_authors())

    def test_string_method(self):
        self.assertEqual("MyBook by Author 1, Author 2", self.book.__str__())

    def test_custom_save_method(self):
        self.assertIsNone(self.book.date_reviewed)
        self.book.review = "My review"
        self.book.save()
        self.assertIsNotNone(self.book.date_reviewed)
