from datetime import datetime, timedelta
from typing import List, Tuple, Optional

from exceptions.FilmNotFoundError import FilmNotFoundError
from validator.Validator import Validator
from models.Film import Film


class WatchHistoryService:
    def __init__(self, film_service):
        self.film_service = film_service

    def add_watch_date(self, film_id: int, date: Optional[datetime] = None) -> None:
        try:
            valid_id = Validator.validate_id(str(film_id))
        except Exception as e:
            raise ValueError(f"Nieprawidłowe ID filmu: {e}")

        try:
            film: Film = self.film_service.get_film_by_id(valid_id)
        except FilmNotFoundError as e:
            raise FilmNotFoundError(f"Film o ID {valid_id} nie istnieje.") from e

        if date is None:
            date = datetime.now()

        if not isinstance(date, datetime):
            raise ValueError("Data musi być typu datetime.")

        updated = False
        if date not in film.watch_dates:
            film.add_watch_date(date)
            updated = True
        if film.status != "watched":
            film.status = "watched"
            updated = True
        if updated:
            self.film_service.save_to_file()
        else:
            print("\nTen film został już obejrzany tego dnia.")

    def get_all_watched_films(self) -> List[Film]:
        return [film for film in self.film_service.list_all_films() if film.watch_dates]

    def clear_watch_history(self, film_id: int) -> None:
        try:
            valid_id = Validator.validate_id(str(film_id))
        except Exception as e:
            raise ValueError(f"Nieprawidłowe ID filmu: {e}")

        try:
            film: Film = self.film_service.get_film_by_id(valid_id)
        except FilmNotFoundError as e:
            raise FilmNotFoundError(f"Film o ID {valid_id} nie istnieje.") from e

        film.watch_dates = []
        film.status = "unwatched"
        self.film_service.save_to_file()

    def get_most_watched_films(self, top_n: int = 5) -> List[Tuple[Film, int]]:
        films = self.get_all_watched_films()
        counted: List[Tuple[Film, int]] = [(film, len(film.watch_dates)) for film in films]
        counted.sort(key=lambda x: x[1], reverse=True)
        return counted[:top_n]

    def get_recently_watched_films(self, days: int = 30) -> List[Film]:
        cutoff_date = datetime.now() - timedelta(days=days)
        films = self.get_all_watched_films()
        return [
            film for film in films
            if any(date >= cutoff_date for date in film.watch_dates)]