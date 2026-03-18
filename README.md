# 🎬 Watchlist - Movie Collection Manager

A robust, modular Command Line Interface (CLI) application built in Python. Designed to seamlessly manage, track, and visualize personal movie collections using a service-oriented architecture.

> **Note:** The interactive CLI menu is presented in Polish, while the underlying architecture, codebase, and documentation adhere strictly to international English standards.

---

## ✨ Key Features

* **Complete CRUD Lifecycle:** Add, edit, remove, and view detailed movie attributes (Title, Director, Year, Genre, Status, Rating, Description, Comments).
* **Advanced Search & Filtering:** * Search by exact ID or partial title matches (e.g., searching "Jurassic" returns all related titles).
  * Filter collections by watch status or genre.
  * Sort dynamically by release year or user rating.
* **Watch History Tracking:** The system automatically logs exact timestamps when a movie is marked as "watched" and maintains a comprehensive viewing history.
* **Data Visualization:** Generates interactive charts using `matplotlib` and `pandas` to display genre distribution, average ratings, and watch history trends over time.
* **Data Portability:** Export your entire structured collection and watch history to a `.txt` file for external use.
* **Data Persistence:** Automatic and safe state-saving using JSON format (`my_films.json`).

## 🛠️ Technical Stack & Architecture

This project was built with a strong emphasis on clean code and scalable design patterns:
* **Language:** Python 3.x
* **Core Libraries:** `pandas`, `matplotlib`, `json`, `datetime`
* **Architecture:** Object-Oriented Programming (OOP) with a strict separation of concerns (Controllers, Services, Models).
* **Robust Error Handling:** Features strict input validation and over 10 custom exceptions (e.g., `DuplicateFilmError`, `InvalidRatingError`) to ensure data integrity.

## 📂 Project Structure

```text
watchlist-python/
├── exceptions/         # Custom business-logic exceptions
├── interface/          # CLI menu routing and user interactions
├── models/             # Domain entities (Film object)
├── services/           # Core business logic (Filtering, Stats, Export, History)
├── validator/          # Centralized data sanitation
├── data/               # Local JSON database storage
└── main.py             # Application entry point
