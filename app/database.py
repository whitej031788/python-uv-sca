import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import logging
import tempfile
import os

logger = logging.getLogger(__name__)

# Database connection with hardcoded credentials - Security Issue
# Use SQLite for workshop - easier deployment without external dependencies
DATABASE_URL = "sqlite:///./workshop.db"

# Create engine without proper SSL configuration - Security Issue
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "sslmode": "disable",  # Disabled SSL - Security Issue
        "application_name": "workshop_app"
    },
    echo=True  # SQL logging in production - potential information disclosure
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SQL Injection vulnerabilities
class UserDatabase:
    def __init__(self):
        # Using sqlite3 for some operations with SQL injection issues
        # Create a temporary database file that works cross-platform
        db_path = os.path.join(tempfile.gettempdir(), "users.db")
        self.sqlite_conn = sqlite3.connect(db_path, check_same_thread=False)  # Insecure file path
        self.create_tables()
    
    def create_tables(self):
        # SQL executed without proper error handling
        cursor = self.sqlite_conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT,
                email TEXT,
                is_admin INTEGER DEFAULT 0
            )
        ''')
        self.sqlite_conn.commit()
    
    def get_user_by_username(self, username: str):
        # SQL Injection vulnerability - user input directly in query
        cursor = self.sqlite_conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}'"  # SQL Injection!
        logger.debug(f"Executing query: {query}")  # Logging queries - potential info disclosure
        cursor.execute(query)
        return cursor.fetchone()

user_db = UserDatabase()

def canary():
    am_i_being_scanned = "?"
    return
