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

### Checking the latest block


We leverage [Alchemy API endpoint `eth_blockNumber_hex`](https://docs.alchemy.com/alchemy/apis/ethereum/eth_blockNumber_hex) to get the latest block:

```
bdex -c
```

<br>

<img width="406" alt="Screen Shot 2022-03-31 at 1 15 25 PM" src="https://user-images.githubusercontent.com/1130416/161032451-685dee8b-8ed3-40c2-9391-191fa2abce35.png">

<br>

The block number can be checked against [ETHstat](https://ethstats.net/).

<br>

<img width="293" alt="Screen Shot 2022-03-31 at 1 15 19 PM" src="https://user-images.githubusercontent.com/1130416/161032358-86969275-7a72-406d-93bc-73906303a0cb.png">


<br>


### Getting the token balance for an exchange

We leverage [Alchemy API endpoint `eth_call`](https://docs.alchemy.com/alchemy/apis/ethereum/eth_call) to retrieve the current token balance for an specific exchange:

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

For this library, it's necessary to supply the contracts' ABI (in our case, for [DAI](https://api.etherscan.io/api?module=contract&action=getabi&address=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2) and [WETH](https://api.etherscan.io/api?module=contract&action=getabi&address=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2) - located at `./docs`)


Note that a third option to verify token balances is through [Etherscan tokenholdings dashboard](https://etherscan.io/tokenholdings?a=0xa478c2975ab1ea89e8196811f51a7b7ade33eb11).


<br>


### Getting trading prices for all the exchanges

To get the current price for ETH/DAI in all the exchanges (e.g., as showed in [the projects' dashboards](https://v2.info.uniswap.org/pair/0xa478c2975ab1ea89e8196811f51a7b7ade33eb11)), run:


```
bdex -p weth eth 10
```

<br>

<img width="484" alt="Screen Shot 2022-03-31 at 10 28 33 PM" src="https://user-images.githubusercontent.com/1130416/161125333-710dc123-206c-488c-9369-7992481f0e4f.png">


#### How the price is calculated

All the exchanges are forks from [UniswapV2](https://uniswap.org/blog/uniswap-v2), so they all use the same price formula for trading:

 ```
price = balance_token1 * balance_token2 = constant
 ```

TODO: add info on selling/buying price


<br>


### Getting arbitrage

To run the algorithm to search for arbitrage in the supported exchanges, run:

```
bdex -x
```

<br>

<img width="509" alt="Screen Shot 2022-03-31 at 10 29 21 PM" src="https://user-images.githubusercontent.com/1130416/161125421-524d1f9c-f4ca-4c60-91ea-4a26062c040f.png">

<br>

TODO: explain how the algorithm works

<br>

### Running Docker container with arbritage script

To run the arbitrage algorithm for a certain amount of minutes MIN, run:

```
bdex -r MIN
```

<br>

<img width="434" alt="Screen Shot 2022-03-31 at 10 30 06 PM" src="https://user-images.githubusercontent.com/1130416/161125459-b5e17e3a-4e24-43d7-81ba-4c911a1d6c7d.png">

<br>

Results will be saved into files names `results/<TIME_SAVED>.txt`.

#### Running in docker

To run the algorithm in a separated container, first [install Docker]().

Then build the Docker image:

```
docker build -t bdex .
```

Finally, run the container:

```
docker run -d bdex
```

Results will be also be available into files names `results/<TIME_SAVED>.txt`. 

You can inspect your container at any time with:

```
docker ps
```

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
