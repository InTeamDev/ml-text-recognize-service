from typing import List

from .using_model import TagsService


def get(source: str) -> List[str]:
    """Получение ключевых слов (тэгов) из текста

    Args:
        source (str): исходный текст

    Returns:
        list[str]: теги
    """

    tags_service = TagsService(source)
    # get tags logic...
    result = []

    return result
