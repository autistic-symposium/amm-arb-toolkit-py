# -*- encoding: utf-8 -*-
# Arbitrage API

import os
import logging
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv

from api.util import hex_to_int, wei_to_eth, send_request, craft_url, open_abi


class ArbritageAPI(object):

    def __init__(self) -> None:

        self.tokens_address = {
            'weth': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
            'dai': '0x6b175474e89094c44da98b954eedeac495271d0f'
        }
        self.exchanges_address = {
            'uniswap': '0xa478c2975ab1ea89e8196811f51a7b7ade33eb11',
            'sushiswap': '0xc3d03e4f041fd4cd388c549ee2a29a9e5075882f',
            'shebaswap': '0x8faf958e36c6970497386118030e6297fff8d275',
            'sakeswap': '0x2ad95483ac838e2884563ad278e933fba96bc242',
            'croswap': '0x60a26d69263ef43e9a68964ba141263f19d71d51'
        }

        self.current_balances = {}
        self.current_balances_web3 = {}
        self.current_prices = {}
        self.provider_url = None
        self.w3_obj = None

        self._load_config()

    def _load_config(self) -> None:

        load_dotenv(Path('.') / '.env')

        ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")
        ALCHEMY_URL = os.getenv("ALCHEMY_URL")

        if not (bool(ALCHEMY_URL) and bool(ALCHEMY_API_KEY)):
            raise Exception('🚨 Please add config to .env file')

        self.provider_url = craft_url(ALCHEMY_URL, ALCHEMY_API_KEY)

    def get_block_number(self) -> dict:

        data = '{"jsonrpc":"2.0", "id":"1", "method": "eth_blockNumber"}'
        response = send_request(self.provider_url, data)

        if response:
            try:
                eth_blockNumber_hex = response['result']
                return hex_to_int(eth_blockNumber_hex)
            except TypeError:
                logging.exception('🚨 Check whether the request is valid.}')

    def get_token_balance(self, token, exchange) -> str:

        token_address = self.tokens_address[token]
        exchange_address = self.exchanges_address[exchange][2:]

        data = '{"jsonrpc": "2.0", "method": "eth_call", "params":' + \
            '[{"data": "' + \
            '0x70a08231000000000000000000000000' + \
            exchange_address + \
            '", "to": "' + \
            token_address + \
            '"}, "latest"], "id": 1}'

        response = send_request(self.provider_url, data)
        try:
            return wei_to_eth(hex_to_int(response['result']))
        except KeyError:
            logging.error(f'🚨 Could not retrieve data: {response}')

    def get_all_balances(self) -> None:

        for exchange in self.exchanges_address.keys():
            self.current_balances[exchange] = {}

            for token in self.tokens_address.keys():
                self.current_balances[exchange][token] = \
                    self.get_token_balance(token, exchange)

    def _get_balance_for_wallet(self, wallet_address, token_obj) -> float:

        balance_wei = token_obj.functions.balanceOf(wallet_address).call()
        return float(self.w3_obj.fromWei(balance_wei, 'ether'))

    def get_balance_through_web3_lib(self) -> None:

        self.w3_obj = Web3(Web3.HTTPProvider(self.provider_url))

        for exchange, contract in self.exchanges_address.items():
            self.current_balances_web3[exchange] = {}
            exchange_address = self.w3_obj.toChecksumAddress(contract)

            for token, contract in self.tokens_address.items():

                abi = open_abi(f'./docs/{token}-abi.json')
                address = self.w3_obj.toChecksumAddress(contract)
                token_obj = self.w3_obj.eth.contract(address=address, abi=abi)

                self.current_balances_web3[exchange][token] = \
                    self._get_balance_for_wallet(exchange_address, token_obj)

    def _calculate_pair_price(self, token1, token2) -> float:

        return token1/token2

    def get_pair_prices(self, token1, token2) -> None:

        for exchange in self.exchanges_address.keys():

            dai_balance = self.current_balances[exchange][token1]
            weth_balance = self.current_balances[exchange][token2]

            self.current_prices[exchange] = \
                self._calculate_pair_price(dai_balance, weth_balance)
