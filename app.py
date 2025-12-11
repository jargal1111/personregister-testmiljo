import sqlite3
import os

def init_database(silent=False):
    """Sätter upp databasen och skapar tabellen 'users' om den saknas
    
    Args:
        silent (bool): Om True, skriv inte ut meddelanden (användbart vid testning)
    """
    db_path = os.getenv("DATABASE_PATH", "/data/test_users.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Skapa tabellen om den inte redan finns
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    # Kolla om det finns några användare i tabellen
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    # Fyll på med testdata om databasen är tom
    if total_users == 0:
        initial_users = [
            ("Anna Andersson", "anna@test.se"),
            ("Bo Bengtsson", "bo@test.se")
        ]

        cur.executemany(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            initial_users
        )
        if not silent:
            print("Databasen har initierats med testanvändare.")
    else:
        if not silent:
            print(f"Det finns redan {total_users} användare i databasen.")

    conn.commit()
    conn.close()


def display_users():
    """Visar alla användare i databasen"""
    db_path = os.getenv("DATABASE_PATH", "/data/test_users.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()

    print("\nAnvändare i databasen:")
    for uid, name, email in rows:
        print(f"ID: {uid}, Namn: {name}, E-post: {email}")

    conn.close()


def clear_test_data(silent=False):
    """GDPR: Tar bort samtliga användare från tabellen
    
    Args:
        silent (bool): Om True, skriv inte ut meddelanden
    """
    db_path = os.getenv("DATABASE_PATH", "/data/test_users.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("DELETE FROM users")
    conn.commit()
    conn.close()

    if not silent:
        print("All testdata har raderats (GDPR-anpassat).")


def anonymize_data(silent=False):
    """GDPR: Anonymiserar både namn och e-post
    
    Args:
        silent (bool): Om True, skriv inte ut meddelanden
    """
    db_path = os.getenv("DATABASE_PATH", "/data/test_users.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET name = 'Anonym Användare',
            email = 'anonym@anonym.se'
    """)
    
    conn.commit()
    conn.close()

    if not silent:
        print("Alla namn och e-postadresser har anonymiserats (GDPR-anpassat).")


if __name__ == "__main__":
    # När filen körs direkt, visa utskrifter
    init_database()
    display_users()

    print("\nContainern körs. Tryck Ctrl+C för att avsluta.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nStänger ner...")