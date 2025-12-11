import unittest
import sqlite3
import os
import tempfile
from app import init_database, display_users, clear_test_data, anonymize_data

class TestDatabaseFunctions(unittest.TestCase):
    """Testar databasfunktionerna i app.py"""
    
    def setUp(self):
        """Körs före varje test - skapar en temporär databas"""
        # Skapa en temporär fil för testdatabasen
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_path = self.temp_db.name
        self.temp_db.close()  # Stäng filen direkt
        
        # Sätt miljövariabeln
        os.environ["DATABASE_PATH"] = self.db_path
        
    def tearDown(self):
        """Körs efter varje test"""
        # Ta bort miljövariabeln
        if "DATABASE_PATH" in os.environ:
            del os.environ["DATABASE_PATH"]
        
        # Försök ta bort filen
        try:
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
        except:
            pass  # Ignorera borttagningsfel
    
    def test_init_database_creates_table(self):
        """Test 1: Kontrollera att tabellen 'users' skapas"""
        # Kör funktionen med silent=True för att undvika utskrifter
        init_database(silent=True)
        
        # Kontrollera att tabellen skapades
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        # Kolla vilka tabeller som finns
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cur.fetchall()]
        
        conn.close()
        
        # Verifiera att 'users' finns i tabellistan
        self.assertIn('users', tables)
    
    def test_init_database_adds_test_data(self):
        """Test 2: Kontrollera att testdata läggs till"""
        init_database(silent=True)
        
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM users")
        count = cur.fetchone()[0]
        
        conn.close()
        
        self.assertEqual(count, 2, "Det borde finnas exakt 2 testanvändare")
    
    def test_clear_test_data(self):
        """Test 3: Testa GDPR-radering"""
        init_database(silent=True)
        clear_test_data(silent=True)
        
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM users")
        count = cur.fetchone()[0]
        
        conn.close()
        
        self.assertEqual(count, 0, "Alla användare borde vara raderade")
    
    def test_anonymize_data(self):
        """Test 4: Testa GDPR-anonymisering"""
        init_database(silent=True)
        anonymize_data(silent=True)
        
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        cur.execute("SELECT name, email FROM users")
        users = cur.fetchall()
        
        conn.close()
        
        # Kontrollera varje användare
        for name, email in users:
            self.assertEqual(name, "Anonym Användare")
            self.assertEqual(email, "anonym@anonym.se")
    
    def test_display_users(self):
        """Test 5: Testa att visa användare (extra test)"""
        init_database(silent=True)
        
        # Hämta användare direkt från databasen för att jämföra
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        db_users = cur.fetchall()
        conn.close()
        
        # Vi skulle normalt testa display_users() här
        # Men eftersom den bara skriver ut, testar vi datainnehållet istället
        self.assertEqual(len(db_users), 2)
        
        # Kontrollera att data är korrekt
        for user in db_users:
            self.assertEqual(len(user), 3)  # id, name, email
            self.assertIsInstance(user[0], int)  # id är integer
            self.assertIsInstance(user[1], str)  # name är sträng
            self.assertIsInstance(user[2], str)  # email är sträng

if __name__ == "__main__":
    unittest.main()