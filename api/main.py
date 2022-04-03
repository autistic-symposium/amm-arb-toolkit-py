#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Entry point for KeeperDAO arbitrage exercise

import sys
import argparse

from api.arbitrage import ArbitrageAPI


def _run_menu_options() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description='🪙✨ BDEX arbitrage CLI')

    parser.add_argument('-c', dest='current_block', action='store_true',
                        help="Get current block nunber.")
    parser.add_argument('-a', dest='all_balances', action='store_true',
                        help="Get balance for all tokens and exchanges.")
    parser.add_argument('-w', dest='all_balances_web3', action='store_true',
                        help="Get balance for all tokens/exchanges (web3).")
    parser.add_argument('-b', dest='balance', nargs=2,
                        help="Get current balance for a token in a exchange. \
                        Example: bdex -b TOKEN EXCHANGE")
    parser.add_argument('-p', dest='prices', nargs=3,
                        help="Get prices for N tokens on a pool, for all exchanges. \
                        Example: bdex -p QUANTITY TOKEN PAIR")
    parser.add_argument('-x', dest='arbitrage', nargs=1,
                        help="Search arbitrage opportunities for a given quantity. \
                        Example: bdex -x QUANTITY")
    parser.add_argument('-r', dest='algorithm', nargs=1,
                        help="Run arbitrage algorithm for TIME minute. \
                        Example: bdex -r MINUTES")

    return parser


def run_menu() -> None:

    parser = _run_menu_options()
    args = parser.parse_args()
    api = ArbitrageAPI()

    ########################################
    # Get block number
    ########################################
    if args.current_block:
        eth_blockNumber = api.get_block_number()
        if eth_blockNumber:
            print(f'\n🧱 Current block number: {eth_blockNumber}\n')

    ########################################
    # Get balance for a token in a exchange
    ########################################
    elif args.balance:
        token = args.balance[0].upper()
        exchange = args.balance[1].upper()

        if token not in api.tokens_address.keys() or \
                exchange not in api.exchanges_address.keys():
            tokens_list = ', '.join([_ for _ in api.tokens_address.keys()])
            ex_list = ', '.join([_ for _ in api.exchanges_address.keys()])
            print(f'\n🚨 {token} or {exchange} not supported')
            print(f'🚨 Supported coins: {tokens_list}')
            print(f'🚨 Supported exchanges: {ex_list}\n')

        else:
            balance = api.get_token_balance(token, exchange)
            if balance:
                print(f'\n♜ Balance for {token} at {exchange}: {balance}\n')

    ########################################
    # Get balances for all tokens/exchanges
    ########################################
    elif args.all_balances:
        api.get_all_balances()

        for exchange, token_dict in api.current_balances.items():
            print(f'\n♜ Current token balances for {exchange}:')
            for token, balance in token_dict.items():
                print(f'    ✅ {token}: {balance}')

    elif args.all_balances_web3:
        api.get_balance_through_web3_lib()

        for exchange, token_dict in api.current_balances_web3.items():
            print(f'\n♜ Current token balances for {exchange} (web3):')
            for token, balance in token_dict.items():
                print(f'    ✅ {token}: {balance}')

    ########################################
    # Get prices for a token pair for a qty
    ########################################
    elif args.prices:
        quantity = args.prices[0]
        token1 = args.prices[1].upper()
        token2 = args.prices[2].upper()

        if token1 not in api.tokens_address.keys() or \
                token2 not in api.tokens_address.keys():
            tokens_list = ", ".join([_ for _ in api.tokens_address.keys()])
            print(f'\n🚨 {token1} or {token2} not supported')
            print(f'🚨 Supported coins: {tokens_list}\n')

        else:
            api.get_pair_prices(token1, token2, quantity)

            print(f'\n🪙 Trading {quantity} ({token1}/{token2}):\n')
            for exchange, data in api.current_price_data.items():
                print(f"✅ {exchange}:")
                print(f"MARKET: ${data['current_price']}")
                if 'buy_price' not in data.keys():
                    print(f"{data['info']}")
                    print(f"{token1} balance: {data['balance_t1']}")
                    print(f"{token2} balance: {data['balance_t2']}\n")
                else:
                    print(f"BUY:    ${data['buy_price']}, 🔺{data['buy_impact']}")
                    print(f"SELL:   ${data['sell_price']}, 🔻{data['sell_impact']}\n")

    ########################################
    # Run arbitrage algorithm once
    ########################################
    elif args.arbitrage:
        quantity = args.arbitrage[0]
        api.get_arbitrage(quantity)

        if api.arbitrage_result:
            print(f'\n✅ Found these opportunities (qty: {quantity} WETH):\n')
            for data in api.arbitrage_result:
                print(f'🤑 Profit: ${data[0]} DAI')
                print(f'   Details: {data[1]}\n')
        else:
            print('\n😭 No arbitrage found.\n')

    ########################################
    # Run arbitrage algorithm in a loop
    ########################################
    elif args.algorithm:
        time = args.algorithm[0]

        print(f'\n✅ Running the in a loop of {time} minutes..\n')

        api.run_algorithm(time)

        print(f'\n✅ Done. Results saved at {api.result_dir}.\n')

    ########################################
    # Print help
    ########################################
    else:
        parser.print_help(sys.stderr)


if __name__ == "__main__":
    run_menu()
