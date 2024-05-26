import gradio as gr
from src.models.musicgen import MusicGen
import librosa
class MusicGenerationApp:
    def __init__(self):
        self.models_variants_dict = {"musicgen": ["small", "medium", "large", "melody"]}

    def generate_music(self, model: str, text: str, length: float, melody_file=None):
        try:
            if "musicgen" in model:
                musicgen = MusicGen(model)
                melody_data = None
                sr = None
                if melody_file:

                    melody_data, sr = librosa.load(melody_file.name, sr=None)
                    print(f"Melody data shape: {melody_data.shape}, sample rate: {sr}")
                output_file = musicgen.generate(prompt=text, length_in_seconds=int(length), melody=melody_data, sr=sr)
                return output_file
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_model_variants(self):
        model_variants = []
        for model, variants in self.models_variants_dict.items():
            for variant in variants:
                model_variants.append(f"{model}-{variant}")
        return model_variants

class GradioInterface:
    def __init__(self, app):
        self.app = app

    def launch_interface(self):
        model_variants = self.app.get_model_variants()
        model_dropdown = gr.Dropdown(model_variants, label="Model")
        input_text = gr.Textbox(value="80s pop track with bassy drums and synth", label="Text Description")
        length = gr.Number(value=5, label="Length of the Audio (in seconds)")
        melody_upload = gr.File(label="Upload Melody File (Optional)")

        app_interface = gr.Interface(
            fn=self.app.generate_music,
            inputs=[model_dropdown, input_text, length, melody_upload],
            outputs="audio",
        )

        app_interface.launch()

if __name__ == "__main__":
    music_app = MusicGenerationApp()
    interface = GradioInterface(music_app)
    interface.launch_interface()
