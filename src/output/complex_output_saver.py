from pathlib import Path

import scipy

from src.output.output_saver import OutputSaver
from src.utils import get_project_root
import os
import json


class ComplexOutputSaver(OutputSaver):
    def __init__(self, output_directory=get_project_root() / "outputs"):
        self.output_directory = output_directory

    def save_generation(self, audio, sampling_rate: int, prompt: str, length_in_seconds: int, model_id: str, model_variant: str, config: dict) -> Path:
        generation_output_directory = self.output_directory / prompt[:80]
        if not os.path.exists(generation_output_directory):
            os.makedirs(generation_output_directory)

        audio_output_filename, generation_parameters_output_filename = self._create_output_paths(generation_output_directory, model_id, model_variant)
        scipy.io.wavfile.write(audio_output_filename, rate=sampling_rate, data=audio)

        generation_parameters = config.copy()
        generation_parameters["prompt"] = prompt
        generation_parameters["length_in_seconds"] = length_in_seconds
        generation_parameters["model_id"] = model_id
        generation_parameters["model_variant"] = model_variant
        with open(generation_parameters_output_filename, "w") as f:
            json.dump(generation_parameters, f, indent=4)
        return audio_output_filename

    def _check_if_files_with_filename_can_be_saved(self, generation_output_directory: Path, filename: str) -> bool:
        audio_output_filename = self._create_audio_output_path(generation_output_directory, filename)
        generation_parameters_output_filename = self._create_generation_parameters_output_path(generation_output_directory, filename)

        return not (os.path.exists(audio_output_filename) and os.path.exists(generation_parameters_output_filename))

    def _create_output_paths(self, generation_output_directory: Path, model_name: str, model_variant: str) -> tuple[Path, Path]:
        filename = f"{model_name}_{model_variant}"

        if not self._check_if_files_with_filename_can_be_saved(generation_output_directory, filename):
            file_index = 1
            filename = f"{model_name}_{model_variant}_{file_index}"
            while not self._check_if_files_with_filename_can_be_saved(generation_output_directory, filename):
                file_index += 1
                filename = f"{model_name}_{model_variant}_{file_index}"

        audio_output_filename = self._create_audio_output_path(generation_output_directory, filename)
        generation_parameters_output_filename = self._create_generation_parameters_output_path(generation_output_directory, filename)
        return audio_output_filename, generation_parameters_output_filename

    @staticmethod
    def _create_audio_output_path(generation_output_directory: Path, filename: str) -> Path:
        return generation_output_directory / f"{filename}.wav"

    @staticmethod
    def _create_generation_parameters_output_path(generation_output_directory: Path, filename: str) -> Path:
        return generation_output_directory / f"{filename}.json"
