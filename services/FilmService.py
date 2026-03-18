import json
import os
from typing import List, Optional, Dict, Any

from models.Film import Film
from exceptions.DuplicateFilmError import DuplicateFilmError
from exceptions.FilmNotFoundError import FilmNotFoundError
from exceptions.InvalidInputError import InvalidInputError
from validator.Validator import Validator


class FilmService:
    def __init__(self, filename: Optional[str] = "my_films.json") -> None:
        os.makedirs("data", exist_ok=True)
        self.filename = os.path.join("data", filename)

        self.films: Dict[int, Film] = {}
        self.load_from_file()

    def save_to_file(self) -> None:
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([film.to_dict() for film in self.films.values()], f, ensure_ascii=False, indent=4)

    def load_from_file(self) -> None:
        if not os.path.exists(self.filename):
            return
        with open(self.filename, "r", encoding="utf-8") as f:
            films_data = json.load(f)
            for data in films_data:
                film = Film.from_dict(data)
                self.films[film.id] = film
            if self.films:
                Film._id_counter = max(f.id for f in self.films.values()) + 1

    def add_film(
            self,
            title: str,
            director: str,
            year: int,
            genre: str,
            status: str = "unwatched",
            rating: Optional[int] = None,
            description: str = ""
    ) -> Film:
        for f in self.films.values():
            if f.title.lower() == title.strip().lower() and f.year == year:
                raise DuplicateFilmError(f"Film '{title}' z rokiem {year} już istnieje.")

        Validator.validate_title(title)
        Validator.validate_director(director)
        valid_year = Validator.validate_year(year)
        Validator.validate_genre(genre)
        status = Validator.validate_status(status)
        valid_rating = Validator.validate_rating(rating)

        film = Film(title, director, valid_year, genre, status, valid_rating, description)
        self.films[film.id] = film
        self.save_to_file()
        return film

    def remove_film(self, film_id: int) -> Film:
        if film_id in self.films:
            removed = self.films.pop(film_id)
            self.save_to_file()
            return removed
        else:
            raise FilmNotFoundError(f"Film o ID {film_id} nie został znaleziony.")

    def edit_film(self, film_id: int, **kwargs: Any) -> Film:
        film = self.get_film_by_id(film_id)
        allowed_fields = {"title", "director", "year", "genre", "status", "rating", "description"}
        for key, value in kwargs.items():
            if key not in allowed_fields:
                raise InvalidInputError(f"Niedozwolona właściwość do edycji -> {key}")
            setattr(film, key, value)

        film.validate()
        self.save_to_file()
        return film

    def add_comment_to_film(self, film_id: int, comment: str) -> Film:
        film = self.get_film_by_id(film_id)
        film.add_comment(comment)
        self.save_to_file()
        return film

    def get_film_by_id(self, film_id: int) -> Film:
        if film_id in self.films:
            return self.films[film_id]
        raise FilmNotFoundError(f"Film o ID {film_id} nie znaleziony.")

    def find_films_by_title(self, term: str) -> List[Film]:
        term_lower = term.lower()
        return [film for film in self.films.values() if term_lower in film.title.lower()]

    def list_all_films(self) -> List[Film]:
        return list(self.films.values())

    def mark_film_as_watched(self, film_id: int, history_service: Any) -> Film:
        film = self.get_film_by_id(film_id)
        film.status = "watched"
        film.add_watch_date()
        history_service.add_watch_date(film_id)
        self.save_to_file()
        return film