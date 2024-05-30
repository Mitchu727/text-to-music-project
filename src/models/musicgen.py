from pathlib import Path

from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy

from src.models.model_interface import ModelInterface

class Musicgen(ModelInterface):
    available_models: list[str] = [
        "musicgen-small",
        "musicgen-medium",
        "musicgen-large",
        "musicgen-melody",
        "musicgen-melody-large"
    ]

    modifiable_parameters = {}

    def __init__(self, model_name: str, output_filename: Path = "musicgen_out.wav"):
        self.processor = AutoProcessor.from_pretrained(f"facebook/{model_name}")
        self.model = MusicgenForConditionalGeneration.from_pretrained(f"facebook/{model_name}")
        self.output_file_name = output_filename

    def generate(self, prompt: str, length_in_seconds: int, config={}):
        inputs = self.processor(
            text=[prompt],
            padding=True,
            return_tensors="pt",
        )

        length_in_tokens = int(length_in_seconds * 256 / 5)
        audio_values = self.model.generate(**inputs, max_new_tokens=length_in_tokens)

        sampling_rate = self.model.config.audio_encoder.sampling_rate
        scipy.io.wavfile.write(self.output_file_name, rate=sampling_rate, data=audio_values[0, 0].numpy())  # TODO jakiś ładny loader
