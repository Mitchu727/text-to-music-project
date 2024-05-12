from src.models.audio_ldm import AudioLDM
from src.models.musicgen import Musicgen
from src.utils import get_project_root

if __name__ == "__main__":
    output_path = get_project_root() / "outputs"
    length = 5
    text = "80s pop track with bassy drums and synth"

    # model = "musicgen-large"
    model = "musicgen-melody-large"
    output_file_name = output_path / f"{model}_out.wav"  # FIXME potrzebne będzie lepsze zarządzanie ścieżkami
    musicgen = Musicgen(model, output_filename= output_file_name)
    musicgen.generate(prompt=text, length_in_seconds=length)

    # model = "audioldm"
    # model = "audioldm-m-full"
    # model = "audioldm-s-full-v2"
    # model = "audioldm-l-full"
    # output_file_name = output_path / f"{model}_out.wav"
    # audio_ldm = AudioLDM(model, output_file_name)
    # audio_ldm.generate(prompt=text, length_in_seconds=length)