from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy

def inference(model: str, text: list[str], out: str = "musicgen_out.wav", max_new_tokens: int = 256):
    processor = AutoProcessor.from_pretrained(f"facebook/{model}")
    model = MusicgenForConditionalGeneration.from_pretrained(f"facebook/{model}")

    inputs = processor(
        text=text,
        padding=True,
        return_tensors="pt",
    )

    audio_values = model.generate(**inputs, max_new_tokens=max_new_tokens)

    sampling_rate = model.config.audio_encoder.sampling_rate
    scipy.io.wavfile.write(out, rate=sampling_rate, data=audio_values[0, 0].numpy())

if __name__ == "__main__":
    inference("musicgen-small", ["90s rock song with loud guitars and heavy drums"])

    