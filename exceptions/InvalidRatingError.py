class InvalidRatingError(ValueError):
    def __init__(self, message="Ocena musi być w zakresie 1-10."):
        self.message = message
        super().__init__(self.message)