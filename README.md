# blockchain
this project creates a blockchain of cryptocurrency, that sends the transactions using a pubsub net on pubnub.

## Create Virtual Environment
create a python 3.8 venv

## Install all packages

```commandline
pip install -r requirements.txt
```

## Run tests

```commandline
python -m pytest tests
```

## Verify code architecture

go to draw.io and open "block-chain.drawio" file.

## Run the API
fill in the configure variables.
# pn_config.subscribe_key =
# pn_config.publish_key =
# pn_config.secret_key =
# pn_config.uuid =

```commandline
python -m API
```

## Run a peer instance

````commandline
set PEER=True
python -m API
````