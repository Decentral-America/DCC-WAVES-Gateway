# TN <-> Waves Platform Gateway Framework
This framework allows to easily establish a gateway between any Waves token and the
TN Platform.
## Installation
Clone this repository and edit the config.json file according to your needs. Install the following dependencies:
```
pywaves
flask
```
via pip and run 
```
python setupdb.py
```
then run the gateway by
```
python gateway.py
```
## Configuration of the config file
The config.json file includes all necessary settings that need to be connfigured in order to run a proper gateway:
```
{
    "waves": {
        "gatewayAddress": "<Waves address of the gateway>",
        "gatewaySeed": "<seed of the above devined address>",
        "fee": <the fee you want to collect on the gateway, calculated in the proxy token, e.g., 0.1>,
        "assetId": "<the asset id of the proxy token on the Waves platform>",
        "decimals": <number of decimals of the token>,
        "network": "<Waves network you want to connect to (testnet|stagenent|mainnet)>",
        "node": "<the waves node you want to connect to>",
        "timeInBetweenChecks": <seconds in between a check for a new block>,
        "confirmations": <number of confirmations necessary in order to accept a transaction>
    },
    "tn": {
        "gatewayAddress": "<TN address of the gateway>",
        "gatewaySeed": "<seed of the above devined address>",
        "fee": <the fee you want to collect on the gateway, calculated in the proxy token, e.g., 0.1>,
        "assetId": "<the asset id of the proxy token on the TN platform>",
        "decimals": <number of decimals of the token>,
        "network": "<Waves network you want to connect to (testnet|mainnet)>",
        "node": "<the TN node you want to connect to>",
        "timeInBetweenChecks": <seconds in between a check for a new block>,
        "confirmations": <number of confirmations necessary in order to accept a transaction>
    }
}
```

## Running the gateway
After starting the gateway, it will provide a webpage on port 8080.

## Usage of the gateway
This is a simple gateway for TN tokens to the Waves Platform and vice versa. For sending tokens from the Waves Platform to the TN blockchain, just add the TN address that should receive the tokens as the description of the transfer and send the tokens to the Waves address of the gateway.

For sending tokens from the TN Platform to the Waves blockchain, just add the Waves address that should receive the tokens as the description of the transfer and send the tokens to the TN address of the gateway.

# Disclaimer
USE THIS FRAMEWORK AT YOUR OWN RISK!!! FULL RESPONSIBILITY FOR THE SECURITY AND RELIABILITY OF THE FUNDS TRANSFERRED IS WITH THE OWNER OF THE GATEWAY!!!
