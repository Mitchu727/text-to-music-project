# text-to-music-project
Project for Music Information Retrieval (pol. Wyszukiwanie informacji muzycznych) subject at Warsaw University of Technology

The design proposal is stored in [docs](docs) folder.

# Installation
## Creating env
To create virtual environment, activate it and install neccasary dependiencies run:
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Check setup
To check installation you can run fadtk tests:
```
python -m fadtk.test
```
or our e2e tests:
```
pytest
```

# App
To run gradio app with text to music models inference and option to look up previously generated audio run:
```
python -m src.gradio.app
```

# Generating audio
We provide additional script generate.py for generating audio for specific model based on given promt or promts.

Example usage:
```
python -m src.generate --model musicgen --variant musicgen-small --prompt 'The mood of this song is relaxing. This song can be played in a spa'
python -m src.generate --model audioLDM --variant audioldm-m-full --prompts configs/musiccaps-prompts.txt
```

# Evaluation
For evaluation purposes we used Microsoft's library for Frechet Audio Distance (FAD) calculation - fadtk.

Interactive way of calculating FAD with additional plots and low probability recordings is available via fad_evaluation.ipynb notebook

## MusicCaps 
To download MusicCaps dataset for evaluation purposes, please reffer to [music_caps_dl](https://github.com/seungheondoh/music_caps_dl?tab=readme-ov-file)