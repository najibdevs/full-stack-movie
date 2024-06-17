# app.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Union  # Import Union from typing module
from pydantic import BaseModel
from models import Movie, MovieIn, Director, DirectorIn, create_tables, delete_tables, db_connection

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your front-end URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
create_tables()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# CRUD operations for movies
@app.get("/movies", response_model=List[Movie])
def get_movies():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "title": row[1], "year": row[2], "director_id": row[3]} for row in movies]

@app.post("/movies", response_model=Movie)
def create_movie(movie: MovieIn):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO movies (title, year, director_id) VALUES (?, ?, ?)", (movie.title, movie.year, movie.director_id))
    conn.commit()
    movie_id = cursor.lastrowid
    conn.close()
    return {"id": movie_id, **movie.dict()}

@app.put("/movies/{movie_id}", response_model=Movie)
def update_movie(movie_id: int, movie: MovieIn):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE movies SET title = ?, year = ?, director_id = ? WHERE id = ?", (movie.title, movie.year, movie.director_id, movie_id))
    conn.commit()
    conn.close()
    return {"id": movie_id, **movie.dict()}

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    conn.commit()
    conn.close()
    return {"message": "Movie deleted"}

# CRUD operations for directors
@app.get("/directors", response_model=List[Director])
def get_directors():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM directors")
    directors = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "name": row[1], "nationality": row[2]} for row in directors]

@app.post("/directors", response_model=Director)
def create_director(director: DirectorIn):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO directors (name, nationality) VALUES (?, ?)", (director.name, director.nationality))
    conn.commit()
    director_id = cursor.lastrowid
    conn.close()
    return {"id": director_id, **director.dict()}

@app.put("/directors/{director_id}", response_model=Director)
def update_director(director_id: int, director: DirectorIn):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE directors SET name = ?, nationality = ? WHERE id = ?", (director.name, director.nationality, director_id))
    conn.commit()
    conn.close()
    return {"id": director_id, **director.dict()}

@app.delete("/directors/{director_id}")
def delete_director(director_id: int):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM directors WHERE id = ?", (director_id,))
    conn.commit()
    conn.close()
    return {"message": "Director deleted"}
