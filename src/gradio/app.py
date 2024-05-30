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

# def change_parameters_dropdown(model: str):
#     if model =
#     return gr.Dropdown(choices=models_variants_dict[model], label="variant")

def change_parameters_list(model:str):
    if model == "audioLDM":
        return AudioLDMGradioWrapper().create_parameters_fields_visible()

    if model == "musicgen":
        return AudioLDMGradioWrapper().create_parameters_fields_not_visible()


models_variants_dict = {
    "musicgen": Musicgen.available_models,
    "audioLDM": AudioLDM.available_models
}

models_parameters_dict = {
    "musicgen": Musicgen.modifiable_parameters,
    "audioLDM": AudioLDM.modifiable_parameters
}


class AudioLDMGradioWrapper:
    id: str = "audioLDM"

    def create_parameters_fields_not_visible(self):
        num_inference_steps = gr.Number(label="Number of inference steps", value=10, interactive=True, visible=False)
        negative_prompt = gr.Textbox(label="Negative prompt", value=None, interactive=True, visible=False)
        return [num_inference_steps, negative_prompt]


    def create_parameters_fields_visible(self):
        num_inference_steps = gr.Number(label="Number of inference steps", value=10, interactive=True, visible=True)
        negative_prompt = gr.Textbox(label="Negative prompt", value=None, interactive=True, visible=True)
        return [num_inference_steps, negative_prompt]



if __name__ == "__main__":

    audioLDMWrapper = AudioLDMGradioWrapper()
    with gr.Blocks() as demo:
        model_dropdown = gr.Dropdown(choices=models_variants_dict.keys(), label="model", value="musicgen")
        variants_dropdown = gr.Dropdown(choices=models_variants_dict[model_dropdown.value], label="variant")

        model_dropdown.change(change_variants_dropdown, inputs=model_dropdown, outputs=variants_dropdown)

        audio_ldm_parameters = audioLDMWrapper.create_parameters_fields_not_visible()
        model_dropdown.change(change_parameters_list, inputs=model_dropdown, outputs=audio_ldm_parameters)

        input_text = gr.Textbox(value="80s pop track with bassy drums and synth", label="text description")
        length = gr.Slider(value=5, label="Length of the audio (in seconds)", minimum=2, maximum=60, step=1)

        run_button = gr.Button("Run")

        audio_output = gr.Audio()

        run_button.click(inference, inputs=[model_dropdown, variants_dropdown, input_text, length], outputs=audio_output)
        demo.launch()