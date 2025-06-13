from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def ask(self, question : str) -> str:
        pass