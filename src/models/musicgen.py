from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy

from src.models.model_interface import ModelInterface

class MusicGen(ModelInterface):
    def __init__(self, model_name: str, out: str = "musicgen_out.wav"):
        self.processor = AutoProcessor.from_pretrained(f"facebook/{model_name}")
        self.model = MusicgenForConditionalGeneration.from_pretrained(f"facebook/{model_name}")
        self.output_file_name = out

    def generate(self, prompt: str, length_in_seconds: int):
        inputs = self.processor(
            text=[prompt],
            padding=True,
            return_tensors="pt",
        )

        length_in_tokens = int(length_in_seconds * 256 / 5)
        audio_values = self.model.generate(**inputs, max_new_tokens=length_in_tokens)

        sampling_rate = self.model.config.audio_encoder.sampling_rate
        scipy.io.wavfile.write(self.output_file_name, rate=sampling_rate, data=audio_values[0, 0].numpy())  # TODO jakiś ładny loader