from abc import ABC, abstractmethod


class TranslatorService(ABC):
    @abstractmethod
    async def translate(self, text: str) -> str: ...
