from src.output.output_saver import OutputSaver
from src.utils import get_project_root
import scipy


class SimpleOutputSaver(OutputSaver):
    def __init__(self, output_directory=get_project_root() / "outputs"):
        self.output_directory = output_directory

    def save_generation(self, audio, sampling_rate: int, prompt: str, length_in_seconds: int, model_name: str, model_variant: str, config: dict) -> None:
        output_path = self.output_directory / f"{model_variant}.wav"
        scipy.io.wavfile.write(output_path, rate=sampling_rate, data=audio)