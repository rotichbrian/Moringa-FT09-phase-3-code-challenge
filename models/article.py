import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from database.connection import get_db_connection
from database.setup import create_tables

conn = get_db_connection()
cursor = conn.cursor()


class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string and between 5-50 characters")
        self._title = title
        
        self._id = id
       
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id
        # uncomment the self.save() to automatically save the initialized data in the database
        # self.save()

    def __repr__(self):
        return f'<Article {self.title}>'
    def save (self):
        cursor.execute("SELECT id FROM articles WHERE id = ?", (self._id,))
        if cursor.fetchone():
                raise ValueError(f"Article with id {self._id} already exists")
        sql = """
         INSERT INTO articles (
         id, title, content, author_id, magazine_id)  
         VALUES (?, ?, ?, ?, ?)  
        """
        cursor.execute(sql,(self._id, self._title, self._content, self._author_id, self._magazine_id))
        conn.commit()

    @property
    def title(self):
        return self._title
    def author_name(self):
        

        query = """
                   SELECT authors.name
                   FROM articles
                   LEFT JOIN authors
                   ON articles.author_id = authors.id
                   WHERE articles.id = ?
            """
        cursor.execute(query, (self._id,))
        author = cursor.fetchone()
        return author[0] if author else None
    

    
   