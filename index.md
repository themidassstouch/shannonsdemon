---
layout: default
---

Welcome to the homepage of Shannon's Demon. The bot that let's you trade cryptocurrencies on binance exchange following a 50/50 rebalancing strategy a.k.a. Shannon's Demon.

![shannonsdemon.exe](bot.png)

This site is currently under construction. Please be patient as we are working hard to get proper documentation and workinstructions in place. For the time being, please find below a short version of how to get your bot working.

# GET THE BOT STARTED:

- Create a new binance account. Create api keys for your account (**disable withdrawal option** but enable trading option). Fund your account. Please use this link. It uses our referral code: [Binance](https://www.binance.com/en/register?ref=43234524).
- Download either shannonsdemon.exe and config.json or create python project by cloning repository master branch (or any other way). The python project assumes you know how to create one, feel free to set it up any way you like. If you choose the first option, be sure to put both files in the same folder. If you choose the latter, be sure to put the config file in the working directory so script can find it.
- Update the config.json file:
 - Put STATE to "TEST". This let's you run the tool as it would do in TRADE state but prevents sending real orders to the exchange. This way you can see if your settings are ok Only if you are sure of the correct settings change STATE to "TRADE" 
 - Enter api public and secret key
 - Put sleep_seconds_after_send_orders, sleep_seconds_after_cancel_orders and rebalance_interval_sec to 180, 60 and 1080. This way the bot waits 180 sec after sending orders. Then wait 60 sec after cancelling orders. Every 1080 seconds the bot rebalances no matter how far away the market price is from the equilibrium price (=price at which you are perfectly balanced). However not if it is less than 5% away as you have to make up for fees too.
  - Enter all pairs (markets) that the bot should trade. Please see config.json as example. Be carefull: fromID should be 0 only when you first initialize. It keeps strack of the trades it already processed. The buy and sell percentage lets you set the price of your orders as a percentage away from the equilibrium price. The base and quote asset quantity lets you set the amount of coins that you want to allocate to this portfolio. For the example below, you are at equilibrium if the price is 98.5 / 27285.79 = 0.00360994.
- Start your bot by double clicking the .exe or run python script. Be sure to first start with STATE set to something different than TRADE, TEST for example.

![config.json](config.png)

# DONATE:

Besides opening and trading using a binance account using our referral: [Binance](https://www.binance.com/en/register?ref=43234524). Feel free to donate so we can keep developing:

1. ETH:   '0x13d55ca40ca3d008b7b0a0118d295f510410b60f'
2. USDT:  '0x13d55ca40ca3d008b7b0a0118d295f510410b60f'
3. BTC:   '1Fxyo5jfMxkDgGDjiAU9KE7svEG6Drriyv'
4. LTC:   'Lbqi2McxsrhM2NR3FtgiMiF2JxswFBsmMX'

# USEFUL LINKS:
[error message documentation (not complete)](https://python-binance.readthedocs.io/en/latest/)
[Shannon's Demon explained](https://thepfengineer.com/2016/04/25/rebalancing-with-shannons-demon/)