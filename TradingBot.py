import json
from threading import Thread
from BaseRequests import BaseRequests
from keys import keys
import pandas as pd
import time
logFile = open("logfile.txt", "w")
bought = False

# defining the 3 symbols the bot will be working with
instrument1 = "CAD_SGD"
instrument2 = "EUR_USD"
instrument3 = "EUR_CAD"

#This class defines a function to get the candlestick data
class CANDLES(BaseRequests, keys):
    def getCandleData(self, instrument, count, granularity):
        params = dict(
            count=count,
            granularity=granularity,
            price = "M"
        )
        endpoint = f"instruments/{instrument}/candles"
        response = self.get(endpoint = endpoint, params = params, headers=self.SECURE_HEADER)
        return response

#This class defines a function to buy 100 units of a symbol
class BUY(BaseRequests, keys):
    def order(self, instrument, units):
        data = {
            "order": {
                "units": units,
                "instrument": instrument,
                "type": "MARKET"
            }
            }
        endpoint = f"accounts/{self.ACCOUNT_ID}/orders"
        response = self.post(endpoint = endpoint, data = data, headers=self.SECURE_HEADER)
        return response

#This class defines a function to sell
class SELL(BaseRequests, keys):
    def sell(self, instrument, lap, orderID):
        data = {
            "order": {
                "timeInForce": "GTC",
                "price": lap,
                "type": "TAKE_PROFIT",
                "tradeID": tradeID
            }
            }
        endpoint = f"accounts/{self.ACCOUNT_ID}/orders/{orderID}"
        response = self.put(endpoint = endpoint, data = data, headers=self.SECURE_HEADER)
        return response

# this is the function assigned for the bot
def BOT(instrument):
    logFile.write("Trade Algorithm started and waiting to analyze the trend for 15 minutess !\n")
    time.sleep(1)
    d = CANDLES()
    response = d.getCandleData(instrument, 1, "M15")
    js = json.loads(response.text)
    print(js)
    js = js['candles']
    js = js[0]
    js = js['mid']
    high = js['h']
    low = js['l']
    logFile.write("Found the open reach breakout values. High = " + high + " and low = " + low +  "\n")
    LTPs = pd.DataFrame(columns=[instrument])
    while True:
        can = CANDLES()
        response = can.getCandleData(instrument, 1, "S30")
        js = json.loads(response.text)
        print(js)
        js = js['candles']
        js = js[0]
        js = js['mid']
        ltp = js['c']
        LTPs = LTPs.append({instrument: ltp}, ignore_index=True)
        print(LTPs)
        logFile.write("The LTP of " + instrument + " is " + ltp +  "\n")
        if ltp > high and bought == False:
            can = BUY()
            units = 100
            response = can.order(instrument, units)
            js = json.loads(response.text)
            orderIDins = js['orderCreateTransaction']['id']
            logFile.write("Bought " + instrument+ " and the order id is " + orderIDins +  "\n")
            print(orderIDins)
            bought = True
        if ltp < low and bought == True:
            can = SELL()
            response = can.sell(instrument, ltp, orderIDins)
            js = json.loads(response.text)
            print(js)
            logFile.write("Sold " + instrument + "\n")
            bought = True

Thread1 = Thread(target=BOT(instrument1), args=(instrument1,))
Thread2 = Thread(target=BOT(instrument2), args=(instrument2,))
Thread3 = Thread(target=BOT(instrument3), args=(instrument3,))

Thread1.start()
Thread2.start()
Thread3.start()

Thread1.join()
Thread2.join()
Thread3.join()


logFile.close()