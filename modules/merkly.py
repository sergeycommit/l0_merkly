from loguru import logger
from web3 import Web3
import random
from eth_abi import encode

from data.network_data import DATA, LAYERZERO_CHAINS_ID
from data.abi_merkly import ABI_MERKLY
from modules.helpers import check_balance, intToDecimal, add_gas_price, add_gas_limit_layerzero, \
    checker_total_fee, sign_tx, check_status_tx


MERKLY_CONTRACTS = {
    'optimism'      : '0xa2c203d7ef78ed80810da8404090f926d67cd892',
    'bsc'           : '0xfdc9018af0e37abf89233554c937eb5068127080',
    'arbitrum'      : '0xaa58e77238f0e4a565343a89a79b4addd744d649',
    'polygon'       : '0xa184998ec58dc1da77a1f9f1e361541257a50cf4',
    # 'polygon_zkevm' : '', пока недоступен
    'zksync'        : '0x6dd28C2c5B91DD63b4d4E78EcAC7139878371768',
    'avalanche'     : '0xe030543b943bdcd6559711ec8d344389c66e1d56',
    'gnosis'        : '0xb58f5110855fbef7a715d325d60543e7d4c18143',
    'fantom'        : '0x97337a9710beb17b8d77ca9175defba5e9afe62e',
    'nova'          : '0x484c402b0c8254bd555b68827239bace7f491023',
    # 'harmony'       : '', # надо конвертировать в one-address
    'core'          : '0xCA230856343C300f0cc2Bd77C89F0fCBeDc45B0f',
    'celo'          : '0xe33519c400b8f040e73aeda2f45dfdd4634a7ca0',
    'moonbeam'      : '0x766b7aC73b0B33fc282BdE1929db023da1fe6458',
    'moonriver'     : '0x97337A9710BEB17b8D77cA9175dEFBA5e9AFE62e',
    'klaytn'        : '0xd02ffae68d902453b44a9e45dc257aca54fb88b2'
}


def get_adapterParams(gaslimit: int, amount: int):
    return Web3.to_hex(encode(["uint16", "uint64", "uint256"], [2, gaslimit, amount])[30:])

def merkly_refuel(privatekey, from_chain, to_chain, amount_from, amount_to):

    try:

        module_str = f'merkly_refuel : {from_chain} => {to_chain}'
        logger.info(module_str)

        balance = float(check_balance(privatekey, from_chain, ''))
        amount = round(random.uniform(amount_from, amount_to), 8)
        print('amount', amount)

        web3        = Web3(Web3.HTTPProvider(DATA[from_chain]['rpc']))
        account     = web3.eth.account.from_key(privatekey)
        wallet      = account.address
        print(wallet)

        contract = web3.eth.contract(address=Web3.to_checksum_address(MERKLY_CONTRACTS[from_chain]), abi=ABI_MERKLY)

        value = intToDecimal(amount, 18)
        adapterParams = get_adapterParams(250000, value) + wallet[2:].lower()
        print('start send value')
        send_value = contract.functions.estimateGasBridgeFee(LAYERZERO_CHAINS_ID[to_chain], False, adapterParams).call()
        print('send_value', send_value)

        contract_txn = contract.functions.bridgeGas(
                LAYERZERO_CHAINS_ID[to_chain],
                '0x0000000000000000000000000000000000000000', # _zroPaymentAddress
                adapterParams
            ).build_transaction(
            {
                "from": wallet,
                "value": send_value[0],
                "nonce": web3.eth.get_transaction_count(wallet),
                'gasPrice': 0,
                'gas': 0,
            }
        )
        print(balance - amount)

        if (balance - amount >= 0):
            print('start')

            if from_chain == 'bsc':
                contract_txn['gasPrice'] = 1000000000 # специально ставим 1 гвей, так транза будет дешевле
            else:
                contract_txn = add_gas_price(web3, contract_txn)

            contract_txn = add_gas_limit_layerzero(web3, contract_txn)

            # смотрим газ, если выше выставленного значения : спим
            total_fee   = int(contract_txn['gas'] * contract_txn['gasPrice'])
            print('total fee', total_fee)
            is_fee      = checker_total_fee(from_chain, total_fee)
            print('isfee', is_fee)
            if is_fee   == False: return merkly_refuel(privatekey, DATA[to_chain]['chain_id'])

            tx_hash = sign_tx(web3, contract_txn, privatekey)
            tx_link = f'{DATA[from_chain]["scan"]}/{tx_hash}'

            status = check_status_tx(from_chain, tx_hash)
            if status == 1:
                logger.success(f'{module_str} | {tx_link}')

            else:
                logger.error(f'{module_str} | tx is failed | {tx_link}')

        else:
            logger.error(f"{module_str} : can't refuel : balance = {balance}")


    except Exception as error:
        logger.error(f'{module_str} | {error}')
