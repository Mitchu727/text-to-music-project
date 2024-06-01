import gradio as gr

from functools import partial

from src.gradio.output_loader import generate_data_for_dataset
from src.gradio.wrappers.audio_ldm_gradio_wrapper import AudioLDMGradioWrapper
from src.api import TextToMusicHub
import pandas as pd


from src.utils import get_project_root

hub = TextToMusicHub()


def inference(model_name: str, model_variant: str, text: str, length: float, *args):
    model = hub.create_model(model_name, model_variant)
    if model_name == "audioLDM":
        config = AudioLDMGradioWrapper.create_config_from_args(args)
    else:
        config = {}
    audio = model.generate(prompt=text, length_in_seconds=int(length), config=config)
    return audio


def change_variants_dropdown(model: str):
    return gr.Dropdown(choices=hub.get_model(model).available_models, label="variant")


def change_parameters_list(model:str, audioLDMWrapper):
    if model == "audioLDM":
        return audioLDMWrapper.create_parameters_fields_visible()
    else:
        return audioLDMWrapper.create_parameters_fields_not_visible()


def load_audio(dataset_values):
    return dataset_values[3]


def reload_dataset():
    samples = generate_data_for_dataset()
    return gr.update(samples=samples)


if __name__ == "__main__":
    wrapped_change_parameters_list = partial(change_parameters_list, audioLDMWrapper=AudioLDMGradioWrapper)
    samples = generate_data_for_dataset()

    with gr.Blocks() as demo:
        with gr.Tab("Generate music!"):
            model_dropdown = gr.Dropdown(choices=hub.get_available_models(), label="model", value="musicgen")
            variants_dropdown = gr.Dropdown(choices=hub.get_model(model_dropdown.value).available_models, label="variant")

            model_dropdown.change(change_variants_dropdown, inputs=model_dropdown, outputs=variants_dropdown)

            audio_ldm_parameters = AudioLDMGradioWrapper.create_parameters_fields_not_visible()
            model_dropdown.change(wrapped_change_parameters_list, inputs=model_dropdown, outputs=audio_ldm_parameters)

            input_text = gr.Textbox(value="80s pop track with bassy drums and synth", label="text description")
            length = gr.Slider(value=5, label="Length of the audio (in seconds)", minimum=2, maximum=60, step=1)

            run_button = gr.Button("Run")

            audio_output = gr.Audio()

            run_button.click(inference, inputs=[model_dropdown, variants_dropdown, input_text, length, *audio_ldm_parameters], outputs=audio_output)

        with gr.Tab("See previous generations"):
            dataset = gr.Dataset(
                components=["textbox", "textbox", "textbox", "textbox", "number"],
                headers=["Model id", "Model variant", "Prompt", "Generated audio path", "Length"],
                samples=samples
            )
            gr.Button("Refresh").click(reload_dataset, outputs=dataset)
            saved_audio_output = gr.Audio()
            dataset.click(load_audio, inputs=dataset, outputs=saved_audio_output)

        demo.launch()
