import random

from modules.merkly import merkly_refuel
from modules.binance_withdraw import binance_withdraw
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
        4.  add_liquidity_stargate (soon)
        5.  snapshoter (soon)
        Выберите модуль (0 - 5) : '''))

    with open('private_keys.txt', 'r', encoding='utf-8-sig') as file:
        private_keys = [row.strip() for row in file]

    if MODULE == 1:
        with open('withdraw_addresses', 'r', encoding='utf-8-sig') as f:
            addresses = [row.strip() for row in f]

        for address in addresses:
            if RANDOM_WITHDRAW:
                amount = random.uniform(WITHDRAW_AMOUNT_FROM, WITHDRAW_AMOUNT_TO)
            else:
                amount = WITHDRAW_AMOUNT_FROM
            binance_withdraw(address, amount, symbolWithdraw, WITHDRAW_NETWORK)


    if MODULE == 2:
        for key in private_keys:
            merkly_refuel(key, CHAIN_FROM, TO_CHAIN, BRIDGE_AMOUNT_FROM, BRIDGE_AMOUNT_TO)