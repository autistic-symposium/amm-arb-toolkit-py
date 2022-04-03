# -*- encoding: utf-8 -*-
# Arbitrage API

import os
import time
import logging
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv

from api.util import hex_to_int, wei_to_eth, send_request, \
                        craft_url, open_abi, format_price, \
                        save_results, format_path, create_dir, \
                        format_filename, get_time_now, format_perc


class ArbitrageAPI(object):

    def __init__(self) -> None:

        self.tokens_address = {
            'WETH': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
            'DAI': '0x6b175474e89094c44da98b954eedeac495271d0f'
        }
        self.exchanges_address = {
            'UNISWAP': '0xa478c2975ab1ea89e8196811f51a7b7ade33eb11',
            'SUSHISWAP': '0xc3d03e4f041fd4cd388c549ee2a29a9e5075882f',
            'SHEBASWAP': '0x8faf958e36c6970497386118030e6297fff8d275',
            'SAKESWAP': '0x2ad95483ac838e2884563ad278e933fba96bc242',
            'CROSWAP': '0x60a26d69263ef43e9a68964ba141263f19d71d51'
        }

        self.current_balances = {}
        self.current_balances_web3 = {}
        self.current_price_data = {}
        self.arbitrage_result = {}
        self.provider_url = None
        self.w3_obj = None
        self.result_dir = None
        self.arbitrage_threshold = 0

        self._load_config()

    def _load_config(self) -> None:

        load_dotenv(Path('.') / '.env')

        ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")
        ALCHEMY_URL = os.getenv("ALCHEMY_URL")
        ARBITRAGE_THRESHOLD = os.getenv("ARBITRAGE_THRESHOLD")
        RESULT_DIR = os.getenv("RESULT_DIR")
        MIN_HEALTHY_POOL = os.getenv("MIN_HEALTHY_POOL")

        if not (bool(ALCHEMY_URL) and bool(ALCHEMY_API_KEY) and
                bool(ARBITRAGE_THRESHOLD) and bool(RESULT_DIR)
                and bool(MIN_HEALTHY_POOL)):
            raise Exception('🚨 Please add info to env file')

        self.result_dir = RESULT_DIR
        self.min_healthy_pool = MIN_HEALTHY_POOL
        self.arbitrage_threshold = float(ARBITRAGE_THRESHOLD)
        self.provider_url = craft_url(ALCHEMY_URL, ALCHEMY_API_KEY)

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

    def get_block_number(self) -> dict:

        data = '{"jsonrpc":"2.0", "id":"1", "method": "eth_blockNumber"}'
        response = send_request(self.provider_url, data)

        if response:
            try:
                eth_blockNumber_hex = response['result']
                return hex_to_int(eth_blockNumber_hex)
            except TypeError:
                logging.exception('\n🚨 Check whether the request is valid.}')

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
            logging.error(f'\n🚨 Retrieved data is ill-formatted: {response}')

    def get_all_balances(self) -> None:

        for exchange in self.exchanges_address.keys():
            self.current_balances[exchange] = {}

            for token in self.tokens_address.keys():
                self.current_balances[exchange][token] = \
                    self.get_token_balance(token, exchange)

    def _calculate_price_data(self, t1_balance, t2_balance, quatity) -> float:

        CONSTANT_PRODUCT = t1_balance * t2_balance
        CURRENT_PRICE = t2_balance / t1_balance

        ###########################
        #  Calculate BUY data
        ###########################

        # 1) How much WETH needs to remain in balance to keep the constant
        token1_balance_buy = CONSTANT_PRODUCT / (t2_balance + quatity)

        # 2) How much WETH goes out to keep the constant
        t1_amount_out_buy = t1_balance - token1_balance_buy

        # 3) Buy price to reflect the balances change
        buy_price = quatity / t1_amount_out_buy

        # 4) Difference of buy price to current price
        buy_impact = 1 - (CURRENT_PRICE / buy_price)

        ###########################
        #  Calculate SELL data
        ###########################

        # 1) How much DAI to keep the balances constant
        token2_balance_buy = CONSTANT_PRODUCT / (t1_balance + quatity)

        # 2) How much DAI goes out that constant
        t2_amount_out_buy = t2_balance + token2_balance_buy

        # 3) How the DAI balance reflects with the income WETH
        token1_balance_sell = CONSTANT_PRODUCT / (t2_balance - quatity)

        # 4) The proportion of WETH in the new balance:
        t1_amount_in_sell = t1_balance + token1_balance_sell

        # 5) Sell price to reflect the balances change
        sell_price = t2_amount_out_buy / t1_amount_in_sell

        # 6) Difference of sell price to current price
        sell_impact = 1 - (CURRENT_PRICE / sell_price)

        return [format_price(CURRENT_PRICE), format_price(buy_price),
                format_price(sell_price), format_perc(buy_impact),
                format_perc(sell_impact), CONSTANT_PRODUCT]

    def get_pair_prices(self, token1, token2, quantity) -> None:

        self.get_all_balances()

        for exchange in self.exchanges_address.keys():

            token1_balance = self.current_balances[exchange][token1]
            token2_balance = self.current_balances[exchange][token2]

            price_data = self._calculate_price_data(token1_balance,
                                                    token2_balance,
                                                    float(quantity))

            self.current_price_data[exchange] = {
                    'current_price': price_data[0],
                    'balance_constant': price_data[5],
                    'token1': token1,
                    'token2': token2,
                    'balance_t1': self.current_balances[exchange][token1],
                    'balance_t2': self.current_balances[exchange][token2]
            }

            if float(price_data[5]) <= float(self.min_healthy_pool):
                self.current_price_data[exchange].update({
                    'info': "Pool's unbalanced for at least one token.",
                })

            else:
                self.current_price_data[exchange].update({
                    'buy_price': price_data[1],
                    'sell_price': price_data[2],
                    'buy_impact': price_data[3],
                    'sell_impact': price_data[4],
                    'info': get_time_now(),
                })

    def _calculate_arbitrage_brute_force(self):

        win_buy_price = float('inf')
        win_sell_price = 0
        win_buy_exchange = None
        win_sell_exchange = None

        for exchange, data in self.current_price_data.items():

            if 'buy_price' not in data.keys():
                continue

            buy_price_here = float(data['buy_price'])
            sell_price_here = float(data['sell_price'])

            if buy_price_here < win_buy_price:
                win_buy_price = buy_price_here
                win_buy_exchange = exchange
                continue

            if sell_price_here > win_sell_price:
                win_sell_price = sell_price_here
                win_sell_exchange = exchange
                continue

        arbitrage = win_buy_price - win_sell_price

        if arbitrage > self.arbitrage_threshold:
            info_buy = f"BUY for ${win_buy_price} at {win_buy_exchange} and "
            info_sell = f"SELL for ${win_sell_price} at {win_sell_exchange}"
            self.arbitrage_result['info'] = info_buy + info_sell
            self.arbitrage_result['arbitrage'] = format_price(arbitrage)

    def get_arbitrage(self, quantity, token1=None, token2=None):

        # TODO: handle other tokens (CLI + algorithm)
        token1 = token1 or 'WETH'
        token2 = token2 or 'DAI'

        self.get_pair_prices(token1, token2, quantity)
        self._calculate_arbitrage_brute_force()

    def run_algorithm(self, runtime) -> None:

        results = []
        loop = 0
        runtime = 60 * float(runtime)
        end = time.time() + runtime

        while time.time() < end:

            data = self.get_arbitrage()
            if data:
                print(f'    Loop {loop}: {data}')
                results.append(data)
            loop += loop + 1

            time.sleep(5)

        create_dir(self.result_dir)
        destination = format_path(self.result_dir, format_filename())

        save_results(destination, results)
