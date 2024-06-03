from abc import ABC, abstractmethod

from src.output.output_saver import OutputSaver


class ModelInterface(ABC):
    id: str
    available_models: list[str]

    @abstractmethod
    def __init__(self, model_name: str, output_saver: OutputSaver):
        pass

    @abstractmethod
    def generate(self, prompt: str, length_in_seconds: int, config: dict):
        pass
