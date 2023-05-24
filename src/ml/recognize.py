from typing import Union

import numpy as np
import whisper

model = whisper.load_model("base")


def get(audio: Union[str, np.ndarray]) -> str:
    """Получения текста из аудио

    Args:
        source (np.ndarray): массив байтов аудиофайла

    Returns:
        str: полученный текст
    """
    result = model.transcribe(audio, fp16=False)
    return result
