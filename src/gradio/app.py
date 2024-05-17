import gradio as gr
from src.models.musicgen import MusicGen

class MusicGenerationApp:
    def __init__(self):
        self.models_variants_dict = {"musicgen": ["small", "medium", "large", "melody"]}

    def generate_music(self, model: str, text: str, length: float, melody_file=None):
        if "musicgen" in model:
            musicgen = MusicGen(model)
            musicgen.generate(prompt=text, length_in_seconds=int(length), melody_file=melody_file)
            return "musicgen_out.wav"

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
