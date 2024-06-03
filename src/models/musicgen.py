import librosa
from transformers import AutoProcessor, MusicgenForConditionalGeneration

from src.models.model_interface import ModelInterface
from src.output.output_saver import OutputSaver


class Musicgen(ModelInterface):
    id: str = "musicgen"
    available_models: list[str] = [
        "musicgen-small",
        "musicgen-medium",
        "musicgen-large",
        "musicgen-melody",
        "musicgen-melody-large"
    ]

    modifiable_parameters = {}

    def __init__(self, model_variant: str, output_saver: OutputSaver):
        self.processor = AutoProcessor.from_pretrained(f"facebook/{model_variant}")
        self.model = MusicgenForConditionalGeneration.from_pretrained(f"facebook/{model_variant}").half().to('cuda')
        self.model_variant = model_variant
        self.output_saver = output_saver

    def generate(self, prompt: str, length_in_seconds: int, config: dict = {}):
        inputs = self.processor(
            text=[prompt],
            padding=True,
            return_tensors="pt",
        )

        length_in_tokens = int(length_in_seconds * 256 / 5)
        if config.get("melody_file") is not None:
            melody, sr = librosa.load(config["melody_file"], sr=None)
            if melody is not None and sr is not None:
                melody_inputs = self.processor(
                    text=[prompt],
                    audio=melody,
                    sampling_rate=sr,
                    padding=True,
                    return_tensors="pt",
                )
                inputs.update(melody_inputs)
        inputs = inputs.to('cuda')
        audio_values = self.model.generate(**inputs, max_new_tokens=length_in_tokens).cpu().float()

        sampling_rate = self.model.config.audio_encoder.sampling_rate
        audio_path = self.output_saver.save_generation(
            audio=audio_values[0, 0].numpy(),
            sampling_rate=sampling_rate,
            prompt=prompt,
            length_in_seconds=length_in_seconds,
            model_id=self.id,
            model_variant=self.model_variant,
            config=config
        )
        return audio_path