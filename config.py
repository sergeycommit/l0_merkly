import json

with open(fr"data/erc20_abi.json", "r") as file:
    ERC20_ABI = json.load(file)