'''
This web service extends the Alphavantage api by creating a visualization module,
converting json query results retuned from the api into charts and other graphics.

This is where you should add your code to function query the api
'''
import requests
from datetime import datetime
from datetime import date
import pygal
import re

apikey = "O1RSZBGP6WA65EAI"

#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()

def do_this_2():
    c = 0
    choicesList = []
    data = requests.get('https://pkgstore.datahub.io/core/nyse-other-listings/nyse-listed_json/data/e8ad01974d4110e790b227dc1541b193/nyse-listed_json.json').json()
    for d in data:
        ticker = d['ACT Symbol']
        msg = (ticker, ticker)
        if '$' not in ticker:
            if '.' not in ticker:
                choicesList.append(msg)
    return choicesList

def validate(date_info):
    try:
        dateRegex = '^[0-9]{4}.(1[0-2]|0[1-9]).(3[01]|[12][0-9]|0[1-9])'
        if re.search(dateRegex, date_info):
            datetime.datetime.strptime(date_info, '%Y-%m-%d')
            return True
        else:
            raise ValueError
    except ValueError:
        print("ERROR - Incorrect data format: should be YYYY-MM-DD - Validate()")


def createData(jsonData, index, opening, highs, lows, closing, dates, mode):
    if mode == 1:
        # IF WE ARE PULLING FOR DATA FOR THE SAME STOP AND START DATE, WE OMIT THE DATE AND ONLY SHOW THE TIME
        timeonly = str(index).split(' ')[1]
        dates.append(timeonly)
    else:
        # THE INDEX IS THE DATE ON ALL FUNCTIONS
        dates.append(index)

    dataOpening = (jsonData[index]["1. open"])
    opening.append(float(dataOpening))

    dataHigh = (jsonData[index]["2. high"])
    highs.append(float(dataHigh))

    dataLow = (jsonData[index]["3. low"])
    lows.append(float(dataLow))

    dataClosing = (jsonData[index]["4. close"])
    closing.append(float(dataClosing))


def reverseLists(opening, highs, lows, closing, dates):
    opening.reverse()
    highs.reverse()
    lows.reverse()
    closing.reverse()
    dates.reverse()

def makeGraph(data, chartType, chartTimeSeries, chartStartDate, chartEndDate):
    #print(data)
    ticker = data['Meta Data']['2. Symbol']

    opening = []
    highs = []
    lows = []
    closing = []
    dates = []

    labels = list(data)[1]
    dailyInformation = data[labels]
    #print(chartStartDate)
    #print(chartEndDate)
    for i in dailyInformation:
        date = str(i)
        #print(date)
        # IF THE USER WANTS A GRAPH OF 1 DAY
        if chartStartDate == chartEndDate:
            # CHECK IF THE TIME SERIES IS SET TO INTRADAY
            if chartTimeSeries == 'TIME_SERIES_INTRADAY':
                # CHECK IF THE CHART START DATE IS IN THE STRING OF DATE1
                if str(chartStartDate) in date:
                    # IF IT IS - SPLIT THEM AT THE SPACE AND ONLY TAKE THE TIME PORTION.
                    createData(dailyInformation, date, opening, highs, lows, closing, dates, 1)

        # IF THE USER WANTS A GRAPH OF OVER 1 DAY
        else:
            # IF THE LOOP INDEX (AKA DATE) IS IN BETWEEN THE START AND STOP DATE, PULL THE DATA
            if chartStartDate < date < chartEndDate or chartEndDate in date:
                createData(dailyInformation, date, opening, highs, lows, closing, dates, 0)

    chart = chartType
    reverseLists(opening, highs, lows, closing, dates)
    chart.title = 'Stock Data for {}: {} to {} '.format(ticker, chartStartDate, chartEndDate)
    chart.x_labels = dates
    chart.add('Opening', opening)
    chart.add('High', highs)
    chart.add('Low', lows)
    chart.add('Closing', closing)
    return chart.render()



# THE PURPOSE OF THE getJsonPage FUNCTION IS TO RUN THE PROGRAM
def getJsonPage(info):
    # FIRST WE PASS info WHICH CONTAINS THE Symbol, chartType, chartTimeSeries , chartStartDate, chartEndDate

    # THEN WE ASSIGN VARIABLES BY THE TUPLE INDEX
    symbol = info[0]

    # THOSE VARIABLES ARE BROKEN DOWN INTO API ENDPOINT COMPONENTS
    # E.G (TIME_SERIES_INTRADAY,TIME_SERIES_DAILY) OR THEIR RESPECTIVE DATES TO BE LOOKED FOR WITHIN THE API RESULTS
    chartType = int(info[1])
    if chartType == 1: chartType = pygal.Bar(x_label_rotation=-45)
    elif chartType == 2: chartType = pygal.Line(x_label_rotation=-45)


    intraDayInfo = "&interval=30min"

    chartTimeSeries = info[2]
    if chartTimeSeries == "1": chartTimeSeries = "TIME_SERIES_INTRADAY"
    elif chartTimeSeries == "2": chartTimeSeries = "TIME_SERIES_DAILY"
    elif chartTimeSeries == "3": chartTimeSeries = "TIME_SERIES_WEEKLY"
    elif chartTimeSeries == "4": chartTimeSeries = "TIME_SERIES_MONTHLY"

    chartStartDate = str(info[3])
    chartEndDate = str(info[4])

    # AFTER THE VARIABLES ARE ASSIGNED WE BUILD THE LINK AND EXECUTE THE GET REQUEST.
    # -> WE PRINT THE BUILT URL TO THE CONSOLE FOR DEBUGGING PURPOSES
    baseLink = "https://www.alphavantage.co/query?"
    queryData = "function={}&symbol={}{}&apikey={}".format(chartTimeSeries, symbol, intraDayInfo, apikey)
    req = requests.get(baseLink + queryData)
    print(req.url)

    # WE LOAD THE REQUEST RESPONSE INTO A VARIABLE CALLED DATA AND USE THE JSON() FUNCTION TO PARSE THE TEXT.
    data = req.json()

    # FINALLY, WE CHECK IF THERE WAS A STRING OF 'INVALID API CALL' IN THE RESPONSE
    # IF THERE IS WE PRINT AN ERROR MESSAGE INSTEAD OF BUILDING THE GRAPH IN BROWSER
    if 'Invalid API call' not in req.text:
        return makeGraph(data, chartType, chartTimeSeries, chartStartDate, chartEndDate)
    else:
        print("The Ticker You Entered is Not in The API\n")
