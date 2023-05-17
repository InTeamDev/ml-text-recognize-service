from typing import Set

from .tags_search import KeywordService


def get(source: str) -> Set[str]:
    """Получение ключевых слов (тэгов) из текста

    Args:
        source (str): исходный текст

    Returns:
        set[str]: теги
    """

    tags_service = KeywordService(source)
    result = tags_service.generate_tags()

    return result
