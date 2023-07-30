import time
from web3 import Web3

from loguru import logger
import random
import asyncio, aiohttp

from config import ERC20_ABI
from settings import MAX_GAS_CHARGE, GAS_WAIT
from data.network_data import DATA

def decimalToInt(num, decimal):
    return num/ (10**decimal)

def intToDecimal(qty, decimal):
    return int(qty * int("".join(["1"] + ["0"]*decimal)))


def sign_tx(web3, contract_txn, privatekey):
    signed_tx = web3.eth.account.sign_transaction(contract_txn, privatekey)
    raw_tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_hash = web3.to_hex(raw_tx_hash)

    return tx_hash


def check_balance(privatekey, chain, address_contract):
    try:
        web3 = Web3(Web3.HTTPProvider(DATA[chain]['rpc']))

        try:
            wallet = web3.eth.account.from_key(privatekey).address
        except:
            wallet = privatekey

        if address_contract == '':  # eth
            balance = web3.eth.get_balance(web3.to_checksum_address(wallet))
            token_decimal = 18
        else:
            token_contract, token_decimal, symbol = check_data_token(chain, address_contract)
            balance = token_contract.functions.balanceOf(web3.to_checksum_address(wallet)).call()

        human_readable = decimalToInt(balance, token_decimal)

        # cprint(human_readable, 'blue')

        return human_readable

    except Exception as error:
        logger.error(error)
        time.sleep(1)
        check_balance(privatekey, chain, address_contract)


def check_data_token(chain, token_address):
    try:

        token_contract = Web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
        decimals = token_contract.functions.decimals().call()
        symbol = token_contract.functions.symbol().call()

        data = {
            'contract': token_contract,
            'decimal': decimals,
            'symbol': symbol
        }

        return token_contract, decimals, symbol

    except Exception as error:
        logger.error(error)

def add_gas_price(web3, contract_txn):
    print('adding gas price')

    gas_price = web3.eth.gas_price
    print('gas price', gas_price)
    contract_txn['gasPrice'] = int(gas_price * random.uniform(1.01, 1.02))
    return contract_txn

def add_gas_limit_layerzero(web3, contract_txn):

    pluser = [1.01, 1.02]
    #gasLimit = web3.eth.estimate_gas(contract_txn)
    gasLimit = 200000
    print('add_gas_limit', gasLimit)
    contract_txn['gas'] = int(gasLimit * random.uniform(pluser[0], pluser[1]))
    return contract_txn

def checker_total_fee(chain, gas):

    gas = decimalToInt(gas, 18) * PRICES_NATIVE[chain]

    # cprint(f'total_gas : {round_to(gas)} $', 'blue')
    logger.info(f'total_gas : {round(gas, 5)} $')

    if gas > MAX_GAS_CHARGE[chain]:
        logger.info(f'gas is too high : {round(gas, 5)}$ > {MAX_GAS_CHARGE[chain]}$. sleep and try again')
        time.sleep(random.randint(GAS_WAIT-3, GAS_WAIT+3))
        return False
    else:
        return True


async def get_prices():
    prices = {
        'ETH': 0, 'BNB': 0, 'AVAX': 0, 'MATIC': 0, 'FTM': 0, 'xDAI': 0, 'CELO': 0, 'COREDAO': 0, 'ONE': 0, 'MOVR': 0,
        'GLMR': 0
    }

    async def get_get(session, symbol):

        url = f'https://min-api.cryptocompare.com/data/price?fsym={symbol}&tsyms=USDT'

        async with session.get(url, timeout=10) as resp:

            try:

                if resp.status == 200:
                    resp_json = await resp.json(content_type=None)

                    try:
                        prices[symbol] = float(resp_json['USDT'])
                    except Exception as error:
                        logger.error(f'{error}. set price : 0')
                        prices[symbol] = 0

                else:
                    await asyncio.sleep(1)
                    return await get_get(session, url)

            except Exception as error:
                await asyncio.sleep(1)
                return await get_get(session, url)

    async with aiohttp.ClientSession() as session:

        tasks = []

        for symbol in prices:
            task = asyncio.create_task(get_get(session, symbol))
            tasks.append(task)

        await asyncio.gather(*tasks)

    data = {
        'avalanche': prices['AVAX'],
        'polygon': prices['MATIC'],
        'ethereum': prices['ETH'],
        'bsc': prices['BNB'],
        'arbitrum': prices['ETH'],
        'optimism': prices['ETH'],
        'fantom': prices['FTM'],
        'zksync': prices['ETH'],
        'nova': prices['ETH'],
        'gnosis': prices['xDAI'],
        'celo': prices['CELO'],
        'polygon_zkevm': prices['ETH'],
        'core': prices['COREDAO'],
        'harmony': prices['ONE'],
        'moonbeam': prices['GLMR'],
        'moonriver': prices['MOVR'],
    }

    return data

def check_status_tx(chain, tx_hash):
    max_time_check_tx_status = 15

    logger.info(f'{chain} : checking tx_status : {tx_hash}')

    start_time_stamp = int(time.time())

    while True:
        try:

            rpc_chain   = DATA[chain]['rpc']
            web3        = Web3(Web3.HTTPProvider(rpc_chain))
            status_     = web3.eth.get_transaction_receipt(tx_hash)
            status      = status_["status"]

            if status in [0, 1]:
                return status

        except Exception as error:
            # logger.info(f'error, try again : {error}')
            time_stamp = int(time.time())
            if time_stamp-start_time_stamp > max_time_check_tx_status:
                logger.info(f'не получили tx_status за {max_time_check_tx_status} sec, думаем что tx is success')
                return 1
            time.sleep(1)

PRICES_NATIVE   = asyncio.run(get_prices())