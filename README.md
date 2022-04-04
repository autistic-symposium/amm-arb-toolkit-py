# 🪙✨ bdex

<br>


### A package and CLI tool to get data and arbitrage for specified tokens/exchange pools.

<br>

#### Token pairs:

* **WETH/DAI**


#### Exchanges:

* **Uniswap** ([0xa478c2975ab1ea89e8196811f51a7b7ade33eb11](https://etherscan.io/address/0xa478c2975ab1ea89e8196811f51a7b7ade33eb11))
* **Sushiswap** ([0xc3d03e4f041fd4cd388c549ee2a29a9e5075882f](https://etherscan.io/address/0xc3d03e4f041fd4cd388c549ee2a29a9e5075882f))
* **Shebaswap** ([0x8faf958e36c6970497386118030e6297fff8d275](https://etherscan.io/address/0x8faf958e36c6970497386118030e6297fff8d275))
* **Sakeswap** ([0x2ad95483ac838e2884563ad278e933fba96bc242](https://etherscan.io/address/0x2ad95483ac838e2884563ad278e933fba96bc242))
* **Croswap** ([0x60a26d69263ef43e9a68964ba141263f19d71d51)](https://etherscan.io/address/0x60a26d69263ef43e9a68964ba141263f19d71d51)

<br>

---

<br>

## Setting your environment

Add your [Alchemy API key and endpoint](https://dashboard.alchemyapi.io/apps) to a file named `.env`:

```bash
cp .env_example .env
vim .env
```

Create a virtual environment:

```bash
virtualenv venv
source venv/bin/activate
```

Install dependencies:

```bash
make install_deps
```

Install the CLI:

```bash
make install
```

<br>

---

<br>

## Running the CLI

You can run the CLI with:

```
bdex
```

<br>

<img width="807" alt="Screen Shot 2022-04-04 at 1 35 46 AM" src="https://user-images.githubusercontent.com/1130416/161449784-3342293b-e75f-4788-aecb-9a653e363917.png">



<br>

## Checking the latest block


We leverage [Alchemy API endpoint `eth_blockNumber_hex`](https://docs.alchemy.com/alchemy/apis/ethereum/eth_blockNumber_hex) to get the latest block:

```bash
bdex -c
```

<br>

<img width="406" alt="Screen Shot 2022-03-31 at 1 15 25 PM" src="https://user-images.githubusercontent.com/1130416/161032451-685dee8b-8ed3-40c2-9391-191fa2abce35.png">

<br>

<br>

💡 The block number can be checked against [ETHstat](https://ethstats.net/).


<br>

<img width="293" alt="Screen Shot 2022-03-31 at 1 15 19 PM" src="https://user-images.githubusercontent.com/1130416/161032358-86969275-7a72-406d-93bc-73906303a0cb.png">


<br>

💡 We are crafting the checksum address string by hand without directly [Keccak-256 hashing the methods and parameters](https://docs.soliditylang.org/en/develop/abi-spec.html).

<br>

## Getting the token balance for an exchange

We leverage [Alchemy API endpoint `eth_call`](https://docs.alchemy.com/alchemy/apis/ethereum/eth_call) to retrieve the current token balance for a specific exchange:

```bash
bdex -b TOKEN EXCHANGE
```
<br>

<img width="481" alt="Screen Shot 2022-03-31 at 10 26 21 PM" src="https://user-images.githubusercontent.com/1130416/161125262-4a623e23-adc9-4928-98c5-16dd67d3302b.png">



<br>


## Getting all token balances for all the exchanges

 We loop over the previous method for a list of tokens and exchanges:

```bash
bdex -a
```

<br>

<img width="407" alt="Screen Shot 2022-03-31 at 10 26 51 PM" src="https://user-images.githubusercontent.com/1130416/161125283-9a320c9b-a89b-4efa-832e-e0c315e2adf6.png">




<br>


## [Extra] Getting all token balances for all exchanges with Python's web3 library

To be able to compare our results from the previous steps, we implemented an alternative way to fetch pair balances utilizing the [Python web3 library](https://web3py.readthedocs.io/en/stable/):

```bash
bdex -w
```
<br>

<img width="401" alt="Screen Shot 2022-03-31 at 10 27 25 PM" src="https://user-images.githubusercontent.com/1130416/161125363-ced644b9-8011-4f9f-b470-324e5f7e4079.png">


<br>

<br>

💡 For this library, it's necessary to supply the contracts' ABI (in our case, for [DAI](https://api.etherscan.io/api?module=contract&action=getabi&address=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2) and [WETH](https://api.etherscan.io/api?module=contract&action=getabi&address=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2), located at `./docs`)


💡 A third option to verify token balances is through [Etherscan tokenholdings dashboard](https://etherscan.io/tokenholdings?a=0xa478c2975ab1ea89e8196811f51a7b7ade33eb11).


<br>


## Getting trading prices for all the exchanges

To get the current price for `WETH/DAI` in all exchanges (e.g., as shown in [the projects' dashboards](https://v2.info.uniswap.org/pair/0xa478c2975ab1ea89e8196811f51a7b7ade33eb11)), run:


```bash
bdex -p QUANTITY TOKEN1 TOKEN2
```

<br>

Quote for trading 1 `WETH`:

<br>

<img width="533" alt="Screen Shot 2022-04-03 at 8 27 55 PM" src="https://user-images.githubusercontent.com/1130416/161438209-6386b71d-94c8-45aa-a60a-ac7a13b2de26.png">

<br>

Quote for trading 10 `WETH`:

<br>

<img width="544" alt="Screen Shot 2022-04-03 at 8 28 20 PM" src="https://user-images.githubusercontent.com/1130416/161438257-5397cd0d-535c-49b8-8db2-3499e04b22bb.png">

<br>

Quote for trading 100 `WETH`:

<br>


<img width="542" alt="Screen Shot 2022-04-03 at 8 28 46 PM" src="https://user-images.githubusercontent.com/1130416/161438283-4e65810f-d297-4331-9ce2-aa9ef23b3c87.png">


<br>

### How the price is calculated

An AMM replaces the buy and sell orders in an order book market with a liquidity pool of two assets, both valued relative to each other. As one asset is traded for the other, the relative prices of the two assets shift, and the new market rate for both is determined.

The constant product is:

```
token_a_pool_size * token_b_pool_size = constant_product
```

All the exchanges are forks from [UniswapV2](https://uniswap.org/blog/uniswap-v2), so they all use the same price formula for trading:

```
market_price_token1 = token2_balance / token1_balance
```

For example, in a pool with `2,000,000 DAI` and `1,000 WETH`, the constant product is `2,000,000,000` and the market price for `WETH` is `$2,000`.

<br>

#### Buy price (e.g., buying `WETH` in a `WETH/DAI` pool)


To find the buy price for a certain quantity, first, we calculate how much `WETH` needs to remain in balance to keep the constant product unchanged:

```
token1_balance_buy = constant_product / (token2_balance + quantity)
```

Then we calculate how much `WETH` goes out to keep this constant:

```
 t1_amount_out_buy = token1_balance - token1_balance_buy
```

The buy price to reflect this ratio is:

```
buy_price = quantity / t1_amount_out_buy
```

<br>

#### Sell price (e.g., selling `WETH` in a `WETH/DAI` pool)

To find how much we can sell a certain quantity of `WETH` for `DAI`, first, we calculate the ratio of `DAI` in the new pool, as we add `WETH`:

```
token2_balance_buy = constant_product / (token1_balance + quantity)
```

We then calculate how much `DAI` will go out:

```
t2_amount_out_buy = token2_balance + token2_balance_buy
```

We calculate the `DAI` balance reflected with the income `WETH`:

```
token1_balance_sell = constant_product / (token2_balance - quantity)
```

And what's the proportion of `WETH` in the new balance:

```
t1_amount_in_sell = token1_balance + token1_balance_sell
```

We can now calculate the sell price to reflect the balance change, keeping the constant:

```
sell_price = t2_amount_out_buy / t1_amount_in_sell
```


<br>


## Getting arbitrage

Run an algorithm to search for arbitrage in the supported exchanges for a certain buy quantity:

```bash
bdex -x QUANTITY
```

<br>

<img width="538" alt="Screen Shot 2022-04-03 at 11 42 09 PM" src="https://user-images.githubusercontent.com/1130416/161447441-dd7126c9-b307-4ded-bbea-42c2a5e60edb.png">



<br>


<br>

## Running arbitrage algorithm in a loop

To run the arbitrage algorithm for a certain amount of minutes:

```bash
bdex -r MIN
```

<br>

<img width="499" alt="Screen Shot 2022-04-04 at 1 05 07 PM" src="https://user-images.githubusercontent.com/1130416/161511273-cebe71dd-863a-4a5d-a13b-5e85f9b99bef.png">



<br>

<br>

Results are saved into `results/<arbitrage_TIMESTAMP>.txt`.

<br>

Here is an sample of the results of this algorithm running for 100 minutes:

```
{'info': 'BUY for $3497.72 at SHEBASWAP and SELL for $3477.39 at SUSHISWAP', 'arbitrage': '20.33'}
{'info': 'BUY for $3503.86 at SUSHISWAP and SELL for $3437.35 at SHEBASWAP', 'arbitrage': '66.51'}
{'info': 'BUY for $3503.92 at SHEBASWAP and SELL for $3485.1 at SUSHISWAP', 'arbitrage': '18.82'}
{'info': 'BUY for $3523.32 at UNISWAP and SELL for $3500.11 at SUSHISWAP', 'arbitrage': '23.21'}
{'info': 'BUY for $3526.93 at SUSHISWAP and SELL for $3460.71 at SHEBASWAP', 'arbitrage': '66.22'}
{'info': 'BUY for $3527.07 at SUSHISWAP and SELL for $3460.71 at SHEBASWAP', 'arbitrage': '66.36'}
{'info': 'BUY for $3527.96 at SHEBASWAP and SELL for $3511.09 at SUSHISWAP', 'arbitrage': '16.87'}
{'info': 'BUY for $3530.13 at SHEBASWAP and SELL for $3511.09 at SUSHISWAP', 'arbitrage': '19.04'}
{'info': 'BUY for $3532.29 at SHEBASWAP and SELL for $3511.09 at SUSHISWAP', 'arbitrage': '21.20'}
{'info': 'BUY for $3532.29 at SHEBASWAP and SELL for $3511.09 at SUSHISWAP', 'arbitrage': '21.20'}
{'info': 'BUY for $3532.29 at SHEBASWAP and SELL for $3515.7 at SUSHISWAP', 'arbitrage': '16.59'}
{'info': 'BUY for $3532.29 at SHEBASWAP and SELL for $3514.69 at SUSHISWAP', 'arbitrage': '17.60'}
{'info': 'BUY for $3532.29 at SHEBASWAP and SELL for $3514.69 at SUSHISWAP', 'arbitrage': '17.60'}
{'info': 'BUY for $3538.12 at UNISWAP and SELL for $3514.69 at SUSHISWAP', 'arbitrage': '23.43'}
{'info': 'BUY for $3538.12 at UNISWAP and SELL for $3523.08 at SUSHISWAP', 'arbitrage': '15.04'}
{'info': 'BUY for $3549.44 at SHEBASWAP and SELL for $3531.53 at SUSHISWAP', 'arbitrage': '17.91'}
{'info': 'BUY for $3551.94 at UNISWAP and SELL for $3531.53 at SUSHISWAP', 'arbitrage': '20.41'}
{'info': 'BUY for $3558.56 at SUSHISWAP and SELL for $3499.37 at SHEBASWAP', 'arbitrage': '59.19'}
{'info': 'BUY for $3565.29 at SUSHISWAP and SELL for $3499.37 at SHEBASWAP', 'arbitrage': '65.92'}
{'info': 'BUY for $3565.29 at SUSHISWAP and SELL for $3499.37 at SHEBASWAP', 'arbitrage': '65.92'}
{'info': 'BUY for $3563.13 at UNISWAP and SELL for $3538.18 at SUSHISWAP', 'arbitrage': '24.95'}
{'info': 'BUY for $3563.13 at UNISWAP and SELL for $3537.9 at SUSHISWAP', 'arbitrage': '25.23'}
{'info': 'BUY for $3563.13 at UNISWAP and SELL for $3537.82 at SUSHISWAP', 'arbitrage': '25.31'}
{'info': 'BUY for $3563.78 at UNISWAP and SELL for $3537.82 at SUSHISWAP', 'arbitrage': '25.96'}
{'info': 'BUY for $3563.27 at UNISWAP and SELL for $3537.82 at SUSHISWAP', 'arbitrage': '25.45'}
{'info': 'BUY for $3550.51 at UNISWAP and SELL for $3524.36 at SUSHISWAP', 'arbitrage': '26.15'}
{'info': 'BUY for $3550.51 at UNISWAP and SELL for $3524.31 at SUSHISWAP', 'arbitrage': '26.20'}
{'info': 'BUY for $3551.26 at SUSHISWAP and SELL for $3486.79 at SHEBASWAP', 'arbitrage': '64.47'}
{'info': 'BUY for $3541.84 at SHEBASWAP and SELL for $3524.31 at SUSHISWAP', 'arbitrage': '17.53'}
{'info': 'BUY for $3541.81 at SUSHISWAP and SELL for $3474.2 at SHEBASWAP', 'arbitrage': '67.61'}
{'info': 'BUY for $3539.29 at UNISWAP and SELL for $3514.96 at SUSHISWAP', 'arbitrage': '24.33'}
{'info': 'BUY for $3535.69 at SHEBASWAP and SELL for $3514.96 at SUSHISWAP', 'arbitrage': '20.73'}
{'info': 'BUY for $3528.53 at SUSHISWAP and SELL for $3462.25 at SHEBASWAP', 'arbitrage': '66.28'}
```

<br>

## Running arbitrage algorithm in a loop in a Docker container

To run the algorithm in a separated container, first [install Docker](https://docs.docker.com/get-docker/), then build the Docker image:

```bash
docker build -t bdex .
```

Finally, run the container (in a separate terminal tab):

```
docker run -v $(pwd):/results -it bdex sleep infinity
```

Results are available at `results/<arbitrage_TIMESTAMP>.txt`.

💡 You can inspect your container at any time with these commands:

```
docker ps
docker exec -it <container_id> /bin/bash
docker inspect bdex
```

Cleaning up:

```
docker volumes prune
```

<br>


---

<br>

## Development


Install dependencies:

```
pip3 -r requirements-dev.txt
```

### Linting

```
make lint
```

### Running tests

```
make test
```
