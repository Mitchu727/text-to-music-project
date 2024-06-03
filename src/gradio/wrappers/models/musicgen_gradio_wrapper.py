import json
from pathlib import Path

from src.gradio.wrappers.models.model_gradio_wrapper_interface import ModelGradioWrapperInterface
from src.models.musicgen import Musicgen
import gradio as gr


class MusicGenGradioWrapper(ModelGradioWrapperInterface):
    id: str = Musicgen.id

    @staticmethod
    def create_parameters_fields_not_visible():
        file_upload = gr.File(label="Upload Melody File (Optional)", visible=False)
        return [file_upload]

    @staticmethod
    def create_parameters_fields_visible():
        file_upload = gr.File(label="Upload Melody File (Optional)", visible=True)
        return [file_upload]

    @staticmethod
    def create_config_from_args(args):
        melody_file = args[0]
        if melody_file:
            return {
                "melody_file": melody_file
            }
        else:
            return {}

    @staticmethod
    def display_generation_parameters(wav_path):
        json_path = Path(wav_path).with_suffix(".json")

        with open(json_path, "r") as f:
            parameters = json.load(f)
        if parameters.get("melody_file") is not None:
            melody_audio_file = gr.File(label="Melody file", value=parameters["melody_file"], interactive=False, visible=True)
        else:
            melody_audio_file = gr.File(label="Melody file", visible=False)

        return [melody_audio_file]
