from pathlib import Path

import scipy
import torch
from diffusers import AudioLDMPipeline

from src.models.model_interface import ModelInterface


class AudioLDM(ModelInterface):
    available_models: list[str] = [
        "audioldm",
        "audioldm-m-full",
        "audioldm-l-full",
        "audioldm-s-full-v2"
    ]

    modifiable_parameters = {
        "num_inference_steps": int,
        "negative_prompt": str
    }

    def __init__(self, model_name: str, output_filename: Path = "audio_ldm_out.wav"):
        self.pipe = AudioLDMPipeline.from_pretrained(f"cvssp/{model_name}", torch_dtype=torch.float16)
        self.pipe = self.pipe.to("cuda")
        self.output_file_name = output_filename


    def generate(self, prompt: str, length_in_seconds: int):
        audio = self.pipe(prompt, num_inference_steps=10, audio_length_in_s=length_in_seconds).audios[0]
        scipy.io.wavfile.write(self.output_file_name, rate=16000, data=audio)


