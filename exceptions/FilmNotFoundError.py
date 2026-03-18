class FilmNotFoundError(LookupError):
    def __init__(self, message="Film nie został znaleziony."):
        super().__init__(message)
