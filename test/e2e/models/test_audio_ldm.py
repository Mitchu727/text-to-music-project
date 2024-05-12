import os

import pytest

from src.models.audio_ldm import AudioLDM
from test.utils import clean_outputs, output_test_directory

length = 5
text = "80s pop track with bassy drums and synth"

@pytest.mark.parametrize("model_name", AudioLDM.available_models)
def test_audioldm(model_name, clean_outputs):
    output_file_name = output_test_directory() / f"{model_name}.wav"
    audio_ldm = AudioLDM(model_name, output_filename=output_file_name)
    audio_ldm.generate(prompt=text, length_in_seconds=length)
    assert os.path.isfile(output_file_name)


