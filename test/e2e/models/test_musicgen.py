import pytest

from src.models.musicgen import Musicgen
import os
from test.utils import clean_outputs, output_test_directory

length = 5
text = "80s pop track with bassy drums and synth"

@pytest.mark.parametrize("model_name", Musicgen.available_models)
def test_musicgen(model_name, clean_outputs):
    output_file_name = output_test_directory() / f"{model_name}.wav"
    musicgen = Musicgen(model_name, output_filename=output_file_name)
    musicgen.generate(prompt=text, length_in_seconds=length)
    assert os.path.isfile(output_file_name)



