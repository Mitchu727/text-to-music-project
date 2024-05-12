import gradio as gr

from src.models.audio_ldm import AudioLDM
from src.models.musicgen import Musicgen


def inference(model: str, model_variant: str, text: str, length: float):
    if "musicgen" in model:
        musicgen = Musicgen(model_variant)
        musicgen.generate(prompt=text, length_in_seconds=int(length))
        return "musicgen_out.wav"
    if "audioLDM" in model:
        audio_ldm = AudioLDM(model_variant)
        audio_ldm.generate(prompt=text, length_in_seconds=int(length))
        return "audio_ldm_out.wav"


def change_variants_dropdown(model: str):
    return gr.Dropdown(choices=models_variants_dict[model], label="variant")


models_variants_dict = {
    "musicgen": Musicgen.available_models,
    "audioLDM": AudioLDM.available_models
}

if __name__ == "__main__":
    with gr.Blocks() as demo:
        model_dropdown = gr.Dropdown(choices = models_variants_dict.keys(), label="model", value="musicgen")
        variants_dropdown = gr.Dropdown(choices= models_variants_dict[model_dropdown.value], label="variant")
        model_dropdown.change(change_variants_dropdown, inputs=model_dropdown, outputs=variants_dropdown)

        input_text = gr.Textbox(value="80s pop track with bassy drums and synth", label="text description")
        length = gr.Slider(value=5, label = "Length of the audio (in seconds)", minimum=2, maximum=60, step=1)

        run_button = gr.Button("Run")

        audio_output = gr.Audio()

        run_button.click(inference, inputs=[model_dropdown, variants_dropdown, input_text, length], outputs=audio_output)

        demo.launch()
