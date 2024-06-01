from src.models.model_interface import ModelInterface
import torch
from diffusers import AudioLDM2Pipeline

from src.output.output_saver import OutputSaver


class AudioLDM2(ModelInterface):
    id: str = "audioLDM2"
    available_models: list[str] = [
        "audioldm2",
        "audioldm2-large",
        "audioldm2-music"
    ]

    def __init__(self, model_variant: str, output_saver: OutputSaver):
        repo_id = f"cvssp/{model_variant}"
        self.pipe = AudioLDM2Pipeline.from_pretrained(repo_id, torch_dtype=torch.float16)
        self.pipe = self.pipe.to("cuda")
        self.output_saver = output_saver
        self.model_variant = model_variant

    def generate(self, prompt: str, length_in_seconds: int, config: dict = {}):
        audio = self.pipe(
            prompt,
            audio_length_in_s=length_in_seconds,
            **config
        ).audios[0]

        audio_path = self.output_saver.save_generation(
            audio=audio,
            sampling_rate=16000,
            prompt=prompt,
            length_in_seconds=length_in_seconds,
            model_id=self.id,
            model_variant=self.model_variant,
            config=config
        )
        return audio_path

