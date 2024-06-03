from pathlib import Path
import csv
import random

def get_project_root() -> Path:
    return Path(__file__).parent.parent

def extract_musiccaps_prompts(musiccas_csv: Path, num : int = 100, randomize: bool = True, out: Path = None) -> list[str]:
    promts = []

    # extract prompts
    with open(musiccas_csv, 'r') as file:
        csv_reader=csv.reader(file)
        for row in csv_reader:
            promts.append(row[5])

    if randomize:
        promts = random.sample(promts, num)
    
    promts = promts[:num]
    
    if out != None:
        with open(out, 'w') as file:
            for promt in promts:
                file.write(promt + '\n')

    return promts

        