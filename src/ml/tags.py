from typing import List

from .tags_search import KeywordService


def get(source: str) -> List[str]:
    """Получение ключевых слов (тэгов) из текста

    Args:
        source (str): исходный текст

    Returns:
        set[str]: теги
    """

    tags_service = KeywordService(source)
    result = tags_service.generate_tags()

    return list(result)
