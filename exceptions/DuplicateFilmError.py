class DuplicateFilmError(Exception):
    def __init__(self, message="Film już istnieje w kolekcji."):
        self.message = message
        super().__init__(self.message)