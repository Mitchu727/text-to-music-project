import librosa
import numpy as np
from transformers import AutoProcessor
from transformers.models.musicgen.modeling_musicgen import MusicgenForConditionalGeneration
import scipy.io.wavfile

class MusicGen:
    def __init__(self, model_name: str, out: str = "musicgen_out.wav"):
        self.processor = AutoProcessor.from_pretrained(f"facebook/{model_name}")
        self.model = MusicgenForConditionalGeneration.from_pretrained(f"facebook/{model_name}")
        self.output_file_name = out

    def generate(self, prompt: str, length_in_seconds: int, melody: np.ndarray = None, sr: int = None):
        inputs = self.processor(
            text=[prompt],
            padding=True,
            return_tensors="pt",
        )

        length_in_tokens = int(length_in_seconds * 256 / 5)

        if melody is not None and sr is not None:
            melody_inputs = self.processor(
                text=[prompt],
                audio=melody,
                sampling_rate=sr,
                padding=True,
                return_tensors="pt",
            )
            inputs.update(melody_inputs)

        audio_values = self.model.generate(**inputs, max_new_tokens=length_in_tokens)

        sampling_rate = self.model.config.audio_encoder.sampling_rate
        scipy.io.wavfile.write(self.output_file_name, rate=sampling_rate, data=audio_values[0, 0].numpy())

        return self.output_file_name
