import ccxt

# api_keys of binance
API_KEY = "key"
API_SECRET = "secret"


def binance_withdraw(address, amount_to_withdrawal, symbolWithdraw, network):
    account_binance = ccxt.binance({
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot'
        }
    })

    try:
        account_binance.withdraw(
            code=symbolWithdraw,
            amount=amount_to_withdrawal,
            address=address,
            tag=None,
            params={
                "network": network
            }
        )
        print(f">>> Успешно | {address} | {amount_to_withdrawal}")
    except Exception as error:
        print(f">>> Неудачно | {address} | ошибка : {error}")
