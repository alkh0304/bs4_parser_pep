class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""


class NullResponseException(Exception):
    """Вызывается, когда от url адреса не поступил ответ."""
