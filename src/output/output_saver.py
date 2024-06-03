from abc import ABC, abstractmethod


class OutputSaver(ABC):
    """
       Abstract base class for saving generated audio outputs.
       """
    @abstractmethod
    def save_generation(self, audio, sampling_rate: int, prompt: str, length_in_seconds: int, model_id: str, model_variant: str, config: dict) -> None:
        pass
