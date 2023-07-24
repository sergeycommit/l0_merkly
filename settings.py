"""
General settings
"""

MAX_GAS_CHARGE = {
    'avalanche'     : 1,
    'polygon'       : 0.5,
    'ethereum'      : 3,
    'bsc'           : 0.3,
    'arbitrum'      : 1,
    'optimism'      : 1.5,
    'fantom'        : 0.5,
    'zksync'        : 1,
    'nova'          : 0.1,
    'gnosis'        : 0.1,
    'celo'          : 0.1,
    'polygon_zkevm' : 0.5,
    'core'          : 0.1,
    'harmony'       : 0.1,
}
GAS_WAIT = 15

#   Пауза между работой кошельков в сек от/до
WAIT_FROM = 2
WAIT_TO = 5


"""
Module 1 - binance withdraw
"""

### Для работы модуля необходимо добавить API_KEY и API_SECRET с бинанса в файл binance_withdraw.py
### в соответствующие поля

symbolWithdraw = 'APT'
WITHDRAW_NETWORK = 'APT'  # ETH | BSC | AVAXC | MATIC | ARBITRUM | OPTIMISM | APT etc.
RANDOM_WITHDRAW = True      # True - рандомное количество из диапазона, False - фиксированное
WITHDRAW_AMOUNT_FROM = 0.02
WITHDRAW_AMOUNT_TO = 0.025


"""
Module 2 - merkly

Выберите сети и количество, Merkly работает только с небольшими суммами
"""

BRIDGE_RANDOM = True   # True - рандомное количество из диапазона, False - фиксированное
BRIDGE_AMOUNT_FROM = 0.000001
BRIDGE_AMOUNT_TO = 0.00007
CHAIN_FROM = 'celo'
TO_CHAIN = 'gnosis'   # дешевые сети celo, gnosis, klaytn, fuse
