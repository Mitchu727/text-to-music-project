from abc import ABC, abstractmethod


class OutputSaver(ABC):

    @abstractmethod
    def save_generation(self, audio, sampling_rate: int, prompt: str, length_in_seconds: int, model_name: str, model_variant: str, config: dict) -> None:
        pass
