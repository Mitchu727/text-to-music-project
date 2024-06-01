import torch
from diffusers import AudioLDMPipeline

from src.models.model_interface import ModelInterface
from src.output.complex_output_saver import ComplexOutputSaver


class AudioLDM(ModelInterface):
    id: str = "audioLDM"
    available_models: list[str] = [
        "audioldm",
        "audioldm-m-full",
        "audioldm-l-full",
        "audioldm-s-full-v2"
    ]

    def __init__(self, model_variant: str, output_saver: ComplexOutputSaver):
        self.pipe = AudioLDMPipeline.from_pretrained(f"cvssp/{model_variant}", torch_dtype=torch.float16)
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



