import time
import requests
import json

from loguru import logger
from web3 import Web3
import random
from eth_abi import encode

from settings import *
from data.network_data import DATA, LAYERZERO_CHAINS_ID
from data.abi_sushi import ABI_SUSHI
from modules.helpers import decimalToInt, check_balance, intToDecimal, add_gas_price, add_gas_limit_layerzero, \
    checker_total_fee, sign_tx, check_status_tx


SUSHISWAP_CONTRACTS = {
    'ethereum'      : '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F',
    'optimism'      : '0x4C5D5234f232BD2D76B96aA33F5AE4FCF0E4BFAb',
    'bsc'           : '0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506',
    'arbitrum'      : '0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506',
    'nova'          : '0x1b02da8cb0d097eb8d57a175b88c7d8b47997506',
    'polygon'       : '0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506',
    'polygon_zkevm' : '',
    'fantom'        : '0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506',
    'zksync'        : '',
    'zksync_lite'   : '',
    'starknet'      : '',
}

TOKEN_CONTRACTS = {
    'ethereum'      : '',
    'optimism'      : {'ETH': '0x4200000000000000000000000000000000000006',
                       "STG": '0x296f55f8fb28e498b858d0bcda06d955b2cb3f97'},
    'bsc'           : '',
    'arbitrum'      : '',
    'nova'          : {'ETH': '0x722E8BdD2ce80A4422E880164f2079488e115365',
                       'STG': '0x08cF9090443691532A5227aD18F9d18c59398837'},
    'polygon'       : {'MATIC': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270',
                       "STG": '0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590'},
    'polygon_zkevm' : '',
    'fantom'        : '',
    'zksync'        : '',
    'zksync_lite'   : '',
    'starknet'      : '',
}

def sushi(privatekey, from_chain, token_from, token_to, amount_from, amount_to, slippage):

    try:
        from_token = Web3.to_checksum_address(TOKEN_CONTRACTS[from_chain][token_from])
        to_token = Web3.to_checksum_address(TOKEN_CONTRACTS[from_chain][token_to])

        module_str = f'stargate_stake'
        logger.info(module_str)

        balance = float(check_balance(privatekey, from_chain, ''))
        amount = round(random.uniform(amount_from, amount_to), 8)
        print('amount', amount)

        web3        = Web3(Web3.HTTPProvider(DATA[from_chain]['rpc']))
        account     = web3.eth.account.from_key(privatekey)
        wallet      = account.address
        print(wallet)

        contract = web3.eth.contract(address=Web3.to_checksum_address(SUSHISWAP_CONTRACTS[from_chain]),
                                                                      abi=ABI_SUSHI)

        value = intToDecimal(amount, 18)
        print('value', value)
        response = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={token_from}&tsyms={token_to}').text
        stg_price = json.loads(response)[token_to]
        print(value*stg_price)

        contract_txn = contract.functions.swapExactETHForTokens(
            int(value*stg_price*((100-slippage)/100)),  # amountOutMin
            [from_token, to_token],  # path
            wallet,  # receiver
            (int(time.time()) + 10000)  # deadline
        ).build_transaction(
            {
                "from": wallet,
                "value": value,
                "nonce": web3.eth.get_transaction_count(wallet),
                'gasPrice': 0,
                'gas': 0,
            }
        )

        if from_chain == 'bsc':
                contract_txn['gasPrice'] = 1000000000 # специально ставим 1 гвей, так транза будет дешевле
        else:
                contract_txn = add_gas_price(web3, contract_txn)

        contract_txn = add_gas_limit_layerzero(web3, contract_txn)

        # смотрим газ, если выше выставленного значения : спим
        total_fee = int(contract_txn['gas'] * contract_txn['gasPrice'])
        print('total fee', total_fee)
        is_fee = checker_total_fee(from_chain, total_fee)
        print('isfee', is_fee)

        tx_hash = sign_tx(web3, contract_txn, privatekey)
        tx_link = f'{DATA[from_chain]["scan"]}/{tx_hash}'

        status = check_status_tx(from_chain, tx_hash)
        if status == 1:
            logger.success(f'{module_str} | {tx_link}')

        else:
            logger.error(f'{module_str} | tx is failed | {tx_link}')


    except Exception as error:
        logger.error(f'{module_str} | {error}')
