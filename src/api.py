from src.models.musicgen import MusicGen

if __name__ == "__main__":
    model = "musicgen-small"
    length = 5
    text = "80s pop track with bassy drums and synth"
    out = "../outputs/" + model + "_out.wav"  # FIXME potrzebne będzie lepsze zarządzanie ścieżkami
    musicgen = MusicGen(model, out = out)  # FIXME logika w interfejsie
    musicgen.generate(prompt=text, length_in_seconds=length)