from database.connection import get_db_connection

class Article:
    def __init__(self, title, content, author, magazine):
        self.title = title
        self.content = content
        self.author_id = author.id
        self.magazine_id = magazine.id
        self.id = self._create_article()

    def _create_article(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                       (self.title, self.content, self.author_id, self.magazine_id))
        conn.commit()
        article_id = cursor.lastrowid
        conn.close()
        return article_id

    @property
    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (self.author_id,))
        author = cursor.fetchone()
        conn.close()
        return author

    @property
    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (self.magazine_id,))
        magazine = cursor.fetchone()
        conn.close()
        return magazine

    def __repr__(self):
        return f'<Article {self.title}>'
