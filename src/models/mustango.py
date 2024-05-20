import scipy

from src.models.model_interface import ModelInterface
from mustango.mustango import Mustango

class MustangoInference(ModelInterface):
    available_models: list[str] = [
        "mustango"
    ]

    def __init__(self, model_name: str, out: str = "mustango_out.wav"):
        self.model = Mustango(f"declare-lab/{model_name}")
        self.output_file_name = out

    def generate(self, prompt: str, length_in_seconds: int):
        audio = self.model.generate(prompt)
        #sampling_rate = self.model.config.audio_encoder.sampling_rate
        scipy.io.wavfile.write(self.output_file_name, rate=16000, data=audio) 