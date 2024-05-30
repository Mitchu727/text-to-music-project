import gradio as gr

from src.models.audio_ldm import AudioLDM
from src.models.musicgen import Musicgen
from functools import partial

def inference(model: str, model_variant: str, text: str, length: float, *args):
    print(args)
    if "musicgen" in model:
        musicgen = Musicgen(model_variant)
        musicgen.generate(prompt=text, length_in_seconds=int(length))
        return "musicgen_out.wav"
    if "audioLDM" in model:
        config = AudioLDMGradioWrapper.create_config_from_args(args)
        print(config)
        audio_ldm = AudioLDM(model_variant)
        audio_ldm.generate(prompt=text, length_in_seconds=int(length), config=config)
        return "audio_ldm_out.wav"


def change_variants_dropdown(model: str):
    return gr.Dropdown(choices=models_variants_dict[model], label="variant")

# def change_parameters_dropdown(model: str):
#     if model =
#     return gr.Dropdown(choices=models_variants_dict[model], label="variant")


def change_parameters_list(model:str, audioLDMWrapper):
    if model == "audioLDM":
        return audioLDMWrapper.create_parameters_fields_visible()

    if model == "musicgen":
        return audioLDMWrapper.create_parameters_fields_not_visible()


models_variants_dict = {
    "musicgen": Musicgen.available_models,
    "audioLDM": AudioLDM.available_models
}


class AudioLDMGradioWrapper:
    id: str = "audioLDM"

    @staticmethod
    def create_parameters_fields_not_visible():
        num_inference_steps = gr.Number(label="Number of inference steps", value=10, interactive=True, visible=False)
        negative_prompt = gr.Textbox(label="Negative prompt", value=None, interactive=True, visible=False)
        guidance_scale = gr.Number(label="Guidance scale", value=2.5, interactive=True, visible=False)
        return [num_inference_steps, negative_prompt, guidance_scale]

    @staticmethod
    def create_parameters_fields_visible():
        num_inference_steps = gr.Number(label="Number of inference steps", value=10, interactive=True, visible=True)
        negative_prompt = gr.Textbox(label="Negative prompt", value=None, interactive=True, visible=True)
        guidance_scale = gr.Number(label="Guidance scale", value=2.5, interactive=True, visible=True)
        return [num_inference_steps, negative_prompt, guidance_scale]

    @staticmethod
    def create_config_from_args(args):
        if args[1] == "":
            return {
                "num_inference_steps": args[0],
                "guidance_scale": args[2]
            }
        else:
            return {
                "num_inference_steps": args[0],
                "negative_prompt": args[1],
                "guidance_scale": args[2]
        }

if __name__ == "__main__":
    # audioLDMWrapper = AudioLDMGradioWrapper()

    wrapped_change_parameters_list = partial(change_parameters_list, audioLDMWrapper=AudioLDMGradioWrapper)

    with gr.Blocks() as demo:
        model_dropdown = gr.Dropdown(choices=models_variants_dict.keys(), label="model", value="musicgen")
        variants_dropdown = gr.Dropdown(choices=models_variants_dict[model_dropdown.value], label="variant")

        model_dropdown.change(change_variants_dropdown, inputs=model_dropdown, outputs=variants_dropdown)

        audio_ldm_parameters = AudioLDMGradioWrapper.create_parameters_fields_not_visible()
        model_dropdown.change(wrapped_change_parameters_list, inputs=model_dropdown, outputs=audio_ldm_parameters)

        input_text = gr.Textbox(value="80s pop track with bassy drums and synth", label="text description")
        length = gr.Slider(value=5, label="Length of the audio (in seconds)", minimum=2, maximum=60, step=1)

        run_button = gr.Button("Run")

        audio_output = gr.Audio()

        run_button.click(inference, inputs=[model_dropdown, variants_dropdown, input_text, length, *audio_ldm_parameters], outputs=audio_output)
        demo.launch()