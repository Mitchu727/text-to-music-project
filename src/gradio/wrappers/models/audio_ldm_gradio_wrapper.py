from pathlib import Path

import gradio as gr

from src.gradio.wrappers.models.model_gradio_wrapper_interface import ModelGradioWrapperInterface
from src.models.audio_ldm import AudioLDM
import json


class AudioLDMGradioWrapper(ModelGradioWrapperInterface):
    id: str = AudioLDM.id

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
    def display_generation_parameters(wav_path):
        json_path = Path(wav_path).with_suffix(".json")
        with open(json_path, "r") as f:
            parameters = json.load(f)

        num_inference_steps = gr.Number(label="Number of inference steps", value=parameters["num_inference_steps"], interactive=False, visible=True)

        if parameters.get("negative_prompt") is not None:
            negative_prompt = gr.Textbox(label="Negative prompt", value=parameters["negative_prompt"], interactive=False, visible=True)
        else:
            negative_prompt = gr.Textbox(label="Negative prompt", visible=False)
        guidance_scale = gr.Number(label="Guidance scale", value=parameters["guidance_scale"], interactive=False, visible=True)
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