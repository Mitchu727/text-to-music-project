import gradio as gr
from musicgen import inference as musicgen

if __name__ == "__main__":
    models_variants_dict = {"musicgen": ["small", "medium", "large", "melody"]}
    model_variants = []
    for model, variants in models_variants_dict.items():
        for variant in variants:
            model_variants.append(f"{model}-{variant}")


    def inference(model: str, text: str):
        if "musicgen" in model:
            musicgen(model, [text])
            return "musicgen_out.wav"


    model_dropdown = gr.Dropdown(model_variants, label="model")
    input_text = gr.Textbox(value="80s pop track with bassy drums and synth", label="text description")


    demo = gr.Interface(
        fn=inference,
        inputs=[
            model_dropdown,
            input_text,
        ],
        outputs="audio",
    )

    demo.launch()