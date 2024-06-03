# text-to-music-project
Project for Music Information Retrieval (pol. Wyszukiwanie informacji muzycznych) subject at Warsaw University of Technology

The design proposal is stored in [docs](docs) folder.

# Virtual environment

To create virtual environment use command:
```
python -m venv env
```
To activate it use command:
```
source env/bin/activate
```


# Tests
To run test use command:
```
pytest
```

# Example usage
```python
hub = TextToMusicHub()
length = 5
text = "80s pop track with bassy drums and synth"
model = hub.create_model("audioLDM2", "audioldm2-music")
model.generate(prompt=text, length_in_seconds=length)
```