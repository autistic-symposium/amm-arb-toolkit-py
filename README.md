# 🪙✨ bDEX

<br>


### A package and CLI tool for making API calls to get data and arbitrage for specified tokens/exchange pools.

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
pip3 -r requirements.txt
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

### Checking the latest block

To connect to Ethereum and get the latest block, run:

```
bdex -c
```

<img width="406" alt="Screen Shot 2022-03-31 at 1 15 25 PM" src="https://user-images.githubusercontent.com/1130416/161032451-685dee8b-8ed3-40c2-9391-191fa2abce35.png">

The block number can be checked against [ETHstat](https://ethstats.net/).

<img width="293" alt="Screen Shot 2022-03-31 at 1 15 19 PM" src="https://user-images.githubusercontent.com/1130416/161032358-86969275-7a72-406d-93bc-73906303a0cb.png">


<br>


### Getting the token balance for an exchange

We use [Alchemy API endpoint `eth_call`](https://docs.alchemy.com/alchemy/apis/ethereum/eth_call) to retrieve the current token balance for an specific exchange:

```
bdex-b dai uniswap
```

<img width="492" alt="Screen Shot 2022-03-31 at 1 14 24 PM" src="https://user-images.githubusercontent.com/1130416/161032288-28d3d980-ff54-45f2-9355-32d41f189ac6.png"> 



<br>


### Getting all token balances for all the exchanges

 We loop over the previous method for a list of tokens and exchanges:

```
bdex -a
```

<img width="399" alt="Screen Shot 2022-03-31 at 3 06 44 PM" src="https://user-images.githubusercontent.com/1130416/161041695-68dbcb58-40af-48ac-8542-d668bd67f2cb.png">


<br>


### [Extra] Getting all token balances for all the exchanges with the web3 lib

To be able to compare our results from the previous steps, we implemented an alternative way to fetch pair balances utilizing the [Python web3 library](https://web3py.readthedocs.io/en/stable/):

```
bdex -w
```

<img width="390" alt="Screen Shot 2022-03-31 at 3 07 03 PM" src="https://user-images.githubusercontent.com/1130416/161041712-fb641492-27a3-4d00-b4b0-7b8a6f8021b8.png">




Note that for utilize this library we had to retrieve the contract ABI for [DAI](https://api.etherscan.io/api?module=contract&action=getabi&address=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2) and [WETH](https://api.etherscan.io/api?module=contract&action=getabi&address=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2) (located at `./docs`)



<br>


### Getting raw pair prices across all the exchanges

To get the current price for ETH/DAI in all the exchanges (as showed in [their dashboards](https://v2.info.uniswap.org/pair/0xa478c2975ab1ea89e8196811f51a7b7ade33eb11), run:


```
bdex -p  dai eth
```

<img width="484" alt="Screen Shot 2022-03-31 at 3 28 49 PM" src="https://user-images.githubusercontent.com/1130416/161045235-b29242d5-e32e-4865-8e6a-13b3d113adca.png">



Note that all the exchanges are forks from Uniswap, using the same price formula for trading on UniswapV2:

 ```
 t1 * t2 = p
 ```

<br>


### Getting buying and selling prices for all the exchanges

TO BE ADDED (working on)


<br>

### Getting arbitrage

TO BE ADDED (working on)


<br>

### Running Docker container with arbritage script

TO BE ADDED (working on)


---

<br>

## Development

### Running the linter

```
make lint
```

### Running tests

```
make test
```
