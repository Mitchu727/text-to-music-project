import gradio as gr
from functools import partial

from src.gradio.output_loader import generate_data_for_dataset
from src.gradio.wrappers.hub_gradio_wrapper import HubWrapper
from src.gradio.wrappers.models.audio_ldm_gradio_wrapper import AudioLDMGradioWrapper
from src.api import TextToMusicHub

hub = TextToMusicHub()
hub_wrapper = HubWrapper(hub=hub)


def change_variants_dropdown(model: str):
    """
        Updates the dropdown choices for model variants based on the selected model.
        """
    return gr.Dropdown(choices=hub.get_model(model).available_models, label="variant")


def change_parameters_list(model:str, audioLDMWrapper):
    """
        Changes the visibility of parameter fields based on the selected model.
        If the model is 'audioLDM', the fields are made visible; otherwise, they are hidden.
        """
    if model == "audioLDM":
        return audioLDMWrapper.create_parameters_fields_visible()
    else:
        return audioLDMWrapper.create_parameters_fields_not_visible()


def load_audio(dataset_row):
    """
        Loads the audio file path from the selected dataset row.
        """
    return dataset_row[3]


def reload_dataset():
    """
        Reloads the dataset with new samples.
        """
    samples = generate_data_for_dataset()
    return gr.update(samples=samples)


def display_generation_parameters(dataset_row):
    """
        Displays the generation parameters for the selected dataset row.
        """
    return hub_wrapper.display_generation_parameters(dataset_row[0], dataset_row[3])


if __name__ == "__main__":
    wrapped_change_parameters_list = partial(change_parameters_list, audioLDMWrapper=AudioLDMGradioWrapper)
    samples = generate_data_for_dataset()

    with gr.Blocks() as demo:
        with gr.Tab("Generate music!"):
            default_model = "musicgen"
            model_dropdown = gr.Dropdown(choices=hub.get_available_models(), label="model", value=default_model)
            variants_dropdown = gr.Dropdown(choices=hub.get_model(model_dropdown.value).available_models, label="variant")

            model_dropdown.change(change_variants_dropdown, inputs=model_dropdown, outputs=variants_dropdown)

            input_text = gr.Textbox(value="80s pop track with bassy drums and synth", label="text description")
            length = gr.Slider(value=5, label="Length of the audio (in seconds)", minimum=2, maximum=60, step=1)
            dynamic_parameters = hub_wrapper.make_parameters_for_model_visible(default_model)
            model_dropdown.change(hub_wrapper.make_parameters_for_model_visible, inputs=model_dropdown, outputs=dynamic_parameters)

            run_button = gr.Button("Run")

            audio_output = gr.Audio()

            run_button.click(hub_wrapper.inference, inputs=[model_dropdown, variants_dropdown, input_text, length, *dynamic_parameters], outputs=audio_output)

        with gr.Tab("See previous generations"):
            dataset = gr.Dataset(
                components=["textbox", "textbox", "textbox", "textbox", "number"],
                headers=["Model id", "Model variant", "Prompt", "Generated audio path", "Length"],
                samples=samples
            )
            gr.Button("Refresh").click(reload_dataset, outputs=dataset)
            saved_audio_output = gr.Audio()
            displayed_parameters = hub_wrapper.make_parameters_for_model_visible("None")
            dataset.click(load_audio, inputs=dataset, outputs=saved_audio_output)
            dataset.click(display_generation_parameters, inputs=dataset, outputs=displayed_parameters)

        demo.launch()
