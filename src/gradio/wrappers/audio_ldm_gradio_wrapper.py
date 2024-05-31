import gradio as gr


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