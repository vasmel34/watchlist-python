from datetime import datetime
from typing import Optional

from exceptions.InvalidRatingError import InvalidRatingError
from exceptions.InvalidInputError import InvalidInputError

class Validator:
    @staticmethod
    def validate_title(title: str) -> bool:
        title = title.strip()
        if not title:
            raise InvalidInputError("Tytuł nie może być pusty.")
        if len(title) > 120:
            raise InvalidInputError("Tytuł nie może być dłuższy 120 znaków.")
        return True

    @staticmethod
    def validate_director(director: str) -> bool:
        director = director.strip()
        if not director:
            raise InvalidInputError("Reżyser nie może być pusty.")
        if len(director) > 100:
            raise InvalidInputError("Reżyser nie może być dłuższy 100 znaków.")
        return True

    @staticmethod
    def validate_year(value: object) -> Optional[int]:
        current_year = datetime.now().year
        if isinstance(value, int):
            year = value
        elif isinstance(value, str) and value.strip().isdigit():
            year = int(value.strip())
        else:
            raise InvalidInputError("Nieprawidłowy format roku.")
        if 1888 <= year <= current_year:
            return year
        raise InvalidInputError(f"Rok musi być w zakresie od 1888 do {current_year}.")

    @staticmethod
    def validate_genre(genre: str) -> bool:
        genre = genre.strip()
        if not genre:
            raise InvalidInputError("Gatunek nie może być pusty.")
        if len(genre) > 80:
            raise InvalidInputError("Gatunek nie może być dłuższy 80 znaków.")
        return True

    @staticmethod
    def validate_status(status: str) -> str:
        status = status.strip().lower()
        if status not in ("watched", "unwatched"):
            print("ustawiono 'unwatched'.")
            return "unwatched"
        return status

    @staticmethod
    def validate_rating(value: object) -> Optional[int]:
        if value is None or value == "":
            return None
        if isinstance(value, int):
            if 1 <= value <= 10:
                return value
            raise InvalidRatingError("Ocena w zakresie 1-10 lub brak.")
        if isinstance(value, str) and value.strip().isdigit():
            rating = int(value.strip())
            if 1 <= rating <= 10:
                return rating
        raise InvalidRatingError("Nieprawidłowa ocena. Dopuszczalne -> 1–10 lub brak.")

    @staticmethod
    def validate_id(id_val: object) -> int:
        if isinstance(id_val, int):
            film_id = id_val
        elif isinstance(id_val, str) and id_val.strip().isdigit():
            film_id = int(id_val.strip())
        else:
            raise InvalidInputError("ID musi być liczbą całkowitą.")
        if film_id <= 0:
            raise InvalidInputError("ID musi być większe od zera.")
        return film_id