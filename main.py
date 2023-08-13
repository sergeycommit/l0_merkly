import random
import time

from modules.merkly import merkly_refuel
from modules.binance_withdraw import binance_withdraw
from modules.stargate_staking import stargate_stake, approve
from modules.sushiswap import sushi
from modules.erc20_generator import erc20_generate
from settings import *

if __name__ == "__main__":
    print(f'----------------------------------------------------'
          f'\n      Subscribe to us : https://t.me/my_utils\n'
          f'----------------------------------------------------')

    MODULE = int(input('''
        MODULE:
        0.  generate_evm_wallets
        1.  binance_withdraw
        2.  merkly
        3.  stargate_bridge (soon)
        4.  stake_stargate
        5.  snapshoter (soon)
        6.  sushiswap
        Выберите модуль (0 - 6) : '''))

    with open('private_keys.txt', 'r', encoding='utf-8-sig') as file:
        private_keys = [row.strip() for row in file]

    if MODULE == 0:
        erc20_generate(WAIT_FROM, WAIT_TO)

    elif MODULE == 1:
        with open('withdraw_addresses', 'r', encoding='utf-8-sig') as f:
            addresses = [row.strip() for row in f]

        for address in addresses:
            if RANDOM_WITHDRAW:
                amount = round(random.uniform(WITHDRAW_AMOUNT_FROM, WITHDRAW_AMOUNT_TO), 8)
                print(amount)
            else:
                amount = WITHDRAW_AMOUNT_FROM
            binance_withdraw(address, amount, symbolWithdraw, WITHDRAW_NETWORK)
            time.sleep(random.randint(WAIT_FROM, WAIT_TO))

    elif MODULE == 2:
        for key in private_keys:
            merkly_refuel(key, CHAIN_FROM, random.choice(TO_CHAIN), BRIDGE_AMOUNT_FROM, BRIDGE_AMOUNT_TO)
            time.sleep(random.randint(WAIT_FROM, WAIT_TO))

    elif MODULE == 4:
        for key in private_keys:
            approve(key, STAKE_CHAIN, STAKE_AMOUNT_TO)
            stargate_stake(key, STAKE_CHAIN, STAKE_AMOUNT_FROM, STAKE_AMOUNT_TO, ALL_BALANCE_STAKING)
            time.sleep(random.randint(WAIT_FROM, WAIT_TO))

    elif MODULE == 6:
        for key in private_keys:
            sushi(key, SUSHI_CHAIN.lower(), SWAP_TOKEN_FROM.upper(), SWAP_TOKEN_TO.upper(),
                  SWAP_AMOUNT_FROM, SWAP_AMOUNT_TO, SLIPPAGE)
            time.sleep(random.randint(WAIT_FROM, WAIT_TO))
