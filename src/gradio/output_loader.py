import json
from pathlib import Path

from src.utils import get_project_root

# def wrap_audio_in_markdown(audio_file):
#     return f"<audio src='/file={audio_file}' controls></audio>"

def generate_data_for_dataset():
    path = get_project_root() / "outputs"
    path_list = Path(path).rglob("*.json")
    samples = []
    for path in path_list:
        if Path(str(path).replace(".json", ".wav")).exists():
            sample = []
            with open(path, "r") as f:
                parameters = json.load(f)
            sample.append(parameters["model_id"])
            sample.append(parameters["model_variant"])
            sample.append(parameters["prompt"])
            # sample.append(gr.Audio(value=path.with_suffix(".wav")))
            sample.append(str(path.with_suffix(".wav")))
            sample.append(parameters["length_in_seconds"])
            samples.append(sample)
    return samples
