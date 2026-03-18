from typing import Dict, Tuple, Optional, Callable, List, Any

from exceptions.DuplicateFilmError import DuplicateFilmError
from exceptions.FilmNotFoundError import FilmNotFoundError
from exceptions.InvalidInputError import InvalidInputError
from models.Film import Film
from services.ExportService import ExportService
from services.FilmFilterService import FilmFilterService
from services.FilmService import FilmService
from services.StatisticsService import StatisticsService
from services.WatchHistoryService import WatchHistoryService
from validator.Validator import Validator


def run_menu(title: str, options: Dict[str, Tuple[str, Optional[Callable[[], None]]]],
             handle_exceptions: bool = False) -> None:
    while True:
        print(f"\n=== {title.upper()} ===")
        for key, (desc, _) in options.items():
            print(f"{key}. {desc}")
        choice = input(f"Wybierz opcję (1-{len(options)}) -> ").strip()
        action = options.get(choice)
        if action:
            _, func = action
            if func:
                if handle_exceptions:
                    try:
                        func()
                    except Exception as e:
                        print(f"\nBłąd podczas wykonywania opcji '{choice}': {e}")
                else:
                    func()
            else:
                break
        else:
            print(f"\nNieprawidłowy wybór. Proszę wybrać numer od 1 do {len(options)}.")


def print_films_list(films: list['Film']) -> None:
    if not films:
        print("\nBrak filmów do wyświetlenia.")
        return
    for film in films:
        rating = film.rating if film.rating is not None else "Brak oceny"
        print(f"ID -> {film.id}, Tytuł -> {film.title}, Rok -> {film.year}, Ocena -> {rating}, Status -> {film.status}")


class CLI:
    def __init__(self):
        self.film_service = FilmService()
        self.history_service = WatchHistoryService(self.film_service)
        self.export_service = ExportService(self.film_service)
        self.statistics_service = StatisticsService(self.film_service)
        self.filter_service = FilmFilterService(self.film_service)


    def start(self):
        self.main_menu()

    def main_menu(self) -> None:
        options: Dict[str, Tuple[str, Optional[Callable[[], None]]]] = {
            "1": ("Filmy", self.menu_filmy),
            "2": ("Historia oglądania", self.menu_historia),
            "3": ("Statystyki", self.menu_statystyki),
            "4": ("Eksport danych", self.menu_eksport),
            "5": ("Wyjście", None)
        }
        run_menu("Główny menu", options)

    def menu_filmy(self) -> None:
        options: Dict[str, Tuple[str, Optional[Callable[[], None]]]] = {
            "1": ("Dodaj film", self.add_film),
            "2": ("Edytuj film", self.edit_film),
            "3": ("Usuń film", self.remove_film),
            "4": ("Oceń film", self.rate_film),
            "5": ("Dodaj komentarz", self.add_comment),
            "6": ("Wyszukaj film", self.menu_search_film),
            "7": ("Filtruj i sortuj filmy", self.filter_sort_films),
            "8": ("Pokaż wszystkie filmy", self.show_all_films),
            "9": ("Powrót", None)
        }
        run_menu("Filmy", options)

    def add_film(self) -> None:
        print("\nDodawanie nowego filmu -> ")

        title = input("Tytuł -> ").strip()
        if not Validator.validate_title(title):
            return

        director = input("Reżyser -> ").strip()
        if not Validator.validate_director(director):
            return

        year_input = input("Rok produkcji -> ").strip()
        year = Validator.validate_year(year_input)
        if year is None:
            return

        genre = input("Gatunek -> ").strip()
        if not Validator.validate_genre(genre):
            return

        status_input = input("Status (watched/unwatched) -> ").strip()
        status = Validator.validate_status(status_input)
        rating_input = input("Ocena (1-10, pozostaw puste jeśli brak) -> ").strip()
        rating = Validator.validate_rating(rating_input)
        description = input("Krótki opis -> ").strip()

        try:
            self.film_service.add_film(title, director, year, genre, status, rating, description)
            print("\nFilm został dodany.")
        except DuplicateFilmError as e:
            print(f"\nBłąd: {e}")
        except ValueError as e:
            print(f"\nBłąd walidacji -> {e}")
        except Exception as e:
            print(f"\nNiespodziewany błąd -> {e}")


    def edit_film(self) -> None:
        print("\nWybierz film do edycji")
        film = self.menu_search_film()
        if not film:
            print("Nie wybrano filmu do edycji.")
            return

        print(f"Edytujesz film -> {film.title}, ({film.id}) ")
        changes: Dict[str, Any] = {}

        def prompt_and_validate(prompt: str, validate_func: Callable[[str], Any]) -> Optional[Any]:
            while True:
                val = input(prompt).strip()
                if val == "":
                    return None
                try:
                    result = validate_func(val)
                except Exception as ex:
                    print(f"Błąd walidacji: {ex}")
                    continue
                if result is not False and result is not None:
                    return val

        def edit_title():
            val = prompt_and_validate("Nowy tytuł -> ", Validator.validate_title)
            if val is not None:
                changes["title"] = val

        def edit_director():
            val = prompt_and_validate("Nowy reżyser -> ", Validator.validate_director)
            if val is not None:
                changes["director"] = val

        def edit_year():
            val = prompt_and_validate("Nowy rok produkcji -> ", Validator.validate_year)
            if val is not None:
                changes["year"] = int(val)

        def edit_genre():
            val = prompt_and_validate("Nowy gatunek -> ", Validator.validate_genre)
            if val is not None:
                changes["genre"] = val

        def edit_status():
            val = prompt_and_validate("Nowy status (watched/unwatched) -> ", Validator.validate_status)
            if val is not None:
                changes["status"] = val.lower()

        def edit_rating():
            val = prompt_and_validate("Nowa ocena (1-10) -> ", Validator.validate_rating)
            if val is not None:
                changes["rating"] = int(val)

        def edit_description():
            val = input("Nowy opis -> ").strip()
            if val:
                changes["description"] = val

        options = {
            "1": ("Tytuł", edit_title),
            "2": ("Reżyser", edit_director),
            "3": ("Rok produkcji", edit_year),
            "4": ("Gatunek", edit_genre),
            "5": ("Status", edit_status),
            "6": ("Ocena", edit_rating),
            "7": ("Opis", edit_description),
            "8": ("Zakończ edycję", None),
        }

        run_menu("Edycja filmu", options)

        if changes:
            try:
                self.film_service.edit_film(film.id, **changes)
                print("Film został zaktualizowany.")
            except InvalidInputError as e:
                print(f"\nBłąd podczas aktualizacji filmu -> {e}")
        else:
            print("\nNie dokonano żadnych zmian.")

    def remove_film(self) -> None:
        print("\nWybierz film do usunięcia")
        film: Optional[Film] = self.menu_search_film()
        if not film:
            print("\nNie wybrano filmu do usunięcia.")
            return

        while True:
            confirm = input(f"Czy na pewno chcesz usunąć film '{film.title}'? (t/n) -> ").strip().lower()
            if confirm == 't':
                try:
                    self.film_service.remove_film(film.id)
                    print("\nFilm usunięty.")
                except Exception as e:
                    print(f"\nBłąd podczas usuwania filmu -> {e}")
                break
            elif confirm == 'n':
                print("\nUsuwanie anulowane.")
                break
            else:
                print("\nNieprawidłowa odpowiedź. Proszę wpisać 't' lub 'n'.")

    def rate_film(self) -> None:
        print("\nWybierz film do oceny")
        film: Optional[Film] = self.menu_search_film()
        if not film:
            print("\nNie wybrano filmu do oceny.")
            return

        rating_input = input("\nWprowadź ocenę (1-10) -> ").strip()
        rating = Validator.validate_rating(rating_input)

        if rating is not None:
            try:
                self.film_service.edit_film(film.id, rating=rating)
                print(f"\nFilm '{film.title}' oceniony na {rating}.")
            except Exception as e:
                print(f"\nBłąd podczas aktualizacji oceny -> {e}")
        else:
            print("\nNieprawidłowa ocena. Wprowadź liczbę od 1 do 10.")

    def add_comment(self) -> None:
        print("\nWybierz film do dodania komentarza")
        film: Optional['Film'] = self.menu_search_film()
        if not film:
            print("\nNie wybrano filmu.")
            return

        comment: str = input("Wpisz komentarz do filmu -> ").strip()
        if not comment:
            print("\nKomentarz nie może być pusty.")
            return

        try:
            self.film_service.add_comment_to_film(film.id, comment)
            print("\nKomentarz został dodany.")
        except ValueError as e:
            print(f"\nBłąd -> {e}")

    def menu_search_film(self) -> Optional[Film]:
        selected_film = None

        def search_by_id_action():
            nonlocal selected_film
            selected_film = self.search_by_id_loop()
            if selected_film:
                self.print_film_details(selected_film)
                raise StopIteration

        def search_by_title_action():
            nonlocal selected_film
            selected_film = self.search_by_title_interactive()
            if selected_film:
                self.print_film_details(selected_film)
                raise StopIteration

        options = {
            "1": ("Wyszukaj po ID", search_by_id_action),
            "2": ("Wyszukaj po tytule", search_by_title_action),
            "3": ("Powrót", None),
        }

        try:
            run_menu("Wybierz sposób wyszukiwania filmu", options)
        except StopIteration:
            pass

        return selected_film

    def print_film_details(self, film: Film) -> None:
        print(f"\n=== Szczegóły filmu ===")
        print(f"ID: {film.id}")
        print(f"Tytuł: {film.title}")
        print(f"Reżyser: {film.director}")
        print(f"Rok: {film.year}")
        print(f"Gatunek: {film.genre}")
        print(f"Status: {film.status}")
        print(f"Ocena: {film.rating if film.rating is not None else 'Brak'}")
        print(f"Opis: {film.description}")
        print(f"Komentarze: {', '.join(film.comments) if film.comments else 'Brak komentarzy'}")
        print("=" * 30)

    def search_by_id_loop(self) -> Optional[Film]:
        while True:
            id_input = input("\nWpisz ID filmu (lub 'n' aby zakończyć) -> ").strip()
            if id_input.lower() == 'n':
                return None
            try:
                film_id = Validator.validate_id(id_input)
            except Exception as e:
                print(f"Błąd: {e}")
                continue
            try:
                film = self.film_service.get_film_by_id(film_id)
                return film
            except FilmNotFoundError:
                print(f"\nFilm o ID {film_id} nie został znaleziony. Spróbuj ponownie.")

    def search_by_title_interactive(self) -> Optional[Film]:
        while True:
            term = input("Podaj tytuł do wyszukania -> ").strip()
            try:
                Validator.validate_title(term)
            except Exception as e:
                print(f"\nBłąd: {e}")
                continue

            found_films = self.film_service.find_films_by_title(term)
            if not found_films:
                print("\nNie znaleziono filmów.")
                return None

            if len(found_films) == 1:
                return found_films[0]

            print("\nZnaleziono wiele filmów -> ")
            for film in found_films:
                print(f"{film.id}: {film.title} ({film.year})")

            while True:
                selected_id = input("\nPodaj ID filmu do wyboru (lub 'n' aby anulować) -> ").strip()
                if selected_id.lower() == 'n':
                    return None
                try:
                    film_id = Validator.validate_id(selected_id)
                except Exception as e:
                    print(f"\nBłąd: {e}")
                    continue
                try:
                    return self.film_service.get_film_by_id(film_id)
                except FilmNotFoundError:
                    print(f"\nFilm o ID {selected_id} nie został znaleziony. Spróbuj ponownie.")

    def filter_sort_films(self) -> None:
        def filter_by_status():
            status = input("\nWpisz status (watched/unwatched) -> ").strip().lower()
            if status in ("watched", "unwatched"):
                filtered = self.filter_service.filter_by_status(status)
                print_films_list(filtered)
            else:
                print("\nNieprawidłowy status.")

        def filter_by_genre():
            genre = input("\nWpisz gatunek -> ").strip()
            if genre:
                filtered = self.filter_service.filter_by_genre(genre)
                print_films_list(filtered)
            else:
                print("\nGatunek nie może być pusty.")

        def sort_by_year():
            order = input("Sortuj wg roku (asc/desc) -> ").strip().lower()
            if order in ("asc", "desc"):
                reverse = order == "desc"
                sorted_list = self.filter_service.sort_by_year(reverse=reverse)
                print_films_list(sorted_list)
            else:
                print("Nieprawidłowa opcja sortowania.")

        def sort_by_rating():
            order = input("Sortuj wg oceny (asc/desc) -> ").strip().lower()
            if order in ("asc", "desc"):
                reverse = order == "desc"
                sorted_list = self.filter_service.sort_by_rating(reverse=reverse)
                print_films_list(sorted_list)
            else:
                print("Nieprawidłowa opcja sortowania.")

        options = {
            "1": ("Filtruj po statusie (watched/unwatched)", filter_by_status),
            "2": ("Filtruj po gatunku", filter_by_genre),
            "3": ("Sortuj po roku produkcji", sort_by_year),
            "4": ("Sortuj po ocenie", sort_by_rating),
            "5": ("Powrót", None),
        }

        run_menu("Opcje filtrowania i sortowania", options)

    def show_all_films(self) -> None:
        films: List['Film'] = self.film_service.list_all_films()
        if not films:
            print("\nBrak filmów do wyświetlenia.")
            return

        print("\n=== Wszystkie filmy ===")
        for film in films:
            rating = film.rating if film.rating is not None else "Brak"
            comments = ', '.join(film.comments) if film.comments else "Brak komentarzy"

            print(
                f"ID -> {film.id} | Tytuł -> {film.title} | Reżyser -> {film.director} | Rok -> {film.year} | "
                f"Gatunek -> {film.genre} | Status -> {film.status} | Ocena -> {rating}"
            )
            print(f"Opis -> {film.description}")
            print(f"Komentarze -> {comments}")
            print("=" * 25)

    def menu_historia(self) -> None:
        options: Dict[str, Tuple[str, Optional[Callable[[], None]]]] = {
            "1": ("Pokaż historię", self.show_watch_history),
            "2": ("Dodaj do historii obejrzenia", self.add_watch_history),
            "3": ("Usuń wpis z historii", self.remove_watch_history),
            "4": ("Pokaż top 5 najczęściej oglądanych filmów", self.show_top_5_watched),
            "5": ("Pokaż filmy oglądane w ciągu ostatnich 30 dni", self.show_recently_watched),
            "6": ("Powrót", None)
        }
        run_menu("Historia oglądania", options)

    def show_watch_history(self) -> None:
        films = self.history_service.get_all_watched_films()
        if not films:
            print("\nBrak historii oglądania.")
            return
        print("Historia oglądania -> ")
        for film in films:
            print(f"- {film.title} (oglądany {len(film.watch_dates)} razy) -> ")
            for date in film.watch_dates:
                print(f"   Data oglądania -> {date}")

    def add_watch_history(self) -> None:
        film_id_str = input("Podaj ID filmu -> ").strip()
        film_id = Validator.validate_id(film_id_str)
        if film_id is None:
            return
        try:
            self.history_service.add_watch_date(film_id)
            print("\nDodano datę oglądania.")
        except FilmNotFoundError:
            print("\nFilm o podanym ID nie istnieje.")
        except Exception as e:
            print(f"\nWystąpił nieoczekiwany błąd -> {e}")

    def remove_watch_history(self) -> None:
        films = self.film_service.list_all_films()
        print_films_list(films)

        film_id_str = input("\nPodaj ID filmu do usunięcia historii -> ").strip()
        film_id = Validator.validate_id(film_id_str)
        if film_id is None:
            return
        try:
            self.history_service.clear_watch_history(film_id)
            print("\nHistoria oglądania usunięta.")
        except FilmNotFoundError:
            print("\nFilm o podanym ID nie istnieje.")
        except Exception as e:
            print(f"\nWystąpił nieoczekiwany błąd -> {e}")

    def show_top_5_watched(self) -> None:
        top_films = self.history_service.get_most_watched_films()
        if not top_films:
            print("\nBrak danych o najczęściej oglądanych filmach.")
            return
        print("\nTop 5 najczęściej oglądanych filmów -> ")
        for film, count in top_films:
            print(f"- {film.title}: {count} razy")

    def show_recently_watched(self) -> None:
        recent_films = self.history_service.get_recently_watched_films()
        if not recent_films:
            print("Brak filmów oglądanych w ciągu ostatnich 30 dni.")
            return
        print("Filmy oglądane w ciągu ostatnich 30 dni -> ")
        for film in recent_films:
            print(f"- {film.title}")

    def menu_statystyki(self):
        menu_options = {
            "1": ("Statystyki tekstowe", self.menu_statystyki_tekstowe),
            "2": ("Statystyki graficzne (wykresy)", self.menu_statystyki_graficzne),
            "3": ("Powrót", None)
        }
        run_menu("Statystyki - wybierz sekcję", menu_options, handle_exceptions=True)

    def menu_statystyki_tekstowe(self):
        menu_options = {
            "1": ("Liczba filmów wg gatunków", self._stat_count_by_genre),
            "2": ("Średnia ocena filmów", self._stat_average_rating),
            "3": ("Najlepiej oceniany film", self._stat_best_rated_film),
            "4": ("Liczba obejrzanych i nieobejrzanych filmów", self._stat_count_by_status),
            "5": ("Liczba obejrzanych filmów lata", self._stat_watched_per_year),
            "6": ("Średnia ocena filmów wg gatunku", self._stat_average_rating_by_genre),
            "7": ("Liczba filmów bez oceny", self._stat_unrated_films_count),
            "8": ("Top 5 najwyżej ocenianych filmów", self._stat_top_rated_films),
            "9": ("Powrót", None)
        }
        run_menu("Statystyki tekstowe", menu_options, handle_exceptions=True)

    def menu_statystyki_graficzne(self):
        menu_options = {
            "1": ("Liczba filmów wg gatunku", self.statistics_service.plot_genres),
            "2": ("Status obejrzane/nieobejrzane", self.statistics_service.plot_statuses),
            "3": ("Liczba obejrzanych filmów w latach", self.statistics_service.plot_watched_per_year),
            "4": ("Średnia ocena i liczba filmów wg gatunku", self.statistics_service.plot_average_rating_by_genre),
            "5": ("Łączna liczba obejrzanych filmów w czasie", self.statistics_service.plot_cumulative_watched),
            "6": ("Rozkład ocen wg gatunku", self.statistics_service.plot_rating_distribution_by_genre),
            "7": ("Powrót", None)
        }
        run_menu("Statystyki graficzne", menu_options, handle_exceptions=True)

    def _stat_count_by_genre(self) -> None:
        stats = self.statistics_service.count_by_genre()
        if not stats:
            print("\nBrak danych o gatunkach filmów.")
            return
        for genre, count in stats.items():
            print(f"{genre} -> {count}")

    def _stat_average_rating(self) -> None:
        avg = self.statistics_service.average_rating()
        if avg is not None:
            print(f"\nŚrednia ocena filmów -> {avg:.2f}")
        else:
            print("\nBrak ocenionych filmów.")

    def _stat_best_rated_film(self) -> None:
        films = self.statistics_service.best_rated_film()
        if films:
            print("\nNajlepiej oceniane filmy:")
            for film in films:
                print(f"- {film.title} (ocena: {film.rating})")
        else:
            print("\nBrak ocenionych filmów.")

    def _stat_count_by_status(self) -> None:
        status_stats = self.statistics_service.count_by_status()
        if not status_stats:
            print("\nBrak danych o statusach filmów.")
            return
        for status, count in status_stats.items():
            print(f"{status.capitalize()}: {count}")

    def _stat_watched_per_year(self) -> None:
        watched_years = self.statistics_service.watched_per_year()
        if watched_years:
            for year, count in sorted(watched_years.items()):
                if Validator.validate_year(year):
                    print(f"{year}: {count}")
        else:
            print("\nBrak danych o obejrzanych filmach.")

    def _stat_average_rating_by_genre(self) -> None:
        data = self.statistics_service.average_rating_by_genre()
        if not data:
            print("\nBrak ocenionych filmów według gatunku.")
            return
        for genre, avg in data.items():
            if avg is not None:
                print(f"{genre}: {avg:.2f}")
            else:
                print(f"{genre}: brak ocenionych filmów")

    def _stat_unrated_films_count(self) -> None:
        unrated = self.statistics_service.unrated_films_count()
        if isinstance(unrated, int) and unrated >= 0:
            print(f"\nLiczba filmów bez oceny -> {unrated}")
        else:
            print("\nBrak danych o filmach bez oceny.")

    def _stat_top_rated_films(self) -> None:
        top_films = self.statistics_service.top_rated_films()
        if top_films:
            for film in top_films:
                rating_display = film.rating if film.rating is not None else "Brak oceny"
                print(f"{film.title} ({film.year}) - Ocena -> {rating_display}")
        else:
            print("\nBrak ocenionych filmów.")

    def menu_eksport(self) -> None:
        option = {
            "1" : ("Eksportuj do pliku tekstowego", self.export_to_txt),
            "2": ("Powrót", None)
        }
        run_menu("Eksport danych", option)

    def export_to_txt(self) -> None:
        filename = input("\nPodaj nazwę pliku do zapisu (np. moja_kolekcja) -> ").strip()
        if not filename:
            filename = "moja_kolekcja.txt"
        elif not filename.lower().endswith(".txt"):
            filename += ".txt"

        try:
            path: str = self.export_service.export_all_to_txt(filename)
            print(f"\nDane zostały wyeksportowane do pliku -> {path}")
        except Exception as e:
            print(f"\nBłąd podczas eksportu -> {e}")