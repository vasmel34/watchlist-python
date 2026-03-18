from typing import List, Optional

from models.Film import Film
from services.FilmService import FilmService


class FilmFilterService:
    def __init__(self, film_service: FilmService) -> None:
        self.film_service = film_service

    def filter_by_status(self, status: str, films: Optional[List[Film]] = None) -> List[Film]:
        films = films or self.film_service.list_all_films()
        return [f for f in films if f.status.lower() == status.lower()]

    def filter_by_genre(self, genre: str, films: Optional[List[Film]] = None) -> List[Film]:
        films = films or self.film_service.list_all_films()
        genre_lower = genre.lower()
        return [f for f in films if f.genre.lower() == genre_lower]

    def sort_by_year(self, films: Optional[List[Film]] = None, reverse: bool = False) -> List[Film]:
        films = films or self.film_service.list_all_films()
        return sorted(films, key=lambda f: f.year, reverse=reverse)

    def sort_by_rating(self, films: Optional[List[Film]] = None, reverse: bool = False) -> List[Film]:
        films = films or self.film_service.list_all_films()
        return sorted(films, key=lambda f: f.rating if f.rating is not None else 0, reverse=reverse)