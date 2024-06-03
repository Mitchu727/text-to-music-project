from src.gradio.wrappers.models.audio_ldm_2_gradio_wrapper import AudioLDM2GradioWrapper
from src.gradio.wrappers.models.audio_ldm_gradio_wrapper import AudioLDMGradioWrapper
from src.gradio.wrappers.models.model_gradio_wrapper_interface import ModelGradioWrapperInterface
from src.gradio.wrappers.models.music_ldm_gradio_wrapper import MusicLDMGradioWrapper
from src.gradio.wrappers.models.musicgen_gradio_wrapper import MusicGenGradioWrapper


class HubWrapper:
    model_wrappers: list[ModelGradioWrapperInterface] = [AudioLDMGradioWrapper, AudioLDM2GradioWrapper, MusicLDMGradioWrapper, MusicGenGradioWrapper]

    def __init__(self, hub):
        self.hub = hub

    def get_dynamic_parameters(self):
        dynamic_parameter_fields = []
        for model_wrapper in self.model_wrappers:
            dynamic_parameter_fields.extend(model_wrapper.create_parameters_fields_not_visible())

    def make_parameters_for_model_visible(self, model_id):
        dynamic_parameter_fields = []
        for model_wrapper in self.model_wrappers:
            if model_id == model_wrapper.id:
                dynamic_parameter_fields.extend(model_wrapper.create_parameters_fields_visible())
            else:
                dynamic_parameter_fields.extend(model_wrapper.create_parameters_fields_not_visible())
        return dynamic_parameter_fields

    def display_generation_parameters(self, model_id, wav_path):
        generation_parameter_fields = []
        for model_wrapper in self.model_wrappers:
            if model_id == model_wrapper.id:
                generation_parameter_fields.extend(model_wrapper.display_generation_parameters(wav_path))
            else:
                generation_parameter_fields.extend(model_wrapper.create_parameters_fields_not_visible())
        return generation_parameter_fields

    def inference(self, model_id: str, model_variant: str, text: str, length: float, *args):
        model = self.hub.create_model(model_id, model_variant)
        config = self.create_config_from_args(model_id, args)
        audio = model.generate(prompt=text, length_in_seconds=int(length), config=config)
        return audio

    def create_config_from_args(self, model_id, args):
        numerator = 0
        for model_wrapper in self.model_wrappers:
            num_of_parameters = len(model_wrapper.create_parameters_fields_not_visible())
            if model_id == model_wrapper.id:
                return model_wrapper.create_config_from_args(args[numerator:numerator+num_of_parameters])
            else:
                numerator += num_of_parameters
        return {}