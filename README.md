# text-to-music-project
Project for Music Information Retrieval (pol. Wyszukiwanie informacji muzycznych) subject at Warsaw University of Technology

The design proposal is stored in [docs](docs) folder.

# Virtual environment

To create virtual environment use command:
```
python -m virtualenv env --python=3.10
```



To activate it use command:
```
source env/bin/activate
```

Install mustango:
```
git clone https://github.com/AMAAI-Lab/mustango
cd mustango
pip install -r requirements.txt
cd diffusers
pip install -e .
```

Install requirements:
```
pip install -r requirements
```


# Tests
To run test use command:
```
pytest
```
