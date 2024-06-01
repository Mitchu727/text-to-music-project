from src.models.musicgen import Musicgen
import gradio as gr
import librosa

class MusicGenGradioWrapper:
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
