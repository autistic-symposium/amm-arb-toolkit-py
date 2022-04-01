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
                        help="Get sell/buy prices for token pair for all exchanges. \
                        Example: bdex -p TOKEN_TO_BUY PAIR QUANTITY")
    parser.add_argument('-x', dest='arbitrage', action='store_true',
                        help="Search arbitrage opportunities.")
    parser.add_argument('-r', dest='algorithm', nargs=1,
                        help="Run arbitrage algorithm for TIME minute. \
                        Example: bdex -r MINUTES")

    return parser


def run_menu() -> None:

    parser = _run_menu_options()
    args = parser.parse_args()
    api = ArbitrageAPI()

    if args.current_block:
        eth_blockNumber = api.get_block_number()
        if eth_blockNumber:
            print(f'\n🧱 Current block number: {eth_blockNumber}\n')

    elif args.balance:
        token = args.balance[0].upper()
        exchange = args.balance[1].upper()

        if token not in api.tokens_address.keys() or \
                exchange not in api.exchanges_address.keys():
            tokens_list = ', '.join([_ for _ in api.tokens_address.keys()])
            ex_list = ', '.join([_ for _ in api.exchanges_address.keys()])
            print(f'\n🚨 Sorry, {token} or {exchange} not supported')
            print(f'🚨 Supported coins: {tokens_list}')
            print(f'🚨 Supported exchanges: {ex_list}\n')

        else:
            balance = api.get_token_balance(token, exchange)
            if balance:
                print(f'\n♜ Balance for {token} at {exchange}: {balance}\n')

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

    elif args.prices:
        token = args.prices[0].upper()
        pair_token = args.prices[1].upper()
        api.set_quantity(args.prices[2])

        if token not in api.tokens_address.keys() or \
                pair_token not in api.tokens_address.keys():
            tokens_list = ", ".join([_ for _ in api.tokens_address.keys()])
            print(f'\n🚨 Sorry, {token} or {pair_token} not supported')
            print(f'🚨 Supported coins: {tokens_list}\n')

        else:
            api.get_all_balances()
            api.get_pair_prices(token, pair_token, api.trading_qty)
            print(f'\n🪙 {api.trading_qty} {token} ({token}/{pair_token}):\n')
            for exchange, price in api.current_prices.items():
                print(f'{exchange}:')
                print(f'                🔺buy: ${price[0]} 🔻sell: ${price[1]}')

    elif args.arbitrage:
        api.get_arbitrage()

        if api.arbitrage_result:
            print(f'\n✅ Found these opportunities (qty: {api.trading_qty}):\n')
            for data in api.arbitrage_result:
                print(f'🤑 profit: {data[0]} DAI')
                print(f'  details: {data[1]}\n')
        else:
            print('\n😭 No arbitrage found.\n')

    elif args.algorithm:

        print(f'\n✅ Running the in a loop of {args.algorithm[0]} minutes..\n')

        api.run_algorithm(float(args.algorithm[0]))

        print(f'\n✅ Done. Results saved at {api.result_dir}.\n')

    else:
        parser.print_help(sys.stderr)


if __name__ == "__main__":
    run_menu()
