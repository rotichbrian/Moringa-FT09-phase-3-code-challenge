import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_db_connection
from database.setup import create_tables

conn = get_db_connection()
cursor = conn.cursor()

class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name should be a string and between 2 - 16 characters")
        self._name = name
        self._category = category
        # uncomment the self.save() to automatically save the initialized data in the database
        # self.save()

    def __repr__(self):
        return f'<Magazine {self._name}>'

    def save(self):
        cursor.execute("SELECT id FROM magazines WHERE id = ?", (self._id,))
        if cursor.fetchone():
            raise ValueError(f"Magazine with id {self._id} already exists")
        sql = """
             INSERT INTO magazines (
             id, name, category)  
             VALUES (?, ?, ?)  
            """
        cursor.execute(sql, (self._id, self._name, self._category))
        conn.commit()

    def articles(self):
        query = """
              SELECT articles.title
              FROM articles
              LEFT JOIN magazines
              ON articles.magazine_id = magazines.id
              WHERE magazines.id = ?
        """
        cursor.execute(query, (self._id,))
        articles = cursor.fetchall()
        return [article[0] for article in articles] if articles else None

    def contributors(self):
        sql = """
          SELECT authors.name
          FROM authors
          LEFT JOIN articles
          ON authors.id = articles.author_id
          LEFT JOIN magazines
          ON articles.magazine_id = magazines.id
          WHERE magazines.id = ?
        """
        cursor.execute(sql, (self._id,))
        contributors = cursor.fetchall()
        return [contributor[0] for contributor in contributors] if contributors else None

    def article_titles(self):
        sql = """
            SELECT articles.title
            FROM articles
            WHERE articles.magazine_id = ?
        """
        cursor.execute(sql, (self._id,))
        article_titles = cursor.fetchall()
        return [article_title[0] for article_title in article_titles] if article_titles else None

    def contributing_authors(self):
        sql = """
            SELECT authors.name
            FROM authors
            LEFT JOIN articles 
            ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(articles.id) > 2
        """
        print("SQL Query:", sql)
        cursor.execute(sql, (self._id,))
        contributing_authors = cursor.fetchall()
        return [contributing_author[0] for contributing_author in contributing_authors] if contributing_authors else None


    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if not isinstance(id, int):
            raise TypeError("ID must be an integer")
        self._id = id

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = value