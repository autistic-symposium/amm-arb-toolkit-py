#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Entry point for KeeperDAO arbritage exercise

import sys
import argparse

from api.arbritage import ArbritageAPI


def _run_menu_options() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description='🪙✨ BDEX arbritage CLI')

    parser.add_argument('-c', dest='current_block', action='store_true',
                        help="Get current block nunber.")
    parser.add_argument('-b', dest='balance', nargs=2,
                        help="Get current balance for a token in a exchange. \
                        Example: bdex -b dai uniswap")
    parser.add_argument('-a', dest='all_balances', action='store_true',
                        help="Get balance for all tokens and exchanges.")
    parser.add_argument('-w', dest='all_balances_web3', action='store_true',
                        help="Get balance for all tokens and exchanges (web3).")
    parser.add_argument('-p', dest='prices', nargs=2,
                        help="Get prices for token pair for all exchanges. \
                        Example: bdex -p dai weth")

    return parser


def run_menu() -> None:

    parser = _run_menu_options()
    args = parser.parse_args()
    api = ArbritageAPI()

    if args.current_block:
        eth_blockNumber = api.get_block_number()
        if eth_blockNumber:
            print(f'\n🧱 Current block number: {eth_blockNumber}\n')

    elif args.balance:
        token = args.balance[0].lower()
        exchange = args.balance[1].lower()

        if token not in api.tokens_address.keys() or \
            exchange not in api.exchanges_address.keys():
            print(f'🚨 Sorry, {token} or {exchange} not supported')
            print(f'🚨 Supported coins: {api.tokens_address.keys()}')
            print(f'🚨 Supported exchanges: {api.exchanges_address.keys()}')

        else:
            balance = api.get_token_balance(token, exchange)
            if balance:
                print(f'\n👛 Balance for {token} at {exchange}: {balance}\n')

    elif args.all_balances:
        api.get_all_balances()

        for exchange, token_dict in api.current_balances.items():
            print(f'\n👛 Current token balances for {exchange.upper()}:')
            for token, balance in token_dict.items():
                print(f'    {token.upper()}: {balance}')

    elif args.all_balances_web3:
        api.get_balance_through_web3_lib()

        for exchange, token_dict in api.current_balances_web3.items():
            print(f'\n👛 Current token balances for {exchange.upper()} (web3):')
            for token, balance in token_dict.items():
                print(f'    {token.upper()}: {balance}')

    elif args.prices:
        token1 = args.prices[0].lower()
        token2 = args.prices[1].lower()

        if token1 not in api.tokens_address.keys() or \
            token2 not in api.tokens_address.keys():
            print(f'🚨 Sorry, {token1} or {token2} not supported')
            print(f'🚨 Supported coins: {api.tokens_address.keys()}')

        else:
            api.get_all_balances()
            api.get_pair_prices(token1, token2)
            for exchange, price in api.current_prices.items():
                print(f'🪙 {token1.upper()}/{token2.upper()} at {exchange}: ${price}')

    else:
        parser.print_help(sys.stderr)


if __name__ == "__main__":
    run_menu()
