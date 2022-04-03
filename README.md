# 🪙✨ bdex

<br>


### A package and CLI tool to get data and arbitrage for specified tokens/exchange pools.

<br>

#### Token pairs:

* ETH/DAI


#### Exchanges:

* Uniswap ([0xa478c2975ab1ea89e8196811f51a7b7ade33eb11](https://etherscan.io/address/0xa478c2975ab1ea89e8196811f51a7b7ade33eb11))
* Sushiswap ([0xc3d03e4f041fd4cd388c549ee2a29a9e5075882f](https://etherscan.io/address/0xc3d03e4f041fd4cd388c549ee2a29a9e5075882f))
* Shebaswap ([0x8faf958e36c6970497386118030e6297fff8d275](https://etherscan.io/address/0x8faf958e36c6970497386118030e6297fff8d275))
* Sakeswap ([0x2ad95483ac838e2884563ad278e933fba96bc242](https://etherscan.io/address/0x2ad95483ac838e2884563ad278e933fba96bc242))
* Croswap ([0x60a26d69263ef43e9a68964ba141263f19d71d51)](https://etherscan.io/address/0x60a26d69263ef43e9a68964ba141263f19d71d51)

<br>

---

<br>

## Setting your environment

Add your [Alchemy API key and endpoint](https://dashboard.alchemyapi.io/apps) to a `.env` file:

```
cp .env_example .env
vim .env
```

Create a virtual environment:

```
virtualenv venv
source venv/bin/activate
```

Install dependencies:

```
make install_deps
```

Install the CLI:

```
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

<img width="865" alt="Screen Shot 2022-03-31 at 10 30 50 PM" src="https://user-images.githubusercontent.com/1130416/161125216-10ec233f-0f64-48eb-8d1a-15e90d433266.png">

<br>

📝 TODO: remove namespace prints from options `bdex -h` (i.e. the extra `BALANCE BALANCE`, etc.).

<br>

### Checking the latest block


We leverage [Alchemy API endpoint `eth_blockNumber_hex`](https://docs.alchemy.com/alchemy/apis/ethereum/eth_blockNumber_hex) to get the latest block:

```
bdex -c
```

<br>

<img width="406" alt="Screen Shot 2022-03-31 at 1 15 25 PM" src="https://user-images.githubusercontent.com/1130416/161032451-685dee8b-8ed3-40c2-9391-191fa2abce35.png">

<br>

<br>

The block number can be checked against [ETHstat](https://ethstats.net/).

📝 TODO: Possible improvement for the future: We are crafting the checksum address string by hand without composing it by [Keccak-256 hashing the methods and parameters](https://docs.soliditylang.org/en/develop/abi-spec.html).

<br>

<img width="293" alt="Screen Shot 2022-03-31 at 1 15 19 PM" src="https://user-images.githubusercontent.com/1130416/161032358-86969275-7a72-406d-93bc-73906303a0cb.png">


<br>


### Getting the token balance for an exchange

We leverage [Alchemy API endpoint `eth_call`](https://docs.alchemy.com/alchemy/apis/ethereum/eth_call) to retrieve the current token balance for a specific exchange:

```
bdex -b dai uniswap
```
<br>

<img width="481" alt="Screen Shot 2022-03-31 at 10 26 21 PM" src="https://user-images.githubusercontent.com/1130416/161125262-4a623e23-adc9-4928-98c5-16dd67d3302b.png">



<br>


### Getting all token balances for all the exchanges

 We loop over the previous method for a list of tokens and exchanges:

```
bdex -a
```

<br>

<img width="407" alt="Screen Shot 2022-03-31 at 10 26 51 PM" src="https://user-images.githubusercontent.com/1130416/161125283-9a320c9b-a89b-4efa-832e-e0c315e2adf6.png">




<br>


### [Extra] Getting all token balances for all the exchanges with the web3 Python library

To be able to compare our results from the previous steps, we implemented an alternative way to fetch pair balances utilizing the [Python web3 library](https://web3py.readthedocs.io/en/stable/):

```
bdex -w
```
<br>

<img width="401" alt="Screen Shot 2022-03-31 at 10 27 25 PM" src="https://user-images.githubusercontent.com/1130416/161125363-ced644b9-8011-4f9f-b470-324e5f7e4079.png">


<br>

<br>

💡 For this library, it's necessary to supply the contracts' ABI (in our case, for [DAI](https://api.etherscan.io/api?module=contract&action=getabi&address=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2) and [WETH](https://api.etherscan.io/api?module=contract&action=getabi&address=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2), located at `./docs`)


💡 Note that a third option to verify token balances is through [Etherscan tokenholdings dashboard](https://etherscan.io/tokenholdings?a=0xa478c2975ab1ea89e8196811f51a7b7ade33eb11).


<br>


### Getting trading prices for all the exchanges

To get the current price for ETH/DAI in all the exchanges (e.g., as shown in [the projects' dashboards](https://v2.info.uniswap.org/pair/0xa478c2975ab1ea89e8196811f51a7b7ade33eb11)), run:


```
bdex -p weth dai 10
```

<br>
<img width="489" alt="Screen Shot 2022-04-01 at 10 26 54 AM" src="https://user-images.githubusercontent.com/1130416/161207492-0dcc6910-8c07-426a-b910-2cfd5336a1b5.png">


<img width="499" alt="Screen Shot 2022-04-01 at 10 27 25 AM" src="https://user-images.githubusercontent.com/1130416/161207508-9bd76eb8-4aac-467c-8801-a3211bed7fff.png">

<img width="523" alt="Screen Shot 2022-04-01 at 10 42 57 AM" src="https://user-images.githubusercontent.com/1130416/161209675-3ed3b07b-f16d-4227-9724-64ac733307ed.png">




<br>

#### How the price is calculated

An AMM replaces the buy and sell orders in an order book market with a liquidity pool of two assets, both valued relative to each other. As one asset is trader for the other, the relative prices of the two assets shift, and the new market rate for both is determined.

All the exchanges are forks from [UniswapV2](https://uniswap.org/blog/uniswap-v2), so they all use the same price formula for trading:

 ```
token_a_pool_size * token_b_pool_size = constant_product
 ```

To find the buy price, we add the quantity of pair tokens which we are using as the exchange (adding to the pool), and we substract the quantity of tokens we are buying (removing from the pool):

```
buy_price = (pair_token_balance + qty) / (token_balance - qty)
```

For sell price, we do the oppose:

```
sell_price = (pair_balance - qty) / (t1_balance + qty)
```



<br>


### Getting arbitrage

To run the algorithm to search for arbitrage in the supported exchanges, run:

```
bdex -x
```

<br>

<img width="511" alt="Screen Shot 2022-04-01 at 11 20 13 AM" src="https://user-images.githubusercontent.com/1130416/161214916-1a95feba-d5fb-4e60-b7fb-5962ad1bb3b8.png">


<br>
<br>

This is a very simple algorithm. Because our set of coins and exchanges is small, brute forcing is not so costly.

📝 TODO: improve this algorithm adding a node walking (graph solution).

<br>

### Running Docker container with arbitrage script

To run the arbitrage algorithm for a certain amount of minutes MIN, run:

```
bdex -r MIN
```

<br>


<img width="764" alt="Screen Shot 2022-04-01 at 11 37 31 AM" src="https://user-images.githubusercontent.com/1130416/161217688-c1aae8b9-6e8b-4a78-9ada-b6adeb066273.png">

<br>

<br>

Results will be saved into files names `results/<TIME_SAVED>.txt`.

<br>

📝 TODO: run the algorithm in several threads (if not running in a Docker container).

<br>

#### Running in docker

To run the algorithm in a separated container, first [install Docker](https://docs.docker.com/get-docker/). Then build the Docker image:

```
docker build -t bdex .
```

Finally, run the container (in a separate terminal tab):

```
docker run -v $(pwd):/results -it bdex sleep infinity
```

Results will also be available in files names `results/<TIME_SAVED>.txt`.

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


📝 TODO: add a script to mount results and save in disk after finished running the script.

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


