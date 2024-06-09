import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from database.connection import get_db_connection
from database.setup import create_tables

class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        create_tables()  # Ensure tables are created before running tests
        cls.conn = get_db_connection()
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
        # Clear tables before each test
        self.cursor.execute("DELETE FROM authors")
        self.cursor.execute("DELETE FROM articles")
        self.cursor.execute("DELETE FROM magazines")
        self.conn.commit()

    def test_author_creation(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        article = Article(1, "Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")

    def test_author_save_and_fetch(self):
        author = Author(1, "John Doe")
        author.save()
        self.cursor.execute("SELECT * FROM authors WHERE id = 1")
        saved_author = self.cursor.fetchone()
        self.assertIsNotNone(saved_author)
        self.assertEqual(saved_author["name"], "John Doe")

    def test_article_save_and_fetch(self):
        author = Author(1, "John Doe")
        author.save()
        magazine = Magazine(1, "Tech Weekly", "Technology")
        magazine.save()
        article = Article(1, "Test Title", "Test Content", 1, 1)
        article.save()
        self.cursor.execute("SELECT * FROM articles WHERE id = 1")
        saved_article = self.cursor.fetchone()
        self.assertIsNotNone(saved_article)
        self.assertEqual(saved_article["title"], "Test Title")

    def test_magazine_save_and_fetch(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        magazine.save()
        self.cursor.execute("SELECT * FROM magazines WHERE id = 1")
        saved_magazine = self.cursor.fetchone()
        self.assertIsNotNone(saved_magazine)
        self.assertEqual(saved_magazine["name"], "Tech Weekly")

    def test_article_author_name(self):
        author = Author(1, "John Doe")
        author.save()
        magazine = Magazine(1, "Tech Weekly", "Technology")
        magazine.save()
        article = Article(1, "Test Title", "Test Content", 1, 1)
        article.save()
        self.assertEqual(article.author_name(), "John Doe")

    def test_author_articles(self):
        author = Author(1, "John Doe")
        author.save()
        magazine = Magazine(1, "Tech Weekly", "Technology")
        magazine.save()
        article1 = Article(1, "Test Title 1", "Test Content 1", 1, 1)
        article1.save()
        article2 = Article(2, "Test Title 2", "Test Content 2", 1, 1)
        article2.save()
        self.assertEqual(author.articles(), ["Test Title 1", "Test Title 2"])

    def test_magazine_articles(self):
        author = Author(1, "John Doe")
        author.save()
        magazine = Magazine(1, "Tech Weekly", "Technology")
        magazine.save()
        article1 = Article(1, "Test Title 1", "Test Content 1", 1, 1)
        article1.save()
        article2 = Article(2, "Test Title 2", "Test Content 2", 1, 1)
        article2.save()
        self.assertEqual(magazine.articles(), ["Test Title 1", "Test Title 2"])

    def test_magazine_contributors(self):
        author1 = Author(1, "John Doe")
        author1.save()
        author2 = Author(2, "Jane Smith")
        author2.save()
        magazine = Magazine(1, "Tech Weekly", "Technology")
        magazine.save()
        article1 = Article(1, "Test Title 1", "Test Content 1", 1, 1)
        article1.save()
        article2 = Article(2, "Test Title 2", "Test Content 2", 2, 1)
        article2.save()
        self.assertEqual(magazine.contributors(), ["John Doe", "Jane Smith"])

if __name__ == "__main__":
    unittest.main()