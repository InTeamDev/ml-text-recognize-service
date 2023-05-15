from typing import Set

from .using_model import TagsService


def get(source: str) -> Set[str]:
    """Получение ключевых слов (тэгов) из текста

    Args:
        source (str): исходный текст

    Returns:
        set[str]: теги
    """

    tags_service = TagsService(source)
    result = tags_service.generate_tags()
    
    return result
