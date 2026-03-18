import os
from datetime import datetime

from services.FilmService import FilmService


class ExportService:
    def __init__(self, film_service: FilmService) -> None:
        self.film_service = film_service

    def export_all_to_txt(self, filename: str = "moja_kolekcja.txt") -> str:
        os.makedirs("data", exist_ok=True)

        full_path = os.path.join("data", filename)

        films = self.film_service.list_all_films()
        if not films:
            raise ValueError("Brak filmów do eksportu.")

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(f"EKSPORT KOLEKCJI FILMÓW — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")

            for film in films:
                f.write(f"ID -> {film.id}\n")
                f.write(f"Tytuł -> {film.title}\n")
                f.write(f"Reżyser -> {film.director}\n")
                f.write(f"Rok -> {film.year}\n")
                f.write(f"Gatunek -> {film.genre}\n")
                f.write(f"Status -> {film.status}\n")
                f.write(f"Ocena -> {film.rating if film.rating is not None else 'Brak'}\n")
                f.write(f"Opis -> {film.description}\n")

                f.write("Komentarze -> \n")
                for comment in film.comments:
                    f.write(f"  - {comment}\n")

                f.write("Historia oglądania -> \n")
                for date in film.watch_dates:
                    f.write(f"  - {date.strftime('%Y-%m-%d %H:%M:%S')}\n")

                f.write("-" * 60 + "\n\n")

        return full_path