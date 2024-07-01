from database.connection import get_db_connection

class Magazine:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.id = self._create_magazine()

    def _create_magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self.name, self.category))
        conn.commit()
        magazine_id = cursor.lastrowid
        conn.close()
        return magazine_id

    @property
    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    @property
    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        contributors = cursor.fetchall()
        conn.close()
        return contributors

    @property
    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self.id,))
        titles = cursor.fetchall()
        conn.close()
        return [title['title'] for title in titles]

    @property
    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.*, COUNT(articles.id) AS article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        ''', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return authors

    def __repr__(self):
        return f'<Magazine {self.name}>'
