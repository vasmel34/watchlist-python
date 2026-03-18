class InvalidInputError(ValueError):
    def __init__(self, message="Nieprawidłowe dane wejściowe."):
        self.message = message
        super().__init__(self.message)