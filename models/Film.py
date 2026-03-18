from datetime import datetime
from typing import Optional, List, Dict, Any

from validator.Validator import Validator


class Film:
    _id_counter: int = 1

    def __init__(
        self,
        title: str,
        director: str,
        year: int,
        genre: str,
        status: str = "unwatched",
        rating: Optional[int] = None,
        description: str = "",
        film_id: Optional[int] = None,
        comments: Optional[List[str]] = None,
        watch_dates: Optional[List[Any]] = None
    ) -> None:
        self.id: int = film_id if film_id is not None else Film._id_counter
        if film_id is None:
            Film._id_counter += 1

        self.title: str = title.strip()
        self.director: str = director.strip()
        self.year: int = year
        self.genre: str = genre.strip()
        self.status: str = status
        self.rating: Optional[int] = rating
        self.description: str = description.strip()
        self.comments: List[str] = comments or []
        self.watch_dates: List[datetime] = [
            datetime.fromisoformat(d) if isinstance(d, str) else d
            for d in (watch_dates or [])]

        self.validate()

    def validate(self) -> None:
        if not Validator.validate_title(self.title):
            raise ValueError("Tytuł nie może być pusty.")
        if not Validator.validate_director(self.director):
            raise ValueError("Reżyser nie może być pusty.")
        valid_year: Optional[int] = Validator.validate_year(self.year)
        if valid_year is None:
            raise ValueError(f"Nieprawidłowy rok produkcji -> {self.year}")
        try:
            self.rating = Validator.validate_rating(self.rating)
        except Exception as e:
            raise ValueError(str(e))
        if not Validator.validate_genre(self.genre):
            raise ValueError("Gatunek nie może być pusty.")
        self.status = Validator.validate_status(self.status)

    def add_comment(self, comment: str) -> None:
        comment = comment.strip()
        if comment:
            self.comments.append(comment)
        else:
            raise ValueError("\nKomentarz nie może być pusty.")

    def add_watch_date(self, date: Optional[datetime] = None) -> None:
        if date is None:
            date = datetime.now()
        if isinstance(date, datetime):
            self.watch_dates.append(date)
        else:
            raise ValueError("\nData musi być typu datetime.")

    def __str__(self) -> str:
        rating_str: str = str(self.rating) if self.rating is not None else "Brak oceny"
        return f"{self.title} ({self.year}), {self.genre}, Status -> {self.status}, Ocena -> {rating_str}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "director": self.director,
            "year": self.year,
            "genre": self.genre,
            "status": self.status,
            "rating": self.rating,
            "description": self.description,
            "comments": self.comments,
            "watch_dates": [d.isoformat() for d in self.watch_dates],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Film":
        return Film (
            title=data["title"],
            director=data["director"],
            year=data["year"],
            genre=data["genre"],
            status=data.get("status", "unwatched"),
            rating=data.get("rating"),
            description=data.get("description", ""),
            film_id=data["id"],
            comments=data.get("comments", []),
            watch_dates=data.get("watch_dates", [])
        )