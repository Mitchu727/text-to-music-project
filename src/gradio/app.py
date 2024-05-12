import gradio as gr
from src.models.musicgen import Musicgen

if __name__ == "__main__":
    models_variants_dict = {"musicgen": ["small", "medium", "large", "melody"]}
    model_variants = []
    for model, variants in models_variants_dict.items():
        for variant in variants:
            model_variants.append(f"{model}-{variant}")
    #  TODO to można dać jako składową klasy


    #  TODO to można wyrzucić do jakiejś klasy
    def inference(model: str, text: str, length: float):
        if "musicgen" in model:
            musicgen = Musicgen(model)  # FIXME logika w interfejsie
            musicgen.generate(prompt=text, length_in_seconds=int(length))
            return "musicgen_out.wav"


    model_dropdown = gr.Dropdown(model_variants, label="model")
    input_text = gr.Textbox(value="80s pop track with bassy drums and synth", label="text description")
    length = gr.Number(value=5 ,label = "Length of the audio (in seconds)")


    app = gr.Interface(
        fn=inference,
        inputs=[
            model_dropdown,
            input_text,
            length
        ],
        outputs="audio",
    )

    app.launch()