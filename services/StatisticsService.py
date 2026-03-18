import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from statistics import mean
from typing import Optional, Dict, List

from models.Film import Film
from services.FilmService import FilmService

class StatisticsService:
    def __init__(self, film_service: FilmService) -> None:
        self.film_service = film_service

    def count_by_genre(self) -> Counter[str]:
        genres: List[str] = [film.genre for film in self.film_service.list_all_films()]
        return Counter(genres)

    def average_rating(self) -> Optional[float]:
        ratings: List[int] = [film.rating for film in self.film_service.list_all_films() if film.rating is not None]
        return round(mean(ratings), 2) if ratings else None

    def best_rated_film(self) -> List[Film]:
        films = [f for f in self.film_service.list_all_films() if
                 isinstance(f.rating, (int, float)) and 1 <= f.rating <= 10]
        if not films:
            return []
        max_rating = max(f.rating for f in films)
        return [f for f in films if f.rating == max_rating]

    def count_by_status(self) -> Counter[str]:
        statuses: List[str] = [film.status for film in self.film_service.list_all_films()]
        return Counter(statuses)

    def watched_per_year(self) -> Counter[int]:
        years: List[int] = []
        for film in self.film_service.list_all_films():
            if getattr(film, "watch_dates", None):
                years.extend([date.year for date in film.watch_dates if date])
        return Counter(years)

    def average_rating_by_genre(self) -> Dict[str, float]:
        genre_ratings: Dict[str, List[int]] = {}
        for film in self.film_service.list_all_films():
            if film.rating is not None:
                genre_ratings.setdefault(film.genre, []).append(film.rating)
        return {genre: round(mean(ratings), 2) for genre, ratings in genre_ratings.items()}

    def unrated_films_count(self) -> int:
        return len([f for f in self.film_service.list_all_films() if f.rating is None])

    def top_rated_films(self, top_n: int = 5) -> List[Film]:
        rated: List[Film] = [film for film in self.film_service.list_all_films() if film.rating is not None]
        return sorted(rated, key=lambda f: f.rating, reverse=True)[:top_n]

    def plot_genres(self) -> None:
        data = self.count_by_genre()
        genres = list(data.keys())
        counts = list(data.values())

        plt.bar(genres, counts, color='royalblue', edgecolor='black')
        plt.title("Liczba filmów wg gatunku")
        plt.xlabel("Gatunek")
        plt.ylabel("Liczba filmów")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_statuses(self) -> None:
        data = self.count_by_status()
        labels = list(data.keys())
        values = list(data.values())
        plt.pie(values, labels=labels, autopct='%1.1f%%', colors=['limegreen', 'tomato'])
        plt.title("Status: obejrzane/nieobejrzane")
        plt.tight_layout()
        plt.show()

    def plot_watched_per_year(self) -> None:
        data = self.watched_per_year()
        years = sorted(data.keys())
        counts = [data[year] for year in years]
        plt.plot(years, counts, marker='o', color='royalblue')
        plt.fill_between(years, counts, color='skyblue', alpha=0.3)
        plt.title("Liczba obejrzanych w latach")
        plt.xlabel("Rok")
        plt.ylabel("Liczba obejrzanych filmów")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

    def plot_average_rating_by_genre(self) -> None:
        avg_data = self.average_rating_by_genre()
        count_data = self.count_by_genre()
        if not avg_data:
            print("\nBrak ocen filmów według gatunku.")
            return

        genres = list(avg_data.keys())
        avg_ratings = [avg_data[g] for g in genres]
        counts = [count_data.get(g, 0) for g in genres]

        fig, ax1 = plt.subplots()
        ax1.bar(genres, avg_ratings, color='deepskyblue', label='Średnia ocena')
        ax1.set_ylabel("Średnia ocena", color='deepskyblue')
        ax1.set_ylim(0, max(avg_ratings + [10]) + 1)

        ax2 = ax1.twinx()
        ax2.plot(genres, counts, color='crimson', marker='o', label='Liczba filmów')
        ax2.set_ylabel("Liczba filmów", color='crimson')
        ax2.set_ylim(0, max(counts + [1]) + 1)

        plt.title("Średnia ocena i liczba filmów wg gatunku")
        plt.xticks(rotation=45)
        fig.tight_layout()
        plt.show()

    def plot_cumulative_watched(self) -> None:
        dates = []
        for film in self.film_service.list_all_films():
            if getattr(film, "watch_dates", None):
                dates.extend([d for d in film.watch_dates if d])
        dates.sort()
        counts = list(range(1, len(dates) + 1))
        plt.plot(dates, counts, marker='o', color='seagreen')
        plt.fill_between(dates, counts, color='lightgreen', alpha=0.3)
        plt.title("Łączna liczba obejrzanych filmów w czasie")
        plt.xlabel("Data")
        plt.ylabel("Liczba obejrzanych filmów")
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

    def plot_rating_distribution_by_genre(self) -> None:
        films = self.film_service.list_all_films()
        data = [(film.genre, film.rating) for film in films if film.rating is not None]

        df = pd.DataFrame(data, columns=['Gatunek', 'Ocena'])
        genres = df['Gatunek'].unique()
        ratings_by_genre = [df[df['Gatunek'] == genre]['Ocena'] for genre in genres]
        plt.boxplot(ratings_by_genre, labels=genres, patch_artist=True,
                    boxprops=dict(facecolor='lightskyblue', color='navy', alpha=0.5))
        plt.title("Rozkład ocen wg gatunku")
        plt.xlabel("Gatunek")
        plt.ylabel("Ocena")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()