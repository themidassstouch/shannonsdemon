---
layout: default
---

# **GET YOUR BOT STARTED:**

![shannonsdemon.exe](bot.png)

<p align="justify">
Please find instructions on how to use your bot below. At the moment the bot only works for Binance. Above picture shows the bot running for 3 different pairs namely BNBUSDT,ETHUSDT and LTCUSDT. In the instructions below we show all steps needed to mimic the bot from the picture along with some explanation of the bot and the different parameters that can be set. Changing parameters or adding and removing pairs should be straightforward after reading these steps. The picture below shows the config.json file that is used for setting the pairs and parameters in our example. You can use any text editor (for example notepad++) to alter it. We prefer visual code which can be downloaded here: <a href="https://code.visualstudio.com/">[link]</a>.
</p>

![config.json](config.png)


## **STEP 1: SET UP YOUR TRADING ACCOUNT.**
<p align="justify">
1. Open a trading account on the Binance exchange. Please use this <a href="https://www.binance.com/nl/register?ref=R9NNDYS8">[link]</a> as you receive a 10% discount on trading fees. Actually the discount is 20% but 10% is donated to us. In my opinion it is easiest to have a new (empty) account used solely for this bot as it makes initializing, debugging, allocating value to different portfolios (pairs) and PnL calculations much easier. Obviously you can use an existing account also.   
</p>
<p align="justify">
2. Create api keys for your account. The bot needs the trading option to be enabled (disabled by default) Make sure to keep the withdrawal option disabled for obvious reasons. Find instructions on how to create api keys on Binance here: <a href="https://www.binance.com/en/support/articles/360002502072">[create api keys]</a> Copy the public and secret key from Binance to the config file's 'publickey' and 'secretkey' attributes.
</p>
<p align="justify">
3. Fund your account and buy the pairs that you want to trade. In our example we allocate aprroximately 480 USDT to each of the three pairs. Therefore we buy approximately 16.29 BNB and 240 USDT for the first pair (BNBUSDT, price = 14.75), 1.11 ETH and 240 USDT for the second pair (ETHUSDT, price = 216) and 5.74 LTC and 240 USDT for the third pair (LTCUSDT, price = 41.85). Theoretically you don't need to own the full amount of asset A or asset B however you might not be able to sell or buy at some point in time if you don't.
</p>

## **STEP 2: DOWNLOADING / INSTALLING YOUR BOT.**

<p align="justify">
1. Download shannonsdemon.exe and config.json from the github repository master branch. The executable is the result of shannonsdemon.py being compiled using pyinstaller. For now only windows is supported unless you run the python script (shannonsdemon.py) Installing it will not be covered as somebody with enough knowledge should be able to set it up him- or herself easily.
</p>
<p align="justify">
2. Make sure the executable and the config.json file are located the same folder as the executable. If not the bot will throw an error message that it can't find the config file.
</p>
<p align="justify">
3. The bot can simply be started by double clicking the executable. Be aware that it immediately starts trading if the attribute 'state'is set to TRADE in the config file.
</p>

## **STEP 3: SETTING THE CONFIG FILE.**

<p align="justify">
1. The 'state' attribute controls whether orders are send to the exchange or not. If not set to TRADE (TEST for example), the bot runs like it does with 'state' set to TRADE except that it doesn't send the orders. The bot instead shows DUMMY orders in the terminal. It can be used to check your settings before sending real orders. We advise to always start your bot with 'state' set to TEST so that you can see if you agree with the orders being send. If for example you have made a mistake in the value of asset A (base asset) and/or asset B (quote asset), the price of your dummy orders is deviating a lot from current market bid or ask. Set it to TEST.
</p>
<p align="justify">
2. The 'secretkey' and 'publickey' attributes should match the keys generated in your binance account. See step 1.2 also.
</p>
<p align="justify">
3. The 'sleep_seconds_after_send_orders', 'sleep_seconds_after_cancel_orders' and 'rebalance_interval_sec' determine the rythm of the rebalancing. The bot always starts with sending regular orders. After sending the orders it sleeps for 'sleep_seconds_after_send_orders' amount of time. When it wakes up it cancels all orders and sleeps again for 'sleep_seconds_after_cancel_orders' amount of time. The last attribute ('rebalance_interval_sec') determines how often you want to send special orders. Special orders are rebalancing not at a price difference specified by the config file ('buy_percentage' and 'sell_percentage') but at any price difference given that it is more than 5% (to offset fees).
</p>
<p align="justify">
4. The attribute 'pairs' is an array of the different pairs you want to trade. You can add or remove all the pairs you want. The 'market' attribute (e.g. BNBUSDT) should be obvious. You can also add pairs like BNBBTC. The 'base_asset_qty' and 'quote_asset_qty' are the quantities of allocated to the respective legs of the pair. The base asset is always the first coin of the pair (BNB) The quote asset is always the second asset (USDT) The 'buy_percentage' and 'sell_percentage' attributes determine the price of the orders that you send. For example BNBUSDT is at the current price of 14.75 and quantities equal to 16.29 and 240 perfectly balanced. The price of your buy and sell orders, with these attributes equal to 0.9 and 1.1, are equal to 13.27 and 16.22 respectively. That is 10% away from equilibrium. The 'fromId' attribute is the id of the last trade that is done by the bot. For new pairs you should always set it to 0. For existing pairs or if you want to change the value allocated to this strategy always let the bot set it. This can be done by starting the bot first with 'state' unequal to TRADE.
</p>

## **STEP 4: ALMOST THERE.**
<p align="justify">
It is very important that you always start the bot with 'state' unequal to TRADE (e.g. TEST) to check if your orders make sense. We advise to always start your bot following the steps below.
</p>
<p align="justify">
1. Start the bot with 'state' equal to TEST. New trades are processed and quantities and 'fromId' in the config file are updated accordingly. Do not check orders yet.
</p>
<p align="justify">
2. Check the 'base_asset_qty' and 'quote_asset_qty' to see if all pairs are balanced. Also change the quantities if you want to allocate more or less value to a pair. Re-start the bot with 'state' equal to TEST. Check order prices.  
</p>
<p align="justify">
3. If all orders are ok then change the 'state' to TRADE and start your bot.
</p>

## **DEBUGGING**
<p align="justify">
For most errors the bot shows a message that is self explanatory. Please see bullets below for more info and possible solutions. Please contact us 
</p>
<p align="justify">
All messages related to time sync. The time of your computer is not in sync with the time of binance servers. Please sync your computer's clock. We have also seen that the time of the router needed to be synced.
</p>
<p align="justify">
Message '   circuitbreaker set because at crt price we hit market, please inspect config file' The pair for which the bot tries to send orders is so far away from equilibrium price that it would hit market immediately. Usually it means that the quantities in your log file are wrong. Sometimes, in very volatile markets, it can happen that the price moves so much (e.g. > 2x 'sell_percentage') in between an update cycle of your bot that you also get this message. You can trade and update quantities in config file accordingly.  
</p>
<p align="justify">
Message that contains 'min_notional' This happens when the order that the bot wants to send is less than the minimal order value required by Binance. Ignore this error or allocate more value to pair.
</p>
<p align="justify">
All messages related to the fact that the config file cannot be found. The config file must be located in the same folder as the bot is.
</p>
<p align="justify">
The bot uses Samm Chardy python-binance library. You can always look here for additional info. <a href="https://python-binance.readthedocs.io/en/latest/">[python-binance]</a>
</p>

[back](./)