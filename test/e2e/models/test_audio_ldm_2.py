import pytest

from src.models.audio_ldm_2 import AudioLDM2
from src.output.simple_output_saver import SimpleOutputSaver
from test.utils import output_test_directory, clean_outputs

import os

length = 5
text = "80s pop track with bassy drums and synth"
output_saver = SimpleOutputSaver(output_test_directory())


@pytest.mark.parametrize("model_variant", AudioLDM2.available_models)
def test_audioldm(model_variant, clean_outputs):
    output_file_name = output_test_directory() / f"{model_variant}.wav"
    audio_ldm = AudioLDM2(model_variant, output_saver=output_saver)
    audio_ldm.generate(prompt=text, length_in_seconds=length)
    assert os.path.isfile(output_file_name)
