class FieldException(Exception):
    """Класс ошибки поля данных."""
    def __init__(self, message: str):
        super(FieldException, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message
