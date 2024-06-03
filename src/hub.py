from src.models.audio_ldm import AudioLDM
from src.models.model_interface import ModelInterface
from src.models.music_ldm import MusicLDM
from src.models.musicgen import Musicgen
from src.models.audio_ldm_2 import AudioLDM2
from src.output.output_saver import OutputSaver
from src.output.complex_output_saver import ComplexOutputSaver


class TextToMusicHub:
    """
       Class representing a hub for managing different text-to-music models.
       """
    models: list[ModelInterface] = [
        AudioLDM,
        Musicgen,
        AudioLDM2,
        MusicLDM
    ]

    def __init__(self, output_saver: OutputSaver = ComplexOutputSaver()):
        self.output_saver = output_saver

    def get_available_models(self):
        return [model.id for model in self.models]

    def get_model(self, model_id):
        for model in self.models:
            if model.id == model_id:
                return model

    def create_model(self, model_id, model_variant):
        for model in self.models:
            if model.id == model_id:
                return model(model_variant, self.output_saver)
