import pytest

from src.models.musicgen import Musicgen
import os

from src.output.simple_output_saver import SimpleOutputSaver
from test.utils import clean_outputs, output_test_directory

length = 5
text = "80s pop track with bassy drums and synth"
output_saver = SimpleOutputSaver(output_test_directory())


@pytest.mark.parametrize("model_variant", Musicgen.available_models)
def test_musicgen(model_variant, clean_outputs):
    output_file_name = output_test_directory() / f"{model_variant}.wav"
    musicgen = Musicgen(model_variant, output_saver=output_saver)
    musicgen.generate(prompt=text, length_in_seconds=length)
    assert os.path.isfile(output_file_name)



