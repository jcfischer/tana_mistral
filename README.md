# tana_mistral

## Install / setup
`pip install poetry`
`poetry env use 3.11`
`source .venv/bin/activate`
`poetry install`

Check basic install is correct
`python smoketest.py`

## Using
* Export your Tana workspace as JSON format, saving the file somewhere.
* run `python index_data.py -f <dumpfile>` to index your json dump
* run `python verify_data.py` to check all is well
  
* run `python app.py` to run the flask app 
* Create a Tana `Command Node` that looks like this: 
* _(change port to 8001)_
![Command Node](docs/ask_mistral_command_node.png)

Now you can write a line of text in Tana and CMD-K "Ask Mistral"