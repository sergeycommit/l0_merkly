"__________________________________________________________________________________________________"

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

"__________________________________________________________________________________________________"

"""
Module 2 - merkly

Выберите сети и количество, Merkly работает только с небольшими суммами. Возможность бриджа
проверьте на оф сайте https://minter.merkly.com/gas
"""

BRIDGE_RANDOM = True   # True - рандомное количество из диапазона, False - фиксированное
BRIDGE_AMOUNT_FROM = 0.000001
BRIDGE_AMOUNT_TO = 0.00007
CHAIN_FROM = 'klaytn'
TO_CHAIN = ['celo']  # выбирает одну сеть из списка

"__________________________________________________________________________________________________"

"""
Module 4 - stargate staking

Стейкаем на stargate.finance STG. На балансе дб токены STG
Выберите сети и количество
"""

STAKE_RANDOM = True   # True - рандомное количество из диапазона, False - фиксированное
STAKE_AMOUNT_FROM = 0.000001
STAKE_AMOUNT_TO = 0.00007
STAKE_CHAIN = 'polygon'
ALL_BALANCE_STAKING = True      # True - стейк весь баланс stg, False - стейкать баланс с настройками выше

"__________________________________________________________________________________________________"

"""
Module 6 - sushiswap

Выберите сети и количество.
"""

SUSHI_RANDOM = True   # True - рандомное количество от/до, False - фиксированное

SUSHI_CHAIN = 'polygon'    # сети и контракты добавлять в modules/sushiswap.py
SWAP_TOKEN_FROM = 'ETH'   # сейчас работает только с нативными токенами, укажите нативный токен
SWAP_TOKEN_TO = 'STG'
SWAP_AMOUNT_FROM = 0.000001
SWAP_AMOUNT_TO = 0.00007
SLIPPAGE = 2

"__________________________________________________________________________________________________"

"""
General settings
"""
# контракты veSTG для стейкинга на Stargate. Добавить сюда контракт veSTG для возможности стейкинга в сети
veSTG_TOKEN_CONTRACT = {
    'polygon': '0x3AB2DA31bBD886A7eDF68a6b60D3CDe657D3A15D',
    'fantom': '0x933421675cdc8c280e5f21f0e061e77849293dba',
    'optimism': '0x43d2761ed16C89A2C4342e2B16A3C61Ccf88f05B',
                        }

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
    'dfk'           : 0.1
}
GAS_WAIT = 15

#   Пауза между работой кошельков в сек от/до
WAIT_FROM = 2
WAIT_TO = 5