from abc import ABC, abstractmethod

class ModelInterface:
    @abstractmethod
    def generate(self, prompt: str, length_in_seconds: int):
        pass