from binance.client import Client
import time
import json

timeconst = 1579349682.0
infos = {}
lastTrades = [None]*3
lastTradesCount = -1
specialOrders = True
tf = "%a, %d %b %Y %H:%M:%S"
filename = 'config.json'
circuitbreaker = True
initialized = True
firstrun = True

#read config file
try:
    with open(filename) as json_data_file:
        config = json.load(json_data_file)
except Exception as e:
    print(time.strftime(tf, time.gmtime()), '   not able to read config file, please fix and restart: ', e)
    initialized = False
#init binance client
try:
    client = Client(config['publickey'], config['secretkey'])
except Exception as e:
    print(time.strftime(tf, time.gmtime()), '   not able to init client (internet connection?), please fix and restart: ', e)
    initialized = False

def getMarketsInfo():
    global circuitbreaker
    try:
        info = client.get_exchange_info()
    except Exception as e:
        print(time.strftime(tf, time.gmtime()), '    circuitbreaker set to false, cant get market info from exchange: ', e)
        circuitbreaker = False

    formats = {}
    for i in range(len(config['pairs'])):
        key = config['pairs'][i]['market']
        format = {}

        for market in info['symbols']:
            if market['symbol'] == key:

                for filter in market['filters']:
                    if filter['filterType'] == 'LOT_SIZE':
                        stepSize = float(filter['stepSize'])
                        t = float(filter['stepSize'])
                        if t >= 1.0:
                            stepSizesFormat ='{:.0f}'
                        elif t == 0.1:
                            stepSizesFormat = '{:.1f}'
                        elif t == 0.01:
                            stepSizesFormat = '{:.2f}'
                        elif t == 0.001:
                            stepSizesFormat = '{:.3f}'
                        elif t == 0.0001:
                            stepSizesFormat = '{:.4f}'
                        elif t == 0.00001:
                            stepSizesFormat = '{:.5f}'
                        elif t == 0.000001:
                            stepSizesFormat = '{:.6f}'
                        elif t == 0.0000001:
                            stepSizesFormat = '{:.7f}'
                        elif t == 0.00000001:
                            stepSizesFormat = '{:.8f}'

                    if filter['filterType'] == 'PRICE_FILTER':
                        tickSize = (float(filter['tickSize']))
                        t = float(filter['tickSize'])
                        if t >= 1.0:
                            tickSizesFormat = '{:.0f}'
                        elif t == 0.1:
                            tickSizesFormat = '{:.1f}'
                        elif t == 0.01:
                            tickSizesFormat = '{:.2f}'
                        elif t == 0.001:
                            tickSizesFormat = '{:.3f}'
                        elif t == 0.0001:
                            tickSizesFormat = '{:.4f}'
                        elif t == 0.00001:
                            tickSizesFormat = '{:.5f}'
                        elif t == 0.000001:
                            tickSizesFormat = '{:.6f}'
                        elif t == 0.0000001:
                            tickSizesFormat = '{:.7f}'
                        elif t == 0.00000001:
                            tickSizesFormat = '{:.8f}'


        format['tickSizeFormat'] = tickSizesFormat
        format['stepSizeFormat'] = stepSizesFormat
        format['tickSize'] = tickSize
        format['stepSize'] = stepSize

        formats[key] = format

    return formats

def writeConfig():
    global circuitbreaker
    try:
        with open(filename, 'w') as outfile:
            json.dump(config, outfile)
    except Exception as e:
        print(time.strftime(tf, time.gmtime()), '    circuitbreaker set to false, cant write to file: ', e)
        circuitbreaker = False

def cancelAllOrders():
    global circuitbreaker
    circuitbreaker = True
    try:
        for i in range(len(config['pairs'])):
            key = config['pairs'][i]['market']
            crtOrders = client.get_open_orders(symbol=key)
            if len(crtOrders) > 0:
                for j, val in enumerate(crtOrders):
                    if crtOrders[j]['clientOrderId'][0:3] == 'SHN':
                        client.cancel_order(symbol=key, orderId=crtOrders[j]['orderId'])
                    time.sleep(1.05)

    except Exception as e:
        print(time.strftime(tf, time.gmtime()), '   circuitbreaker set to false, cannot cancel all orders: ', e)
        circuitbreaker = False
        time.sleep(5.0)

def processAllTrades():

    global config, lastTrades, lastTradesCount, ordersAllowed, circuitbreaker
    circuitbreaker = True

    try:
        for i in range(len(config['pairs'])):

            key = config['pairs'][i]['market']
            lastId = config['pairs'][i]['fromId']
            tradesTemp = client.get_my_trades(symbol=key, limit=1000,fromId=lastId+1)
            trades = []
            trades = sorted(tradesTemp, key=lambda k: k['id'])

            #process trades
            for j in range(len(trades)):

                try:

                    order = client.get_order(symbol=key, orderId=trades[j]['orderId'])

                    if order['clientOrderId'][0:3] == 'SHN':

                        if trades[j]['isBuyer']:
                            config['pairs'][i]['base_asset_qty'] = config['pairs'][i]['base_asset_qty'] + float(trades[j]['qty'])
                            config['pairs'][i]['quote_asset_qty'] = config['pairs'][i]['quote_asset_qty'] - float(trades[j]['quoteQty'])
                        else:
                            config['pairs'][i]['base_asset_qty'] = config['pairs'][i]['base_asset_qty'] - float(trades[j]['qty'])
                            config['pairs'][i]['quote_asset_qty'] = config['pairs'][i]['quote_asset_qty'] + float(trades[j]['quoteQty'])

                        config['pairs'][i]['fromId']=trades[j]['id']
                        writeConfig()

                        lastTradesCount = lastTradesCount + 1
                        if lastTradesCount >= 3:
                            lastTradesCount = 0
                        if trades[j]['isBuyer']:
                            print(time.strftime(tf, time.gmtime()), '   new trade (buy) :',key, ' qty: ', trades[j]['qty'], ' price: ', trades[j]['price'])
                            lastTrades[lastTradesCount]=' ' + str(time.ctime((float(trades[j]['time'])/1000.0))) + ' buy:' + '{0: <10}'.format(key) + ' qty: ' + '{0: <10}'.format(trades[j]['qty']) + ' price: ' + '{0: <10}'.format(trades[j]['price'])
                        else:
                            print(time.strftime(tf, time.gmtime()), '   new trade (sell):',key, ' qty: ', trades[j]['qty'], ' price: ', trades[j]['price'])
                            lastTrades[lastTradesCount] = ' ' + str(time.ctime((float(trades[j]['time'])/1000.0))) + ' sell:' + '{0: <10}'.format(key) + ' qty: ' + '{0: <10}'.format(trades[j]['qty']) + ' price: ' + '{0: <10}'.format(trades[j]['price'])

                except Exception as e:
                    print('')

            time.sleep(1.1)
    except Exception as e:
        print(time.strftime(tf, time.gmtime()), '   circuitbreaker set to fasle, not able to process all trades ',e)
        circuitbreaker = False

def sendOrders():
    global config,initialized,firstrun

    try:
        for i in range(len(config['pairs'])):

            circuitbreaker = True
            key = config['pairs'][i]['market']
            coin = float(config['pairs'][i]['base_asset_qty'])
            ticksize = infos[key]['tickSize']
            ticksizeformat = infos[key]['tickSizeFormat']
            stepsizeformat = infos[key]['stepSizeFormat']

            try:
                prices = client.get_ticker(symbol=key)
                circuitbreaker = True
            except Exception as e:
                circuitbreaker = False
                print(time.strftime(tf, time.gmtime()), '   not able to get price ',e)

            bidp = float(prices['bidPrice'])
            askp = float(prices['askPrice'])
            mid = ticksizeformat.format(0.5*(bidp+askp))

            totcoin = float(coin)
            totcash = float(config['pairs'][i]['quote_asset_qty'])

            fairp = totcash / totcoin

            awayFromBuy  = '{:.1f}'.format( 100.0 * (float(mid) - fairp) / fairp ) + '%'
            awayFromSell = '{:.1f}'.format( 100.0 * (float(mid) - fairp) / fairp ) + '%'
            awayFromMid =  (float(mid) - fairp) / fairp

            if specialOrders:
                if float(awayFromMid) >= 0.05:
                    bidpercentage = min(0.95,float(config['pairs'][i]['buy_percentage']))
                    askpercentage = max(1.05,1.0+float(awayFromMid))
                elif float(awayFromMid) <= -0.05:
                    bidpercentage = min(0.95,1.0+float(awayFromMid))
                    askpercentage = max(1.05,float(config['pairs'][i]['sell_percentage']))
                else:
                    bidpercentage = min(0.95, float(config['pairs'][i]['buy_percentage']))
                    askpercentage = max(1.05, float(config['pairs'][i]['sell_percentage']))
            else:
                bidpercentage = min(0.95, float(config['pairs'][i]['buy_percentage']))
                askpercentage = max(1.05, float(config['pairs'][i]['sell_percentage']))

            mybidp = bidpercentage * fairp
            myaskp = askpercentage * fairp


            if float(mid) < 0.99 * mybidp or float(mid) > 1.01 * myaskp:
                circuitbreaker = False
                print(time.strftime(tf, time.gmtime()), '   please inspect quantities config file as bot hits market')
                if firstrun:
                    initialized = False
            else:
                circuitbreaker = True


            mybidq = stepsizeformat.format((0.5 * (totcoin * mybidp + totcash) - totcoin * mybidp) * 1.0 / mybidp)
            myaskq = stepsizeformat.format((-0.5 * (totcoin * myaskp + totcash) + totcoin * myaskp) * 1.0 / myaskp)

            #start buy order
            orderbidp = ticksizeformat.format(min(mybidp,bidp+ticksize))
            orderbidq = mybidq
            if config['state'] == 'TRADE' and circuitbreaker:
                print(time.strftime(tf, time.gmtime()), '   send buy  order: ', '{0: <9}'.format(key),' p: ', '{0: <9}'.format(str(orderbidp)), ' q: ', '{0: <8}'.format(str(mybidq)), ' l:' , '{0: <9}'.format(str(mid)) , ' b:' , awayFromBuy)

                myId = 'SHN-B-' + key + '-' + str(int(time.time() - timeconst))
                try:
                    client.order_limit_buy(symbol=key, quantity=orderbidq,price=orderbidp,newClientOrderId=myId)
                except Exception as e:
                    print(time.strftime(tf, time.gmtime()), '   not able to send buy order for: ',key, ' because: ',e)
            else:
                print(time.strftime(tf, time.gmtime()), '   send DUMMY  buy order: ', '{0: <9}'.format(key),' p: ', '{0: <9}'.format(str(orderbidp)), ' q: ', '{0: <8}'.format(str(mybidq)), ' l:' , '{0: <9}'.format(str(mid)), ' b:' , awayFromBuy)

            #start sell order
            orderaskp = ticksizeformat.format(max(myaskp,askp-ticksize))
            orderaskq = myaskq
            if config['state'] == 'TRADE' and circuitbreaker:
                print(time.strftime(tf, time.gmtime()), '   send sell order: ', '{0: <9}'.format(key),' p: ', '{0: <9}'.format(str(orderaskp)), ' q: ', '{0: <8}'.format(str(myaskq)), ' l:' , '{0: <9}'.format(str(mid)), ' s:' , awayFromSell)

                myId = 'SHN-S-' + key + '-' + str(int(time.time() - timeconst))
                try:
                    client.order_limit_sell(symbol=key, quantity=orderaskq,price=orderaskp,newClientOrderId=myId)
                except Exception as e:
                    print(time.strftime(tf, time.gmtime()), '   not able to send sell order for: ',key, ' because: ',e)
            else:
                print(time.strftime(tf, time.gmtime()), '   send DUMMY sell order: ', '{0: <9}'.format(key),' p: ', '{0: <9}'.format(str(orderaskp)), ' q: ', '{0: <8}'.format(str(myaskq)), ' l:' , '{0: <9}'.format(str(mid)), ' s:' , awayFromSell)

    except Exception as e:
        print(time.strftime(tf, time.gmtime()), '    not able to send orders ',e)

    firstrun = False

wait_interval_sec = float(config['sleep_seconds_after_cancel_orders'])
quote_interval_sec = float(config['sleep_seconds_after_send_orders'])
rebalance_interval_sec = float(config['rebalance_interval_sec'])
lastUpdate = time.time()

if initialized:
    print(time.strftime(tf, time.gmtime()), '   start initializing')
    infos = getMarketsInfo()
    time.sleep(5)
    print(time.strftime(tf, time.gmtime()), '   end initializing')

    print(time.strftime(tf, time.gmtime()), '   start cancel all orders')
    cancelAllOrders()
    print(time.strftime(tf, time.gmtime()), '   end cancel all orders')
    rebalanceUpdate = time.time() #if start with rebalance:   - rebalance_interval_sec -1.0

while True and initialized:

    if not circuitbreaker:
        print(time.strftime(tf, time.gmtime()), '   circuitbreaker false, do not send orders')
    else:

        print(time.strftime(tf, time.gmtime()), '   start processing trades')
        processAllTrades()
        print(time.strftime(tf, time.gmtime()), '   end processing trades')

        #send orders special or normal
        lastUpdate = time.time()
        if time.time() > rebalanceUpdate + rebalance_interval_sec and rebalance_interval_sec > 0:
            rebalanceUpdate = time.time()
            print(time.strftime(tf, time.gmtime()), '   start sending special orders')
            specialOrders = True
            sendOrders()
            specialOrders = False
            print(time.strftime(tf, time.gmtime()), '   end sending special orders')
        else:
            print(time.strftime(tf, time.gmtime()), '   start sending orders')
            sendOrders()
            print(time.strftime(tf, time.gmtime()), '   end sending orders')

        for i in range(len(lastTrades)):
            if lastTrades[i] != None:
                print(time.strftime(tf, time.gmtime()), '   last 3 trades: ', lastTrades[i])

    print(time.strftime(tf, time.gmtime()), '   sleep for: ', quote_interval_sec, ' seconds')
    time.sleep(quote_interval_sec)

    #canel orders
    lastUpdate = time.time()
    print(time.strftime(tf, time.gmtime()), '   start cancel all orders')
    cancelAllOrders()
    print(time.strftime(tf, time.gmtime()), '   end cancel all orders')

    print(time.strftime(tf, time.gmtime()), '   sleep for: ' , wait_interval_sec , ' seconds')
    time.sleep(wait_interval_sec)



