import time

from loguru import logger
from web3 import Web3
import random
from eth_abi import encode

from settings import *
from data.network_data import DATA, LAYERZERO_CHAINS_ID
from data.abi_stargate import ABI_STARGATE, ABI_STARGATE_APPROVE
from modules.helpers import decimalToInt, check_balance, intToDecimal, add_gas_price, add_gas_limit_layerzero, \
    checker_total_fee, sign_tx, check_status_tx

STG_TOKEN_CONTRACT = '0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590'

def stargate_stake(privatekey, from_chain, amount_from, amount_to):

    try:

        module_str = f'stargate_stake'
        logger.info(module_str)

        balance = float(check_balance(privatekey, from_chain, ''))
        amount = round(random.uniform(amount_from, amount_to), 8)
        print('amount', amount)

        web3        = Web3(Web3.HTTPProvider(DATA[from_chain]['rpc']))
        account     = web3.eth.account.from_key(privatekey)
        wallet      = account.address
        print(wallet)

        contract = web3.eth.contract(address=Web3.to_checksum_address(veSTG_TOKEN_CONTRACT[from_chain]),
                                                                      abi=ABI_STARGATE)

        value = intToDecimal(amount, 18)
        print('value', value)

        contract_txn = contract.functions.create_lock(
                value,
                int(time.time()) + 86400*1093
            ).build_transaction(
            {
                "from": wallet,
                "value": 0,
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

def approve(privatekey, from_chain, amount_from):

    try:

        module_str = f'stargate_stake'
        logger.info(module_str)

        balance = float(check_balance(privatekey, from_chain, ''))
        amount = amount_from
        print('amount', amount)

        web3        = Web3(Web3.HTTPProvider(DATA[from_chain]['rpc']))
        account     = web3.eth.account.from_key(privatekey)
        wallet      = account.address
        print(wallet)

        contract = web3.eth.contract(address=Web3.to_checksum_address(STG_TOKEN_CONTRACT),
                                                                      abi=ABI_STARGATE_APPROVE)

        value = intToDecimal(amount, 18)
        print('value', value)

        contract_txn = contract.functions.approve(
            veSTG_TOKEN_CONTRACT[from_chain],
                value,
                # int(time.time()) + 86400*1093
            ).build_transaction(
            {
                "from": wallet,
                "value": 0,
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