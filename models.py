# models.py

import sqlite3
from pydantic import BaseModel
from typing import List

# Database connection function
def db_connection():
    conn = sqlite3.connect('movies.db')
    return conn

# Movie model
class Movie(BaseModel):
    id: int
    title: str
    year: int
    director_id: int

# Movie input model (for creation)
class MovieIn(BaseModel):
    title: str
    year: int
    director_id: int

# Director model
class Director(BaseModel):
    id: int
    name: str
    nationality: str

# Director input model (for creation)
class DirectorIn(BaseModel):
    name: str
    nationality: str

# Function to create database tables
def create_tables():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        year INTEGER NOT NULL,
        director_id INTEGER NOT NULL,
        FOREIGN KEY (director_id) REFERENCES directors (id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS directors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        nationality TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Function to delete database tables
def delete_tables():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS movies")
    cursor.execute("DROP TABLE IF EXISTS directors")
    conn.commit()
    conn.close()
