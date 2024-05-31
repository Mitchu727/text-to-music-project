from src.models.audio_ldm import AudioLDM
from src.models.model_interface import ModelInterface
from src.models.musicgen import Musicgen
from src.models.audio_ldm_2 import AudioLDM2
from src.output.output_saver import OutputSaver
from src.output.complex_output_saver import ComplexOutputSaver

class TextToMusicHub:
    models: list[ModelInterface] = [
        AudioLDM,
        Musicgen,
        AudioLDM2
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


if __name__ == "__main__":
    hub = TextToMusicHub()

    # output_path = get_project_root() / "outputs"
    length = 5
    text = "80s pop track with bassy drums and synth"
    model = hub.create_model("audioLDM2", "audioldm2-music")
    model.generate(prompt=text, length_in_seconds=length)


    #
    # # model = "musicgen-large"
    # model = "musicgen-melody-large"
    # output_file_name = output_path / f"{model}_out.wav"  # FIXME potrzebne będzie lepsze zarządzanie ścieżkami
    # musicgen = Musicgen(model, output_filename= output_file_name)
    # musicgen.generate(prompt=text, length_in_seconds=length)

    # model = "audioldm"
    # model = "audioldm-m-full"
    # model = "audioldm-s-full-v2"
    # model = "audioldm-l-full"
    # output_file_name = output_path / f"{model}_out.wav"
    # audio_ldm = AudioLDM(model, output_file_name)
    # audio_ldm.generate(prompt=text, length_in_seconds=length)