import requests
import json
from threading import Thread
import datetime


class TradeAlgo:
    """
    This class defines how a trade oblecj will be
    """
    
    def __init__(self, apiKey, baseUrl, searchDate):
        """
        Parameters
        ----------
        apiKey : String
            This is the Key that API uses for authentication.
        baseUrl : String
            Base URL for API requests.
        Returns
        -------
        None.
        """
        self.apiKey = apiKey   
        self.baseUrl = baseUrl
        self.searchDate = searchDate
    
    def getFifteenMinRequest(self,symbol):
        """
        Parameters
        ----------
        symbol : [String]
            First element is base symbol
            Second elemnt is quote symbol
            Ex: EURCAD
        Returns
        -------
        fifteenMinResponse : String JSON
            Response of the API request. Need to be Parsed.
        """
        typeURL = 'candle.json?api_key='
        candleURL = self.baseUrl + typeURL + self.apiKey + '&date_time=' + self.searchDate + 'T00:15:00+00:00&base=' + symbol[0] + '&quote=' + symbol[1] + '&fields=highs&fields=lows'
        
        fifteenMinResponse = requests.get(candleURL)
        return fifteenMinResponse
    
    def getCurrentRates(self,symbol):
        """
        
        Parameters
        ----------
        symbol : [String]
            First element is base symbol
            Second elemnt is quote symbol
            Ex: EURCAD
        Returns
        -------
        currentResponse : String JSON
            Response of the API request. Need to be Parsed.
        """
        

        typeURL = 'spot.json?api_key='
        currentRateURL = self.baseUrl + typeURL + self.apiKey + '&base=' + symbol[0] + '&quote=' + symbol[1]
        currentResponse = requests.get(currentRateURL)
        return currentResponse


def checkORB(currentValue, fifteenHigh, fifteenLow):
    """
    Check if the current value is highed than fifteen minute high val, or lower than fifteen minute low val
    Parameters
    ----------
    currentValue : Float
        Current Value of the symbol.
    fifteenHigh : Float
        Fifteen Minute after opening Candle's High value. 
    fifteenLow : Float
        Fifteen Minute after opening Candle's Low Value.
    Returns
    -------
    str
        Returns BUY, SELL or HOLD for current symbol according to comparison.
    """
    
    if currentValue > fifteenHigh:
        return "buy"
    elif currentValue < fifteenLow:
        return "sell"
    return None

def createORB(symbol):
    """
    Create and Trade object for selected symbol and Create 15 minORB signal.
    Parameters
    ----------
    symbol : [String]
        First element is base symbol
            Second elemnt is quote symbol
            Ex: EURCAD
    Returns
    -------
    None.
    """
    logFile.write("\tCurrent values of " + symbol[0] + symbol[1] + " asked\n")
    current = newTrade.getCurrentRates(symbol)
    logFile.write("\tCurrent value response status code for " + symbol[0] + symbol[1] + " is " + str(current.status_code) + "\n")
    logFile.write("\tFifteen Minute Candle value of " + symbol[0] + symbol[1] + " asked\n")
    fifteenMin = newTrade.getFifteenMinRequest(symbol)
    logFile.write("\tFifteen Minute Candle value response status code for " + symbol[0] + symbol[1] + " is " + str(fifteenMin.status_code) + "\n")

    currentJson = json.loads(current.text)
    fifteenMinJson = json.loads(fifteenMin.text)
    
    currentValue = float(currentJson['quotes'][0]['ask'])
    fifteenHigh = float(fifteenMinJson['quotes'][0]['high_ask'])
    fifteenLow = float(fifteenMinJson['quotes'][0]['low_ask'])
    result = checkORB(currentValue, fifteenHigh, fifteenLow)
    
    if result == "buy":
        print(symbol[0] + symbol[1] + " = BUY")
    elif result == "sell":
        print(symbol[0] + symbol[1] + " = SELL") 
    else:
        print(symbol[0] + symbol[1] + " = HOLD")


apiKey = "xffq5RFlOSJe0H7HcAKEStbA"      
baseUrl = 'https://www1.oanda.com/rates/api/v2/rates/'

today = datetime.datetime.now()
deltaTime = datetime.timedelta(days = 1)
requestTime = today-deltaTime
indis = str(requestTime).find(" ")
requestTime = str(requestTime)[:10]

newTrade = TradeAlgo(apiKey,baseUrl,requestTime)

logFile = open("logfile.txt", "w")
logFile.write("Trade Algorithm starts at " +str(datetime.datetime.now())+ " !\n")

symbols= [['EUR', 'AUD'], ['EUR', 'CHF'], ['EUR', 'USD']]

firstThread = Thread(target=createORB, args=(symbols[0],))
secondThread = Thread(target=createORB, args=(symbols[1],))
thirdThread = Thread(target=createORB, args=(symbols[2],))

firstThread.start()
secondThread.start()
thirdThread.start()

firstThread.join()
secondThread.join()
thirdThread.join()

logFile.write("Trade Algorithm finish working at " +str(datetime.datetime.now())+ " !\n")
logFile.close()