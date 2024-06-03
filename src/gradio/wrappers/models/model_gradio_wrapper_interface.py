from abc import ABC, abstractmethod

from gradio.components.base import Component


class ModelGradioWrapperInterface(ABC):
    id: str

    @staticmethod
    @abstractmethod
    def create_parameters_fields_not_visible() -> list[Component]:
        pass

    @staticmethod
    @abstractmethod
    def create_parameters_fields_visible() -> list[Component]:
        pass

    @staticmethod
    @abstractmethod
    def display_generation_parameters(wav_path) -> list[Component]:
        pass

    @staticmethod
    @abstractmethod
    def create_config_from_args(args) -> dict:
        pass
