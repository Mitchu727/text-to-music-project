import yaml
from src.api import TextToMusicHub
from argparse import HelpFormatter, ArgumentParser
from pathlib import Path
from src.output.complex_output_saver import ComplexOutputSaver
import textwrap
from tqdm import tqdm


def main(ar=None):
    """
        Main function to generate audio from text prompts using specified models and configurations.
        """
    args = get_args(ar)

    with open(args.config, 'r') as file:
        config = yaml.safe_load(file)
    model_config = config[args.model]

    output = ComplexOutputSaver(args.out)
    hub = TextToMusicHub(output)
    model = hub.create_model(args.model, args.variant)

    prompts = [args.prompt]
    if args.prompts != None:
        with open(args.prompts, 'r') as file:
            prompts = file.readlines()
    
    for prompt in tqdm(prompts, total=len(prompts)):
        print(f"Generating for prompt: {prompt}")
        audio_path = model.generate(prompt=prompt, length_in_seconds=args.length, config=model_config)
        print(f"Saved audio in {audio_path}")

    return

class RawFormatter(HelpFormatter):
    """
        Custom formatter class for argument parser help messages to maintain text formatting.
        """
    def _fill_text(self, text, width, indent):
        return "\n".join([textwrap.fill(line, width) for line in textwrap.indent(textwrap.dedent(text), indent).splitlines()])
    

def get_args(args=None):
    """
        Parses command-line arguments for the script.
        Returns a namespace with parsed arguments.
        """

    epilog = f'''
Example usage: 
    python -m src.generate --model musicgen --variant musicgen-small --prompt 'The mood of this song is relaxing. This song can be played in a spa'
    python -m src.generate --model audioLDM --variant audioldm-m-full --prompts configs/musiccaps-prompts.txt

Available model ids and variants:
'''
    models = TextToMusicHub.models
    for model in models:
        epilog+=f"\n{model.id}\n"
        for variant in model.available_models:
            epilog+=f"  {variant}\n" 

    parser = ArgumentParser(description="Generate music from text prompt",
                            epilog=epilog,
                            formatter_class=RawFormatter)

    parser.add_argument('--model', type=str, required=True, help="Model id")
    parser.add_argument('--variant', type=str, required=True, help="Model variant")
    parser.add_argument('--length', type=int, default=10, help="Audio length in s")
    parser.add_argument('--prompt', 
                        type=str, 
                        default='''A female vocalist sings this pleasant pop song. The tempo is medium with a keyboard harmony, 
                        melodious acoustic guitar harmony, bright drumming , steel pan and the sound of birds chirping. The song is mellow, soft, 
                        pleasant, soothing, hopeful, sentimental, sweet and cheerful.this song is a Reggae Pop.''',
                        help="Text prompt")
    parser.add_argument('--out', type=Path, default="outputs/", help="Out directory")
    parser.add_argument('--config', type=Path, default="configs/generate_config.yml", help="Models configs")
    parser.add_argument('--prompts', type=Path, default=None, help="File with prompts in txt format. Overwrites prompt arg")

    return parser.parse_args(args)

if __name__ == "__main__":
    main()
    
